"""Exercise two typical source edits in a temporary directory, not the candidates."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import subprocess
import time
import xml.etree.ElementTree as ET

from build_figures import HERE, ROOT, intervals


def main():
    data = json.loads((HERE / "data.json").read_text())
    binary = Path("/home/reggie/.local/share/jiaocai-tools/drawio-32.4.1/opt/drawio/drawio")
    with TemporaryDirectory(prefix="jiaocai-figure-edit-") as temporary:
        out = Path(temporary)
        # A normal GUI-style label edit changes two XML values; edge IDs stay stable.
        tree = ET.parse(ROOT / "assets/figures/teaching-pilot/fig1-2-candidate.drawio")
        changed_ids = []
        for node in tree.iter("mxCell"):
            if node.get("id") in {"b", "count-b"}:
                node.set("value", "b′")
                changed_ids.append(node.get("id"))
        graph = out / "label-edit.drawio"
        tree.write(graph, encoding="utf-8", xml_declaration=True)
        started = time.monotonic()
        subprocess.run(["xvfb-run", "-a", str(binary), "-x", "-f", "png",
                        "--width", "2441", "-o", str(graph.with_suffix(".png")),
                        str(graph), "--disable-gpu", "--no-sandbox"],
                       check=True, capture_output=True, timeout=90)
        graph_seconds = time.monotonic() - started
        graph_check = subprocess.run(
            ["/usr/bin/python3", str(ROOT / "skills/drawio-skill/scripts/validate.py"),
             str(graph), "--strict", "--json"],
            check=True, capture_output=True, text=True)
        # Change a teaching parameter and its explicit derived data, with no code edit.
        changed = deepcopy(data)
        expanded = changed["intervals"]["cases"][2]
        expanded["A_cleanup_minutes"] = 30
        expanded["effective_A"][1] = 690
        expanded["expected_overlap"][1] = 690
        started = time.monotonic()
        intervals(out, changed)
        time_seconds = time.monotonic() - started
        svg = (out / "fig1-6-candidate.svg").read_text()
        assert "共同占用 45 分钟" in svg
        assert "清理 30 分钟" in svg
        assert "11:30" in svg
        assert "清理 20 分钟" not in svg
        report = {
            "label_edit": {"changed_values": changed_ids, "edges_changed": False,
                           "export_seconds": round(graph_seconds, 2),
                           "validation": json.loads(graph_check.stdout)},
            "parameter_edit": {"changed_json_values": 3, "code_edits": 0,
                               "expected_overlap_minutes": 45,
                               "expected_end_label": "11:30",
                               "export_seconds": round(time_seconds, 2)},
            "scope": "temporary test edits only; accepted teaching examples remain 20/15 and 60/0/35",
            "artifacts": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in out.iterdir() if p.suffix in {".drawio", ".png", ".svg"}},
            "human_edit_time": "not measured; timings are machine export time only"
        }
        (HERE / "editing-probe.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()

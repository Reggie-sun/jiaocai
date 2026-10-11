"""Run existing numerical checks against the preserved data and revised source."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tables(text):
    return re.findall(r"(?:^\|[^\n]*\n)+", text, flags=re.M)


for n in range(1, 4):
    old = HERE / "snapshots" / f"ch0{n}-baseline.md"
    new = ROOT / "manuscripts/ch01-03-review" / f"ch0{n}.md"
    assert tables(old.read_text()) == tables(new.read_text()), f"Chapter {n} raw table changed"

file = ROOT / "materials/ch02-progressive/verify_exercises.py"
spec = importlib.util.spec_from_file_location("existing_ch02_checks", file)
module = importlib.util.module_from_spec(spec)
original_code = file.read_text()
deadline_check = 'return now <= e1["arrival_deadline_minute_of_day"]'
assert original_code.count(deadline_check) == 1
# The prose says before 10:05; retain that strict boundary in this task's check.
exec(compile(original_code.replace(deadline_check, 'return now < e1["arrival_deadline_minute_of_day"]'),
             str(file), "exec"), module.__dict__)
module.derive()
source2 = (ROOT / "manuscripts/ch01-03-review/ch02.md").read_text()
graph = module.D["new_worked_examples"]["route_edges"]
routes = {"→".join(path): cost for path, cost in module.paths(graph, "P", "D")}
case = source2.split("### 2.4.1", 1)[1].split("### 2.4.2", 1)[0]
listed = dict((route, int(cost)) for route, cost in re.findall(r"路线([PABCD→]+)需要[0-9+]+=([0-9]+)分钟", case))
module.check("PRO-01 all six routes exactly match actual prose", listed, routes)
module.check("PRO-01 six legal routes", len(routes), 6)
module.check("PRO-02 prose inclusive deadline", "J→L这段须不晚于10:00完成" in source2, True)
limit = next(e["completion_deadline_minute_of_day"] for e in module.D["e01"]["edges"] if e["from"] == "J")
module.check("PRO-02 exact 10:00 is within inclusive cutoff", 600 <= limit, True)
module.check("E01 exact 10:05 is outside the prose arrival cutoff", 605 < module.D["e01"]["arrival_deadline_minute_of_day"], False)
(HERE / "ch02/exercise-verification.json").write_text(json.dumps({"status": "PASS",
    "checks": module.CHECKS, "check_count": len(module.CHECKS),
    "source_sha256": sha(ROOT / "manuscripts/ch01-03-review/ch02.md"),
    "inherited_input": "materials/ch02-progressive/exercise-inputs.json",
    "input_sha256": sha(ROOT / "materials/ch02-progressive/exercise-inputs.json"),
    "data_binding": "All raw revised tables byte-identical to the accepted baseline; new route enumeration parsed from prose. Task-local arrival check follows the prose strict-before-10:05 rule, while J→L uses the inclusive 10:00 cutoff; original checker preserved.",
    "boundary": "Fixed toy data, not actual models or classroom evidence."}, ensure_ascii=False, indent=2) + "\n")

file = ROOT / "materials/ch03/verify_exercises.py"
source3_path = ROOT / "manuscripts/ch01-03-review/ch03.md"
source3 = source3_path.read_text()
code = file.read_text()
start = code.index("def read(name):")
end = code.index("\ndef table", start)
code = code[:start] + "def read(name):\n    return current_source\n\n" + code[end:]
code = code.replace("(ROOT / 'materials/ch03/exercise-verification.json')", "(ROOT / 'materials/ch01-03-review/ch03/exercise-verification.json')")
code = code.replace("{p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(MS.glob('*.md')) if p.name != 'ch03.md'}",
                    "{'manuscripts/ch01-03-review/ch03.md': current_sha}")
exec(compile(code, str(file), "exec"), {"__file__": str(file), "current_source": source3,
    "current_sha": sha(source3_path)})
print(f"PASS: Chapter 2 {len(module.CHECKS)} checks; Chapter 3 existing checks consume current combined manuscript")

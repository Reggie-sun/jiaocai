"""Render disjoint chapter deliveries with the existing artifact/check adapters."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PYTHON = "/home/reggie/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python"
RENDER = "/home/reggie/.codex/plugins/cache/openai-primary-runtime/documents/26.1009.11318/skills/documents/render_docx.py"
ADAPTER = ROOT / "materials/revision-implementation-20261012/delivery.py"


def deliver(n):
    here = ROOT / f"materials/ch{n:02d}-feedback"
    output = ROOT / f"output/ch{n:02d}-feedback/ch{n:02d}-feedback.docx"
    toc = here / "toc-pages.json"
    for iteration in range(1, 4):
        # Chapter eight already has two historical iterations.
        label = iteration + 2 if n == 8 else iteration
        pages = here / f"pages-r{label}"
        with (here / f"render-r{label}.log").open("w") as log:
            commands = [[PYTHON, str(ADAPTER), "build", str(n)]]
            if toc.exists():
                commands[0] += ["--toc", str(toc)]
            commands += [[PYTHON, RENDER, str(output), "--output_dir", str(pages), "--emit_pdf"],
                         [PYTHON, str(ADAPTER), "verify", str(n), "--pdf", str(pages / f"ch{n:02d}-feedback.pdf"), "--toc", str(toc)]]
            for command in commands:
                subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                               timeout=300, check=True)
        verification = json.loads((here / "layout-verification.json").read_text())
        if verification["toc_cache_matches_actual_pages"]:
            shutil.copyfile(pages / f"ch{n:02d}-feedback.pdf", output.with_suffix(".pdf"))
            result = {"chapter": n, "pages_dir": str(pages.relative_to(ROOT)),
                      "verification": str((here / "layout-verification.json").relative_to(ROOT)),
                      "status": "PASS", "pages": verification["pages"]}
            print(json.dumps(result), flush=True)
            return result
    raise RuntimeError(f"Chapter {n}: TOC pagination did not converge in three rounds")


def guarded(n):
    try:
        return deliver(n)
    except Exception as error:
        result = {"chapter": n, "status": "FAILED", "error": str(error)}
        print(json.dumps(result), flush=True)
        return result


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(guarded, map(int, sys.argv[1:])))
    (ROOT / "materials/revision-implementation-20261012/render-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    sys.exit(any(result["status"] != "PASS" for result in results))

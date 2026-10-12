"""Parent transcription of actual read-only reviewer messages, not new review."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
initial = {}
for name in ("snapshot.json", "snapshot-2456.json"):
    initial.update(json.loads((HERE / "content-r1" / name).read_text()))
final = {str(n): hashlib.sha256((ROOT / f"manuscripts/ch{n:02d}-feedback/ch{n:02d}.md").read_bytes()).hexdigest()
         for n in (2, 4, 5, 6, 7, 8, 9)}
common = {
    "sealed_by": "/root",
    "provenance": "Parent transcription of actual native read-only reviewer messages; reviewer profile prohibited writing report files.",
    "initial_full_read": initial,
    "initial_full_read_line_ranges": {"ch02": [1, 988], "ch04": [1, 814], "ch05": [1, 721], "ch06": [1, 812], "ch07": [1, 666], "ch08": [1, 772], "ch09": [1, 756]},
    "final_candidate_sha256": final,
    "review_method": "Full initial frozen text, then actual targeted semantic rereads. No claim that all final bytes were reread in full.",
    "limits": ["AI content review only; no actual teacher/student/classroom acceptance", "No Word-native field update, physical printing or publisher approval", "No full brand-login/mobile/network availability test"],
}
professional = {
    **common, "reviewer": "/root/content_professional", "profile": "reviewer_high",
    "scope": "Professional mechanisms, primary-source scope, case identity, calculations and exercise/data consistency for seven full chapters; outline and necessary chapter6/10 dependency excerpts.",
    "findings": [
        {"id": "P789-01", "chapter": 7, "problem": "Zero-byte reproduction file described as two-line input", "resolution": "Changed to zero-byte empty file; actually targeted reread and closed"},
        {"id": "P2456-001", "chapter": 4, "problem": "Four section training tasks lacked stable identifiers and corresponding answers", "resolution": "E07–E10 and answers added; final targeted ranges 118–145,281–311,458–487,607–638,788–849; final two supplements reread814–832; closed"},
    ],
    "additional_closures": {"ch08": "Actually reread320–338 after SiYuan pricing clarification; no new finding", "ch09": "Actually checked clarified second example and separate single-weight sensitivity/priority reset; calculations correct", "ch05": "Final reread562–605,668–713; generic hint and answers consistent", "ch02": "Independently reproduced 28-reference bijection; citation identities identical and body identical after reverse mapping"},
    "numeric_evidence": {"ch04": {"12_to_8_absolute_minutes": 4, "relative_reduction": "33.33%"}, "ch06": {"prototype_actually_executed": True, "kwh": [38.88, 51.84, 8.64], "total_kwh": 99.36, "cost_yuan": 61.60, "emergency_light_excluded": True}, "ch09": {"x3": [21, 17], "x7": [29, 29], "priority_reset": [13, 17, 12]}, "ch07_ch08": "Actual task-data and budget CSV checks; source boundaries distinguish simulated data from reported results"},
    "page_qa": {"ch02": {"actually_viewed_pages": list(range(1,87)), "manifest_sha256": "d93b909878b9edaf69c21201dfb2cd51dd4e4e3a039831213659a4fe7c772dd1"}, "ch06": {"actually_viewed_pages": list(range(1,73)), "manifest_sha256": "00487f6622ffb9c46dc292e09862811675b1bad33d5b58bdc11b06b448a3fb3f"}},
    "final_new_findings": [], "blocking_findings_remaining": [],
}
teaching = {
    **common, "reviewer": "/root/content_teaching", "profile": "reviewer_high",
    "scope": "Teaching entry, difficulty progression, independent section cases, prerequisite explanation, practice/answer boundaries and reflection for seven full chapters; actual quality Skill, original outline/sample and needed continuity excerpts.",
    "findings": [
        {"id": "T789-001", "chapter": 7, "problem": "Empty-file material and two-line reproduction description inconsistent", "resolution": "Empty-file wording corrected and actually targeted reread; closed"},
        {"id": "T789-002", "chapter": 9, "problem": "Website exhibition example ambiguously described as repeating rainwater case", "resolution": "Explicit second example and shared method; actually reread; closed"},
        {"id": "T789-003", "chapter": 9, "problem": "Single-weight sensitivity conflated with large multi-weight priority reset", "resolution": "Separate x example from reset; actual numerical checks and reread; closed"},
        {"id": "T2456-001", "chapter": 5, "problem": "E07 immediate hint disclosed concrete A/B/C decisions", "resolution": "Generic mechanism clue only, specific decisions in answers; actually reread571–593,673–691; closed"},
        {"id": "T2456-002", "chapter": 4, "problem": "E07 answer lacked operational definitions requested by base task", "resolution": "Service population/category/completion criteria and all-human-minutes measure added; final reread124–140,812–832; closed"},
        {"id": "T2456-003", "chapter": 4, "problem": "E08 answer lacked observable stop-condition example", "resolution": "Indicators and proposed pause conditions added with design/verification boundary; final reread290–310,812–832; closed"},
    ],
    "additional_closures": {"ch07": "Actual113–127 reread", "ch09": "Actual28–44,89–113,361–390 and table9-4 reread/calculations", "ch08": "Actual320–338 SiYuan wording reread, no new teaching finding", "ch02": "No new teaching targeted reread after citation numbering; initial full read inherited only through professional independently reproduced semantic-equivalence proof", "ch03": "Actual before/after1–30 comparison; only school-dependent phrase at22 changed, no new full chapter review claimed"},
    "page_qa": {"ch04": {"actually_viewed_pages": list(range(1,75)), "manifest_sha256": "4a0d49effc84fc7ea5be498b4ce35e1a2cdfc01796d75db346437bb3f8f92c4b"}, "ch05": {"actually_viewed_pages": list(range(1,73)), "manifest_sha256": "05d779e57a47dd27756ed5fa02c94e02178de68aed7b451d12b9301992cb00b4"}},
    "final_new_findings": [], "blocking_findings_remaining": [],
}
for name, record in (("professional", professional), ("teaching", teaching)):
    (HERE / f"content-{name}-report.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"sealed_initial_chapters": len(initial), "final_chapters": len(final), "blocking_findings_remaining": []}))

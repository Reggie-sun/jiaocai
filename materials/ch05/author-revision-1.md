# Chapter 5 Revision 1 Record

Review basis: two complete initial readers reviewed the manuscript snapshot with SHA-256 `1f8935f28291b11ef3b1b91415884c348bcd8fd77c915619be58acbf24eaa3d7`. The following targeted corrections were applied to that snapshot and synchronized across section components, `manuscripts/ch05/ch05.md`, and applicable exercise/source files.

## Findings and corrections

- **C5-P01 — citation mismatch; `manuscripts/ch05/s5-1.md`, 5.1.3 and 5.1.5.** The gecko adhesion study now cites `[2]` (Autumn et al. 2002); the Kano quality-model discussion cites `[3]`. The chapter's first-use order, full numbered references, source-map entries, and matching bare URLs were checked.
- **C5-P02 — inaccurate functional reversal; `manuscripts/ch05/s5-1.md`, 5.1.4.** Replaced the refrigerator example, which described a control adjustment rather than reversing the function, with a concept-level contrast between cooling and heating/maintaining warmth. The revised text explicitly says an ordinary refrigerator is not presumed to heat, identifies extra hardware and safety requirements, and proposes simulation/risk analysis before any controlled prototype test.
- **C5-P03 / T01 — E01 condition misapplied; `manuscripts/ch05/s5-1.md`, E01; `manuscripts/ch05/closing.md`, E01 answer; `materials/ch05/exercise-data.json`.** The hard condition is now represented as “without mouse for key tasks.” The voice interface is not rejected for lacking keyboard input: it is excluded under the stated criteria because it asks for an unrelated booking reason. Voice usability remains an untested question. The data JSON and answer rationale match the task wording.
- **C5-T02 — E02 example conflicted with free-choice task; `manuscripts/ch05/s5-2.md`, 5.2.6; `manuscripts/ch05/closing.md`, E02 answer.** Card A is explicitly a worked demonstration. Independent E02 responses are limited to cards B–D; the chapter-end answers provide a concrete evidence plan for each of B, C, and D.
- **C5-T03 — E02 evidence did not distinguish stale display from a later booking; `manuscripts/ch05/s5-2.md`, card-A demonstration; `manuscripts/ch05/closing.md`, E02 answer alignment.** The demonstration now compares the same resource ID, authoritative status history, page version/render time/displayed state, and request/transaction timestamps. It distinguishes a status change after rendering from a page/authority mismatch, does not claim that mismatch proves a cache defect, and retains “unknown” when reliable records are unavailable. The independent answer key remains focused on B–D as required by T02.
- **C5-P04 — transfer-learning scope too broad; `manuscripts/ch05/s5-7.md`, 5.7.3 and Table 5-8; `manuscripts/ch05/closing.md`, key term.** The definition now concerns source-task learned parameters, representations, or patterns. It explicitly distinguishes copying a script and training from random initialization (code/process reuse) from reusing learned parameters or representations and adapting them to a target task.

## Verification

`python materials/ch05/verify_exercises.py` passed after synchronizing the component files and complete chapter. It uses `Decimal` to recompute both weighted matrices and compares them with the Markdown tables and answer totals; checks E01–E08 and answer coverage; checks table, figure, and reference numbering; verifies first-use citation order `[1]`–`[14]`; and compares bibliography URLs between the chapter and source register.

- Worked-example matrix (Table 5-2): A 4.30, B 2.55, C 4.35, D 3.45.
- Independent E01 matrix (Table 5-3): A 3.80, B 2.35, C 3.75, D 2.80.
- Final chapter SHA-256: `6e0578d7ddae3d2021400cabe985f3bc6782de396ba565ad472cfe570a0a4061`.
- Han-character count excluding URLs and code: `32,747`.

This record documents author corrections and executable content checks; it is not a replacement for reader re-review or final parent acceptance.

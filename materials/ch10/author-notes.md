# Chapter 10 Author Notes

## Draft and Scope

Chapter: **第十章 领导力初探与未来展望**. The manuscript preserves the three section titles required by `specs/ch10.spec.md`. The merged manuscript contains 35,490 Han characters after the focused verifier removes fenced code, inline code, and URLs. Its SHA-256 is `da69285fdc210a4dad59b23beeb83da05a40ad8e481acaebf0e3e40bbf94954c`.

This is a complete chapter draft. A structural/numeric PASS does not establish source acceptance, teaching effectiveness, figure quality, classroom use, or publisher readiness. The independent professional and teaching reviews produced targeted corrections recorded below; the parent owns final review and acceptance.

## Targeted Review Corrections

- PR-1001: E02's T4 branch now keeps the three-hour task within 小叶's remaining capacity (her total becomes 4/4 hours) and assigns the required one-hour skill-2 review to 小陈, whose total becomes 10/9 hours. The exercise verifier recalculates the pre-T4 loads `[8, 1, 9]`, post-T4/review loads `[8, 4, 10]`, and the respective fit/over-capacity results; exhaustive assignment search still finds no full-scope plan.
- PR-1002: the prose and glossary define psychological safety as a team-shared belief. The source record distinguishes this construct from one person's experience and labels using individual experience as a clue as instructional interpretation; the study remains bounded to 51 teams in one manufacturing company and an association rather than a causal guarantee.
- TR-1001: E03's answer now gives a proposed responsibility, check question, and pause condition for each of GOVERN, MAP, MEASURE, and MANAGE. The roles are discussion proposals for the synthetic classroom case, not appointments or approvals; checks are plans, not completed tests or measurements.
- TR-1002: E02's evaluation criterion now asks students to determine feasibility from skills, individual capacity, and added review time, leaving the chapter-end infeasibility derivation as the worked explanation.
- TR-1003: the recurring example and base matrix both give 小叶 seven project hours. The distinct exam-week exercise still sets her capacity to four hours; six-hour mentions remain estimates for the T2 work package, not a second capacity figure.

The recurring “地方记忆数字展” is an author-created classroom simulation. Names, stories, estimates, activities, stakeholder reactions, team assignments, and AI outputs are fictional. The manuscript reports no real interviews, real locations, field measurements, external model run, deployment, permission, or institutional outcome. It keeps public release, real data, and external AI service use outside the stated classroom authorization.

## Continuity and Teaching Boundary

Chapter 6's actual project is an offline teaching prototype for classroom electricity estimates in a shared learning space. Its author notes and project README bound it to synthetic inputs, local computation, and human review; it does not control equipment or report a real campus deployment. Chapter 10 uses a distinct fictional exhibit scenario and does not carry forward Chapter 6 project facts or outcomes. The E04 archive may draw on a student's own authorized Chapter 6 artifacts as optional evidence, but must preserve their original scope and distinguish a simulation from field evidence.

Chapter 9 contributes collaboration context. Chapter 10 focuses on leadership judgment, allocation, responsibility, and development rather than restating the prior chapter's coordination procedures. The chapter's task estimates, matrices, and portfolio rubric are original teaching structures, not published scales or empirical findings.

## Source Support Record

The complete item-by-item source record, consulted URLs, read scope, claim mapping, and non-supported extrapolations are in [author-sources.md](author-sources.md). Key limits:

- NRC Chapter 6 is titled “Team Science Leadership.” Only selected skim excerpts for printed pages 126 and 129–134 were read; the official contents page was checked for the chapter title and page span 125–148. The notes do not claim that the full chapter was read. Chapter-specific leadership functions and the reported limits of leadership measurement are distinguished from the author's instructional inference.
- Edmondson (1999) was checked through the publisher page and abstract, not the access-restricted full text. The abstract defines psychological safety as a team-shared belief about interpersonal risk-taking. The manuscript keeps the reported association bounded to 51 teams in one manufacturing company and makes no universal or causal guarantee; it labels the individual-experience-as-clue distinction as instructional interpretation, not an article-tested diagnostic rule.
- The ACM reference is the 2018 booklet object; its DOI/ISBN are not transferred to the separate live-code PDF or other ACM documents. The consulted sections and limits are recorded in the source matrix.
- NIST AI RMF 1.0 supports the named high-level functions and framework caveats. It does not certify the fictional project, prescribe this chapter's worksheet, or guarantee safety or compliance.

## Verification Snapshot

`python materials/ch10/verify_exercises.py` completed with PASS. The report is [author-exercise-verification.json](author-exercise-verification.json), SHA-256 `f9dcff0953b09afccefe2ba09515c1c67a20aa40fac44ecedf941644521f20a3`. It confirms:

- opening, three section files, and closing exactly match `ch10.md`;
- the exact three section titles, chapter closing order, E01–E04 prompts and detailed answers are present;
- all 13 numbered tables are rectangular, four figure markers are sequential and captioned, and four references are cited in order;
- E02 worked assignments include named one-hour reviews for every skill-1 task owner, count each review against the reviewer’s capacity, and match the worked arithmetic; an explicit T4 branch independently recomputes pre-task loads `[8, 1, 9]` and post-task/review loads `[8, 4, 10]`, confirming that 小叶 fits her 4-hour limit while 小陈's required review exceeds his 9-hour limit;
- exhaustive enumeration finds no full-scope E02 assignment under the reduced capacity and review rule; the independent T2a plan meets the stated minimum acceptance criteria and computes to 20 hours;
- the base-case capacity for 小叶 is seven hours and the exam-week variant is four; E02's independent feasibility criterion does not disclose the worked conclusion;
- the psychological-safety definition states the team-shared belief; the individual's experience is identified only as a clue, not a substitute for the team-level construct;
- E03 simulation assumptions match the exercise data, and its answer has all four proposed risk-record functions with a responsible role, check question, and pause condition;
- the E04 six-dimension, 24-point classroom rubric matches the exercise data.

This verification does not review teaching quality, source truth beyond the separately documented source pass, rendered images, or human acceptance. Figures have author plans and manuscript anchors; the parent owns their rendered assets and visual review.

## Input Snapshot Hashes

The following are the consulted local inputs at the time this draft was assembled:

| Input | SHA-256 |
|---|---|
| `AGENTS.md` | `1b859b79d8984157253df55df697679ba7fa28799299b3b443b8b516a01e67ae` |
| `skills/textbook-authoring/SKILL.md` | `bc08bde674c2dba84c100f9dd0c2e7448b1fd961c1c44fc2986456269a2ec5da` |
| `specs/authoring-quality.spec.md` | `7c5c2e24ffb99f6d9e3013c7bcc3e7dc1f4b7d04e9f6af078f6f7057a05c7a14` |
| `specs/ch10.spec.md` | `b38ce69d3c2abf74fc63fcb04b48efeb46c081aa497a1c843cc0e5b06f0f1741` |
| `plans/ch10.plan.md` | `b47e7238cca79f6715d7a7a4a35a094166e2329f700a1d975c34363bc581d63d` |
| `materials/ch07-10/outline-actual.txt` | `364ad7409c1658142bc4b0693426b39bf934897d9baaa5323ea2ff380363ed84` |
| `materials/ch07-10/sample-actual.txt` | `4527f0025d39e224354378a13feaa1f2c923f355dff74c681a7abcbd18ba77fd` |
| `manuscripts/ch06/ch06.md` | `900bb39564d336ee0c58089f110720813225a42d4a033a61794a46c5f8995b77` |
| `materials/ch06/author-sources.md` | `f1a3f2536d2714037c1c973e004913f6fddcac6fab377530478f6ad48f4ea010` |
| `materials/ch06/project/README.md` | `e730258db62a5e1ce9325968e86c0a948ed67c0228c5fd5541c8f24ee3debf81` |

## Current Chapter Artifacts

| Artifact | SHA-256 |
|---|---|
| `manuscripts/ch10/ch10.md` | `da69285fdc210a4dad59b23beeb83da05a40ad8e481acaebf0e3e40bbf94954c` |
| `materials/ch10/author-sources.md` | `067d58a0a70efee060ca3d825a56081f55418f80ee6400dcfa0973ae97189112` |
| `materials/ch10/author-figures.md` | `6f2039822d4eb6aabfae47bb959d4244ef14d8c023cf99764fac15dc70e0a2c5` |
| `materials/ch10/exercise-data.json` | `634aedb9ea171e04356260f0c0ea9fdda78caa01940cc2bb0c560e1e7fa2fee2` |
| `materials/ch10/verify_exercises.py` | `7279b924e687b05261eafd63ec6384cc78398bb574c8a1400f5252a526cb592d` |
| `materials/ch10/author-exercise-verification.json` | `f9dcff0953b09afccefe2ba09515c1c67a20aa40fac44ecedf941644521f20a3` |

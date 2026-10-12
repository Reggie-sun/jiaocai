# Chapter 2 Revision Record

## Scope and Baseline

This author-owned deliverable changes only `manuscripts/ch02-feedback/ch02.md` and the author materials in `materials/ch02-feedback/`. It implements the Chapter 2 M1/M2 revision scope against the latest timeline version, `manuscripts/ch01-03-review/ch02.md`, whose pre-edit SHA-256 was `00d10d3d24ef040c9639d241991996fed49a33fe0d61f5399fc4f665733d1eb2`. The new manuscript began as a byte-for-byte copy of that baseline. The original three source manuscripts and all other worktree paths remain outside this author scope.

All three versions were read in full. The first and latest files were read in successive line ranges to avoid truncation; the 934-line progressive version was checked against the 934-line latest version with a complete diff. Their shared text was reviewed as the latest version; four differing hunks were inspected individually. The extracted original outline and `sample-actual.txt` were also read. Baseline hashes, counts, and section-by-section decisions are recorded in [`comparison-and-decisions.md`](comparison-and-decisions.md).

## Changes Made

- Kept the exact five outline titles and order, and gave every second-level section a lead-in followed by a first-subsection case with explicit description and analysis.
- Added source-bounded examples for CNN steering from camera pixels, GPT-class scientific-paper summarization, transmission-tower HRL, medical saliency-map limits, cross-hospital COVID prediction, Transformer electrical-load forecasting, dynamic programming versus GNN shortest paths, job-shop heuristics versus deep RL, state machines versus AlphaGo/MCTS, and bank credit-scoring federated learning.
- Preserved the beginner hand calculations and added explicit distinctions where the outline's shorthand could overstate the evidence: a saliency map is not causal or diagnostic evidence; local federated data does not guarantee privacy; MAML does not generally select every optimizer or hyperparameter; and study results do not establish universal superiority or deployment readiness.
- Kept the original guide as the integrated chapter-end task. E01–E06 prompts, answers, numerical tables, route results, and all eight figure links are byte-identical to the latest source manuscript. No new figure was created.
- Added source notes with direct primary-source links, exact claim scope, and limitations; appended references [19]–[28] to the chapter.

## Verification

Focused content smoke checks were run before and after implementation. The baseline passed with the exact five titles, E01–E06, eight resolving figure links, and 37,035 Han characters. The final check passed with:

- exact five outline titles, lead-ins, and case description/analysis in sections 2.1–2.5;
- E01–E06 exercise and answer spans, E06 graph data, and the reference-answer block unchanged from the latest baseline;
- the same eight figure links, all resolving relative to the manuscript, with no added figures;
- every reference [1]–[28] present in the bibliography and cited in the manuscript;
- 39,225 Han characters, counted after removing fenced code, inline backtick code, and URL strings and counting `U+3400–U+9FFF`;
- no school-specific terms such as `西南财经大学`, `西财`, or `[学校名称]`.

Final manuscript SHA-256: `d9b2b2553e54ee11e79f83d89b14d8ba0cd6a23acf1db4543b6018496129e499`.

This is an author draft for Parent review. Word/PDF generation, Harness checks, independent review, and acceptance remain with the Parent as assigned; none are claimed here.

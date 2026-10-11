# Teaching Review

## Snapshot

Native `/root/teaching_review`, independent read-only session. Entire manuscript lines 1–774, all five sections, E01–E06 and all solutions, Spec, figure plan, exercise data and project README actually read. Before/after SHA256: `df09374a957dd1054cbade3afeac5b14f34249ff844a91ebef94b52007dc2be6`. Electricity, money and changed conditions independently recalculated. Prototype execution, actual pictures, Word/PDF, real illumination and human learning outcomes were outside scope.

## Finding

C6-T01, blocking_candidate, line 184: data dictionary requires candidate hours “0至24之间；不得大于基线”, while lines 334/433 and E04 X (8→9 hours), solution −6.48 kWh and `SCENARIO_INCREASE` explicitly accept an increase. A student implementing the dictionary would reject the exercise's valid case. Change the dictionary to allow 0–24 hours, show increased consumption explicitly, and prohibit describing it as saving. Values above 24 and unknown protection must remain held.

## Parent Adjudication

Confirmed against manuscript, exercise JSON and executable prototype. Original writer is assigned dictionary correction and component synchronization. The tested program already permits the scenario correctly; the correction must preserve its behavior. Original reader targeted rereview is required.

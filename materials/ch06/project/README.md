# Offline Teaching Prototype

This small Python program demonstrates the chapter's arithmetic and review boundary. It reads a local JSON file and prints candidate electricity estimates for teaching scenarios. All values in `inputs.json` are author-created examples. The price of 0.62 CNY/kWh is a teaching assumption, not a campus tariff.

The program does not use network access, install packages, read campus systems, collect personal information, control lamps, or execute recommendations. A result marked `READY_FOR_HUMAN_REVIEW` is only a candidate scenario calculation. A protected or unknown emergency-lighting state, missing data, invalid value, or conflicting identifier cannot yield a definite adjustment recommendation.

## Run

Use Python 3.10 or later. From this directory:

```sh
python3 prototype.py inputs.json
```

The result is also available as a report in `expected-output.txt` for comparison. The program does not write to the input file.

## Verify

Run the prototype tests with the Python standard library:

```sh
python3 -m unittest -v
```

From the project root, the chapter exercise checker is:

```sh
python3 materials/ch06/verify_exercises.py
```

It independently recalculates the worked and exercise examples from `materials/ch06/exercise-data.json`, tests missing/conflicting/unknown cases and changes in days and teaching price, then writes `materials/ch06/author-exercise-verification.json`.

## Input Fields

The top-level fields are `period_days`, `teaching_price_cny_per_kwh`, `teaching_price_note`, and `zones`. Each zone has `id`, `name`, `lamp_count`, `watts_per_lamp`, `baseline_hours_per_day`, `candidate_hours_per_day`, `emergency_lighting_status`, and `source_note`. The emergency status must be `confirmed_yes`, `confirmed_no`, or `unknown`; missing or unknown status does not mean “confirmed no.” `lamp_count` and `period_days` must be JSON integers; the price, wattage, and hour fields must be JSON numbers. Quoted numeric strings and booleans are rejected rather than coerced. The report retains the original zone inputs and prints lamp count, wattage, both hour values, protection status, units, and `source_note` for ready and held zones.

The model uses:

`baseline kWh - candidate kWh = lamp count × watts per lamp ÷ 1000 × (baseline hours - candidate hours) × days`

The signed electricity difference is then multiplied by the teaching price to show an illustrative money difference. The report prints the teaching price at its full supplied decimal precision and displays energy quantities rounded to 0.001 kWh. Monetary amounts are calculated from unrounded energy values and the full input price, then rounded to cents. Because displayed energy is rounded, multiplying the displayed energy by the displayed price may differ from the reported amount by a cent. Reproduce an exact amount from the original inputs and formula, not from the rounded energy display. The calculation assumes constant rated power across the chosen hours and period. It excludes measured load, tariffs, installation and maintenance costs, safety evaluation, actual usage, and user research. It is a classroom simulation, not an implementation, field study, financial recommendation, or compliance assessment.

If code is unavailable, students can use the same input fields, formula, calculator, and state checklist on paper. They should show all units and keep protected, missing, or conflicting cases out of the definite recommendation set.

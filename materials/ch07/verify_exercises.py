#!/usr/bin/env python3
"""Check the arithmetic used by Chapter 7's numeric exercises."""

from decimal import Decimal
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "exercise-data.json"
OUTPUT_PATH = HERE / "author-exercise-verification.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def one_decimal(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.1")))


def median(values: list[int]) -> Decimal:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return Decimal(ordered[middle])
    return (Decimal(ordered[middle - 1]) + Decimal(ordered[middle])) / 2


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    self_ratings = data["exercises"]["E05"]
    scores = self_ratings["scores"]
    require(len(scores) == 6, "E05 must contain the six anonymous teaching-example rows")
    require(
        all(0 <= row["start"] <= 10 and 0 <= row["end"] <= 10 for row in scores),
        "E05 scores must stay within the teaching scale 0–10",
    )

    start_total = sum(row["start"] for row in scores)
    end_total = sum(row["end"] for row in scores)
    changes = [row["end"] - row["start"] for row in scores]
    start_mean = Decimal(start_total) / len(scores)
    end_mean = Decimal(end_total) / len(scores)
    mean_change = Decimal(sum(changes)) / len(changes)
    direction_counts = {
        "increased": sum(change > 0 for change in changes),
        "decreased": sum(change < 0 for change in changes),
        "unchanged": sum(change == 0 for change in changes),
    }
    expected_ratings = self_ratings["expected"]
    require(start_total == expected_ratings["start_total"], "E05 start total mismatch")
    require(end_total == expected_ratings["end_total"], "E05 end total mismatch")
    require(one_decimal(start_mean) == expected_ratings["start_mean"], "E05 start mean mismatch")
    require(one_decimal(end_mean) == expected_ratings["end_mean"], "E05 end mean mismatch")
    require(one_decimal(mean_change) == expected_ratings["mean_change"], "E05 mean change mismatch")
    require(changes == expected_ratings["individual_changes"], "E05 individual changes mismatch")
    require(direction_counts == expected_ratings["direction_counts"], "E05 direction counts mismatch")
    require(sum(changes) == end_total - start_total, "E05 change-of-means cross-check failed")

    planning = data["exercises"]["E07"]
    durations = planning["historical_actual_days"]
    require(len(durations) == 4 and all(day > 0 for day in durations), "E07 requires four positive historical durations")
    historical_mean = Decimal(sum(durations)) / len(durations)
    historical_median = median(durations)
    planned = Decimal(planning["planned_days"])
    expected_planning = planning["expected"]
    require(one_decimal(historical_mean) == expected_planning["historical_mean_days"], "E07 historical mean mismatch")
    require(one_decimal(historical_median) == expected_planning["historical_median_days"], "E07 historical median mismatch")
    require((planned < historical_mean) == expected_planning["plan_below_mean"], "E07 mean comparison mismatch")
    require((planned < historical_median) == expected_planning["plan_below_median"], "E07 median comparison mismatch")

    report = {
        "status": "PASS",
        "checks": {
            "E05": {
                "start_total": start_total,
                "end_total": end_total,
                "start_mean": one_decimal(start_mean),
                "end_mean": one_decimal(end_mean),
                "mean_change": one_decimal(mean_change),
                "individual_changes": changes,
                "direction_counts": direction_counts,
                "cross_check_mean_change_equals_difference_of_means": True,
            },
            "E07": {
                "historical_actual_days": durations,
                "historical_mean_days": one_decimal(historical_mean),
                "historical_median_days": one_decimal(historical_median),
                "planned_days": planning["planned_days"],
                "plan_below_both_historical_summaries": True,
            },
        },
        "scope": "Arithmetic only; does not validate causal, psychological, or project-quality claims.",
    }
    OUTPUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

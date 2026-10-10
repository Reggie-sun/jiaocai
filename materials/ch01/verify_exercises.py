"""复算第一章教学数据；输出证据，不修改材料或Harness状态。"""

import copy
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def enumerate_solutions(resources, requests, resource_key, compatible):
    choices = [
        [(r[resource_key], s) for r in resources for s in r["available_slots"]
         if s in q["allowed_slots"] and compatible(r, q)]
        for q in requests
    ]
    return [
        [{"request_id": q["request_id"], resource_key: r, "slot_id": s}
         for q, (r, s) in zip(requests, picked)]
        for picked in itertools.product(*choices)
        if len(set(picked)) == len(picked)
    ], choices


def check_reference(resources, requests, reference, resource_key, compatible):
    resource_by_id = {r[resource_key]: r for r in resources}
    request_by_id = {q["request_id"]: q for q in requests}
    assert len(reference) == len(requests)
    assert {row["request_id"] for row in reference} == set(request_by_id)
    occupied = set()
    for row in reference:
        q = request_by_id[row["request_id"]]
        r = resource_by_id[row[resource_key]]
        assert row["slot_id"] in r["available_slots"]
        assert row["slot_id"] in q["allowed_slots"]
        assert compatible(r, q)
        key = (row[resource_key], row["slot_id"])
        assert key not in occupied
        occupied.add(key)


def main():
    d = read("e01-devices.json")["devices"]
    q = read("e01-requests.json")["requests"]
    fit = lambda r, t: t["required_capability"] in r["capabilities"]
    solutions, choices = enumerate_solutions(d, q, "device_id", fit)
    assert len(solutions) == 12
    reference = read("e01-reference.json")["reference"]
    check_reference(d, q, reference, "device_id", fit)
    closed = copy.deepcopy(d)
    closed[1]["available_slots"] = []
    closed_solutions, _ = enumerate_solutions(closed, q, "device_id", fit)
    assert not closed_solutions
    # 反例：逐行功能/开放/允许时段都正确，仍因同一位置重复而非法。
    invalid = copy.deepcopy(reference)
    invalid[3] = {"request_id": "R4", "device_id": "D1", "slot_id": "S2"}
    try:
        check_reference(d, q, invalid, "device_id", fit)
    except AssertionError:
        duplicate_rejected = True
    else:
        raise AssertionError("未识别资源重复占用")

    rooms = read("e03-rooms.json")["rooms"]
    requests = read("e03-requests.json")["requests"]
    assert len(rooms) <= 2 and len(requests) <= 4
    assert all(type(r["capacity"]) is int and r["capacity"] > 0 for r in rooms)
    assert all(type(t["participants"]) is int and t["participants"] > 0
               and t["duration_slots"] == 1 for t in requests)
    room_fit = lambda r, t: (t["participants"] <= r["capacity"]
                             and set(t["required_facilities"]) <= set(r["facilities"]))
    room_solutions, room_choices = enumerate_solutions(rooms, requests, "room_id", room_fit)
    assert len(room_solutions) == 2
    check_reference(rooms, requests, read("e03-guidance.json")["reference"], "room_id", room_fit)
    reduced = copy.deepcopy(rooms)
    reduced[1]["capacity"] = 18
    reduced_solutions, reduced_choices = enumerate_solutions(reduced, requests, "room_id", room_fit)
    assert not reduced_solutions and reduced_choices[2] == []
    assert not room_fit(rooms[0], requests[2])  # 时间正确仍不能容纳Q3。
    assert not room_fit(rooms[0], requests[3])  # 设施也不能由容量替代。

    data = read("e05-data.json")
    staff_fit = lambda r, t: (t["required_qualification"] in r["qualifications"]
                              and t["participants"] <= r["capacity"]
                              and t["duration_slots"] == 1)
    staff_solutions, staff_choices = enumerate_solutions(data["resources"], data["requests"], "resource_id", staff_fit)
    assert len(staff_solutions) == 6
    check_reference(data["resources"], data["requests"], read("e05-guidance.json")["reference"], "resource_id", staff_fit)
    unqualified = copy.deepcopy(data["resources"])
    unqualified[1]["qualifications"] = ["general"]
    unqualified_solutions, unqualified_choices = enumerate_solutions(unqualified, data["requests"], "resource_id", staff_fit)
    assert not unqualified_solutions and unqualified_choices[2] == []

    brief = read("e04-brief.json")
    estimate = lambda r: r["lamps"] * r["watts_per_lamp"] * r["hours_per_day"] * r["days_per_month"] / 1000
    energies = {"baseline": estimate(brief["baseline"])}
    energies.update({r["id"]: estimate(r) for r in brief["candidates"]})
    assert energies == {"baseline": 14.4, "A": 21.6, "B": 14.4}
    assert all(r["one_time_cost_yuan"] <= 4000 for r in brief["candidates"])
    assert [r["hesitations"] / r["passers"] for r in brief["observations"][:2]] == [0.2, 0.15]
    return {
        "method": "finite_cartesian_enumeration_and_independent_reference_checks",
        "e01": {"baseline_count": len(solutions), "D2_closed_count": 0,
                "choices": choices, "reference_checked": True, "duplicate_rejected": duplicate_rejected},
        "e03": {"baseline_count": len(room_solutions), "C2_capacity18_count": 0,
                "choices": room_choices, "Q3_variant_choices": reduced_choices[2], "reference_checked": True},
        "e04": {"energy_kwh": energies, "stair_hesitation_rates": [0.2, 0.15],
                "boundary": "模拟算术核验；不证明照明改善或因果效应"},
        "e05": {"baseline_count": len(staff_solutions), "V2_without_screen_reader_count": 0,
                "choices": staff_choices, "P3_variant_choices": unqualified_choices[2], "reference_checked": True},
        "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(ROOT.glob("e[0-9][0-9]-*.json"))},
        "verification_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))

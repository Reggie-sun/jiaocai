"""Recompute the printed pilot examples; no subjective quality assessment."""
import itertools
import json
from pathlib import Path


def assignments(domains):
    return [items for items in itertools.product(*domains.values())
            if len(set(items)) == len(items)]


def verify():
    root = Path(__file__).resolve().parents[2]
    data = json.loads(Path(__file__).with_name("examples.json").read_text())
    e01 = root / "materials/ch01"
    devices = json.loads((e01 / "e01-devices.json").read_text())
    requests = json.loads((e01 / "e01-requests.json").read_text())
    # Field ownership stays with the original exercise inputs.
    devices = devices["devices"]
    requests = requests["requests"]
    positions = {tuple(v): k for k, v in data["positions"].items()}
    actual = {}
    for request in requests:
        actual[request["request_id"]] = sorted(
            positions[(device["device_id"], slot)]
            for device in devices
            if request["required_capability"] in device["capabilities"]
            for slot in device["available_slots"]
            if slot in request["allowed_slots"])
    assert actual == data["domains"], (actual, data["domains"])
    count = len(assignments(actual))
    assert count == 12
    closed = {k: [x for x in v if data["positions"][x][0] != "D2"]
              for k, v in actual.items()}
    assert len(assignments(closed)) == 0
    assert "a" in actual["R2"] and actual["R1"] == ["a"]
    failed_branch = dict(actual, R2=["a"])
    assert len(assignments(failed_branch)) == 0
    repaired = {"R1": "a", "R2": "b", "R3": "c", "R4": "d"}
    assert all(v in actual[k] for k, v in repaired.items())
    assert len(set(repaired.values())) == len(repaired)
    bottleneck = data["bottleneck"]
    union = set().union(*map(set, bottleneck["domains"].values()))
    assert len(bottleneck["resources"]) == len(bottleneck["domains"]) == 3
    assert len(union) == 2 and len(assignments(bottleneck["domains"])) == 0
    old = data["old_transfer_assignment"]
    assert {r for r, _, _ in old} == set(actual)
    assert len({(d, s) for _, d, s in old}) == len(old)
    assert all(positions[(d, s)] in actual[r] for r, d, s in old)
    rooms = json.loads((e01 / "e03-rooms.json").read_text())["rooms"]
    activities = json.loads((e01 / "e03-requests.json").read_text())["requests"]
    q3 = next(x for x in activities if x["request_id"] == "Q3")
    c1 = next(x for x in rooms if x["room_id"] == "C1")
    assert q3["participants"] == 20 and c1["capacity"] == 12
    room_domains = {
        r["request_id"]: [(room["room_id"], slot)
                          for room in rooms
                          if r["participants"] <= room["capacity"]
                          and set(r["required_facilities"]) <= set(room["facilities"])
                          for slot in room["available_slots"]
                          if slot in r["allowed_slots"]]
        for r in activities}
    room_solutions = [dict(zip(room_domains, x)) for x in assignments(room_domains)]
    assert len(room_solutions) == 2
    assert all(x["Q1"] == ("C1", "S1") and x["Q2"] == ("C1", "S2")
               and {x["Q3"], x["Q4"]} == {("C2", "S2"), ("C2", "S3")}
               for x in room_solutions)
    interval_results = {}
    for name, case in data["interval_cases"].items():
        a, b = case["A"], case["B"]
        overlaps = a[0] < b[1] and b[0] < a[1]
        a_slots, b_slots = set(range(*a)), set(range(*b))
        assert overlaps == bool(a_slots & b_slots)
        assert a[0] != b[0]  # Old start-only check would pass both.
        interval_results[name] = {"overlap": overlaps,
                                  "shared_hours": sorted(a_slots & b_slots)}
    assert interval_results["overlap"]["overlap"] is True
    assert interval_results["touching"]["overlap"] is False
    impulse = data["impulse"]
    result = impulse["input_lbf_s"] * impulse["approximate_factor"]
    assert abs(result - impulse["expected_N_s"]) < 1e-10
    return {"e01_count": count, "D2_closed_count": 0,
            "bottleneck_count": 0, "impulse_N_s": result,
            "transfer_failure": "Q3:20>C1:12",
            "e03_count": len(room_solutions), "e03_forced_Q2": ["C1", "S2"],
            "intervals": interval_results,
            "limit": "验证例题数值和关系，不判断教学质量或课堂效果"}


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))

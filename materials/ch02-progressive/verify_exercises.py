"""Independent exhaustive/arithmetical checks for the progressive edition."""
from pathlib import Path
from fractions import Fraction
from collections import deque
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = json.loads((HERE / "exercise-inputs.json").read_text())
CHECKS = []


def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    CHECKS.append({"name": name, "actual": actual, "expected": expected})


def paths(edges, start, goal):
    """Enumerate simple paths for small fixed graphs, independent of Dijkstra."""
    if start == goal:
        yield [start], 0
    for a, b, cost in edges:
        if a == start:
            remaining = [e for e in edges if e[0] != start and e[1] != start]
            for rest, weight in paths(remaining, b, goal):
                yield [start, *rest], cost + weight


def schedule(activities):
    end, starts = {}, {}
    for item in activities:
        ident = item["id"]
        predecessors = item.get("pred", item.get("predecessors", []))
        starts[ident] = max((end[p] for p in predecessors), default=0)
        end[ident] = starts[ident] + item.get("duration", item.get("minutes"))
    return starts, end


def confusion(actual, predicted):
    return [sum(a == aa and p == pp for a, p in zip(actual, predicted))
            for aa, pp in [(1, 1), (0, 1), (1, 0), (0, 0)]]


def service_minimum(stairs=False, closed=(), unknown=(), allow_unknown=False,
                    service_by=8, service_minutes=2):
    """Enumerate reachable (location, service flag, minute) states up to40 minutes.

    Keeping time explicit allows revisits and optional service on reaching C;
    this is independent of the shortest-path lower-bound argument in answers.
    """
    edges = []
    for e in D["e06"]["undirected_edges"]:
        pair = frozenset((e["a"], e["b"]))
        if (e["stairs"] and not stairs) or pair in closed:
            continue
        if pair in unknown and not allow_unknown:
            continue
        edges += [(e["a"], e["b"], e["minutes"]), (e["b"], e["a"], e["minutes"])]
    states = {(D["e06"]["start"], False, 0)}
    queue = deque(states)
    arrivals = []
    while queue:
        node, done, minute = queue.popleft()
        if node == "X" and done:
            arrivals.append(minute)
        options = [(b, done, minute + cost) for a, b, cost in edges if a == node]
        if node == "C" and not done and minute + service_minutes <= service_by:
            options.append((node, True, minute + service_minutes))
        for state in options:
            if state[2] <= 40 and state not in states:
                states.add(state); queue.append(state)
    return min(arrivals) if arrivals else None


def derive():
    e1 = D["e01"]
    all_paths = list(paths([(e["from"], e["to"], e["minutes"]) for e in e1["edges"]], "H", "L"))
    def valid(path, step_free):
        now = e1["start_minute_of_day"]
        for a, b in zip(path, path[1:]):
            edge = next(e for e in e1["edges"] if (e["from"], e["to"]) == (a, b))
            if step_free and not edge["step_free"]:
                return False
            now += edge["minutes"]
            limit = edge["completion_deadline_minute_of_day"]
            if limit is not None and now > limit:
                return False
        return now <= e1["arrival_deadline_minute_of_day"]
    check("E01 confirmed step-free route", [p for p, _ in all_paths if valid(p, True)], [["H", "K", "L"]])
    check("E01 cancel stairs requirement still excludes late J-L", [p for p, _ in all_paths if valid(p, False)], [["H", "K", "L"]])
    check("E01 arrival minute", 597 + 3 + 4, 604)
    entering = [(e["minutes"], e["to"]) for e in e1["edges"] if e["from"] == "H"]
    leaving = [(e["minutes"], e["from"]) for e in e1["edges"] if e["to"] == "L"]
    check("E01 coarse entering minimum source", min(entering), (2, "J"))
    check("E01 coarse leaving minimum source", min(leaving), (2, "J"))
    confirmed = [e for e in e1["edges"] if (e["from"], e["to"]) != ("K", "L")]
    confirmed_paths = paths([(e["from"], e["to"], e["minutes"]) for e in confirmed], "H", "L")
    check("E01 unknown K-L leaves no confirmed qualified route", [p for p, _ in confirmed_paths if valid(p, True)], [])
    for duration, finish, f_start in [(5, 15, 11), (2, 12, 8), (1, 12, 8)]:
        items = [dict(e, minutes=duration if e["id"] == "D" else e["minutes"]) for e in D["e02"]["activities"]]
        start, end = schedule(items)
        check(f"E02 D={duration} finish", end["G"], finish)
        check(f"E02 D={duration} F earliest start", start["F"], f_start)
        check(f"E02 D={duration} F dependency", start["F"], max(end["D"], end["E"]))
    check("E02 AI E start violates B dependency", 2 < 6, True)
    check("E02 AI F start violates baseline D dependency", 8 < 11, True)
    for subset, expected in [(D["e03"]["development_ids"], [[4, 0, 1, 3], [5, 0, 0, 3]]),
                             (D["e03"]["test_ids"], [[1, 0, 1, 2], [1, 1, 1, 1]])]:
        rows = [r for r in D["e03"]["rows"] if r["id"] in subset]
        actual = [r["y"] for r in rows]
        predictions = [[int(r["x"] >= 50) for r in rows],
                       [int(r["x"] >= 50 or (r["event"] == 1 and r["x"] >= 35)) for r in rows]]
        check(f"E03 {subset[0]} confusion TP/FP/FN/TN", [confusion(actual, p) for p in predictions], expected)
    graph = D["e04"]["graph"]["edges"]
    solutions = list(paths(graph, "S", "T"))
    check("E04 all simple path minimum", min(w for _, w in solutions), 5)
    check("E04 minimum route", [p for p, w in solutions if w == 5], [["S", "A", "B", "T"]])
    weights = dict((tuple(p), w) for p, w in solutions)
    check("E04 greedy candidate actual minutes", weights[("S", "A", "C", "T")], 11)
    check("E04 minimum edge count", min(len(p) - 1 for p, _ in solutions), 2)
    changed = [(a, b, -3 if (a, b) == ("B", "T") else w) for a, b, w in graph]
    check("E04 negative variant minimum", min(w for _, w in paths(changed, "S", "T")), 0)
    check("E04 negative counterexample", min(w for _, w in paths(D["e04"]["negative_counterexample"]["edges"], "S", "A")), 1)
    rows = D["e05"]["rows"]
    for key, count, total in [("baseline", 7, 77), ("candidate", 6, 49)]:
        values = [r[key] for r in rows if r[key] is not None]
        check(f"E05 {key} success count", len(values), count)
        check(f"E05 {key} success sum", sum(values), total)
    common = [r for r in rows if r["baseline"] is not None and r["candidate"] is not None]
    check("E05 paired improvement exact", str(sum(Fraction(r["baseline"] - r["candidate"]) for r in common) / len(common)), "7/3")
    check("E05 A successes B/C", [sum(r[key] is not None for r in rows if r["group"] == "A") for key in ["baseline", "candidate"]], [3, 2])
    check("E05 penalty totals B/C", [sum(r[key] if r[key] is not None else 16 for r in rows) for key in ["baseline", "candidate"]], [93, 81])
    check("E05 cache equality", 40 * 4, 120 + 10 * 4)
    check("E05 first strict integer win", next(q for q in range(1, 10) if 120 + 10 * q < 40 * q), 5)
    for stairs in [False, True]:
        check(f"E06 stairs={stairs} minimum", service_minimum(stairs=stairs), 12)
        closed = (frozenset(("C", "D")),)
        check(f"E06 stairs={stairs} CD closed", service_minimum(stairs=stairs, closed=closed), 14)
        unknown = (frozenset(("C", "X")),)
        check(f"E06 stairs={stairs} confirmed subset", service_minimum(stairs=stairs, closed=closed, unknown=unknown), 15)
        check(f"E06 stairs={stairs} optimistic CX7", service_minimum(stairs=stairs, closed=closed, unknown=unknown, allow_unknown=True), 14)
    check("E06 service cutoff6", service_minimum(service_by=6), None)
    check("E06 service cutoff7", service_minimum(service_by=7), 12)
    check("E06 arrival deadline11 infeasible", service_minimum() <= 11, False)
    check("E06 arrival deadline12 feasible", service_minimum() <= 12, True)
    new = D["new_worked_examples"]
    start, end = schedule(new["plan"])
    check("New T1-T4 worked plan", [start, end], [{"T1": 0, "T2": 0, "T3": 1, "T4": 3}, {"T1": 1, "T2": 2, "T3": 3, "T4": 4}])
    check("New worked route independent enumeration", min(w for _, w in paths(new["route_edges"], "P", "D")), 6)
    check("New seven-record confusion", confusion(new["confusion_actual"], new["confusion_predicted"]), [2, 1, 2, 2])
    fixed_predictions = [0, 1]
    check("Label40 fixed predictions TP/FP/FN/TN", confusion([int(n >= 40) for n in [35, 45]], fixed_predictions), [1, 0, 0, 1])
    check("Label30 fixed predictions TP/FP/FN/TN", confusion([int(n >= 30) for n in [35, 45]], fixed_predictions), [1, 0, 1, 0])
    check("Decision threshold0.5 fixed labels", confusion([0, 1], [int(s >= .5) for s in [.4, .7]]), [1, 0, 0, 1])
    check("Decision threshold0.3 fixed labels", confusion([0, 1], [int(s >= .3) for s in [.4, .7]]), [1, 1, 0, 0])
    check("New four-request means B/C", [str(sum(Fraction(x) for x in new["evaluation"][k] if x is not None) / sum(x is not None for x in new["evaluation"][k])) for k in ["baseline", "candidate"]], ["12", "17/2"])
    check("New threshold weighted score", [fp + 2 * fn for fp, fn in new["threshold_trials"]], [6, 6, 9])
    check("New threshold equal weight", [fp + fn for fp, fn in new["threshold_trials"]], [5, 4, 5])
    check("New cache first win differs from E05", next(q for q in range(1, 10) if 100 + 10 * q < 30 * q), 6)
    check("New RL reward backup/regular", [-6 * 3 - 8, -6 * 8], [-26, -48])


if __name__ == "__main__":
    derive()
    record = {"verification": "PASS", "check_count": len(CHECKS), "checks": CHECKS,
              "input_sha256": hashlib.sha256((HERE / "exercise-inputs.json").read_bytes()).hexdigest(),
              "manuscript_sha256": hashlib.sha256((ROOT / "manuscripts/ch02-progressive/ch02.md").read_bytes()).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "递进版固定E01—E06与新增独立示范；小图路径穷举、显式含时间服务状态遍历、分组算术。不是实际模型、课堂或页面验收。"}
    (HERE / "exercise-verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(f"PASS: {len(CHECKS)} independent checks")

#!/usr/bin/env python3
"""Independently derive and check Chapter 2 exercise results (stdlib only)."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import heapq
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = Path(__file__).with_name("exercise-inputs.json")
DEFAULT_OUTPUT = Path(__file__).with_name("exercise-verification.json")
CHECKS: list[dict[str, Any]] = []


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator,
                "decimal": float(value)}
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, set):
        return [plain(x) for x in sorted(value)]
    if isinstance(value, (list, tuple)):
        return [plain(x) for x in value]
    return value


def check(name: str, actual: Any, expected: Any) -> None:
    passed = actual == expected
    CHECKS.append({"name": name, "passed": passed,
                   "actual": plain(actual), "expected": plain(expected)})
    if not passed:
        raise AssertionError(f"{name}: actual={actual!r}, expected={expected!r}")


def adjacency(edges: list[tuple[str, str, int]], directed: bool = True):
    graph: dict[str, list[tuple[str, int]]] = {}
    for left, right, weight in edges:
        graph.setdefault(left, []).append((right, weight))
        graph.setdefault(right, [])
        if not directed:
            graph[right].append((left, weight))
    for neighbors in graph.values():
        neighbors.sort(key=lambda pair: pair[0])
    return graph


def enumerate_simple_paths(graph, start: str, goal: str):
    """Enumerate every vertex-simple route; suitable for these tiny teaching graphs."""
    found: list[dict[str, Any]] = []

    def visit(node: str, route: list[str], cost: int) -> None:
        if node == goal:
            found.append({"route": route[:], "cost": cost})
            return
        for nxt, weight in graph.get(node, []):
            if nxt not in route:
                visit(nxt, route + [nxt], cost + weight)

    visit(start, [start], 0)
    return found


def bfs(graph, start: str, goal: str):
    queue = [start]
    parent: dict[str, str | None] = {start: None}
    order: list[str] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        if node == goal:
            break
        for nxt, _ in graph.get(node, []):
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    if goal not in parent:
        return {"order": order, "route": None}
    route = []
    node: str | None = goal
    while node is not None:
        route.append(node)
        node = parent[node]
    return {"order": order, "route": list(reversed(route))}


def dijkstra(graph, start: str, goal: str | None = None):
    """Standard settled-node Dijkstra with lexical tie-break and stale-key skipping."""
    dist = {start: 0}
    parent: dict[str, str | None] = {start: None}
    heap = [(0, start)]
    settled: set[str] = set()
    trace: list[dict[str, Any]] = []
    while heap:
        distance, node = heapq.heappop(heap)
        if node in settled or distance != dist.get(node):
            continue
        settled.add(node)
        updates = []
        if node == goal:
            trace.append({"settled": node, "distance": distance, "updates": updates})
            break
        for nxt, weight in graph.get(node, []):
            candidate = distance + weight
            if nxt not in settled and candidate < dist.get(nxt, float("inf")):
                old = dist.get(nxt)
                dist[nxt] = candidate
                parent[nxt] = node
                heapq.heappush(heap, (candidate, nxt))
                updates.append({"node": nxt, "old": old, "new": candidate})
        trace.append({"settled": node, "distance": distance, "updates": updates})
    route = None
    if goal is not None and goal in dist and goal in settled:
        route = []
        node: str | None = goal
        while node is not None:
            route.append(node)
            node = parent[node]
        route.reverse()
    return {"distances": dist, "settled_order": [x["settled"] for x in trace],
            "route": route, "trace": trace}


def topological_order(activities):
    pending = {a["id"]: set(a["predecessors"]) for a in activities}
    order: list[str] = []
    while pending:
        ready = sorted(node for node, preds in pending.items() if not preds)
        if not ready:
            raise ValueError("dependency graph is cyclic")
        for node in ready:
            order.append(node)
            del pending[node]
        for preds in pending.values():
            preds.difference_update(ready)
    return order


def schedule(activities):
    data = {a["id"]: a for a in activities}
    order = topological_order(activities)
    starts: dict[str, int] = {}
    ends: dict[str, int] = {}
    for node in order:
        preds = data[node]["predecessors"]
        starts[node] = max((ends[p] for p in preds), default=0)
        ends[node] = starts[node] + data[node]["minutes"]
    sinks = sorted(node for node in data if not any(node in a["predecessors"] for a in activities))
    paths: list[dict[str, Any]] = []

    def extend(node: str, path: list[str], cost: int):
        if node in sinks:
            paths.append({"path": path[:], "minutes": cost})
            return
        for nxt in sorted(n for n, a in data.items() if node in a["predecessors"]):
            extend(nxt, path + [nxt], cost + data[nxt]["minutes"])

    sources = sorted(node for node in data if not data[node]["predecessors"])
    for source in sources:
        extend(source, [source], data[source]["minutes"])
    maximum = max(p["minutes"] for p in paths)
    critical = [p for p in paths if p["minutes"] == maximum]
    return {"topological_order": order,
            "schedule": {n: {"start": starts[n], "finish": ends[n]} for n in order},
            "project_minutes": max(ends.values()), "critical_paths": critical,
            "all_source_to_sink_paths": paths}


def e01(data):
    def candidate_routes(edges, require_step_free=True):
        graph: dict[str, list[dict[str, Any]]] = {}
        for edge in edges:
            if edge["status"] != "confirmed":
                continue
            if require_step_free and not edge["step_free"]:
                continue
            graph.setdefault(edge["from"], []).append(edge)
        found = []

        def visit(node, route, elapsed):
            if node == data["goal"]:
                found.append({"route": route[:], "minutes": elapsed,
                              "arrival_minute_of_day": data["start_minute_of_day"] + elapsed})
                return
            for edge in sorted(graph.get(node, []), key=lambda e: e["to"]):
                nxt = edge["to"]
                if nxt in route:
                    continue
                finish = data["start_minute_of_day"] + elapsed + edge["minutes"]
                deadline = edge["completion_deadline_minute_of_day"]
                if deadline is not None and finish > deadline:
                    continue
                visit(nxt, route + [nxt], elapsed + edge["minutes"])

        visit(data["start"], [data["start"]], 0)
        return [r for r in found if r["arrival_minute_of_day"] <= data["arrival_deadline_minute_of_day"]]

    routes_profile = candidate_routes(data["edges"], True)
    routes_relaxed = candidate_routes(data["edges"], False)
    changed = [dict(e) for e in data["edges"]]
    for edge in changed:
        if [edge["from"], edge["to"]] == data["variants"]["unknown_edge"]:
            edge["status"] = "unknown"
    routes_unknown = candidate_routes(changed, True)

    merged = data["coarse_merge"]["merged_nodes"]
    merged_name = data["coarse_merge"]["merged_name"]
    projected: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for edge in data["edges"]:
        a = merged_name if edge["from"] in merged else edge["from"]
        b = merged_name if edge["to"] in merged else edge["to"]
        projected.setdefault((a, b), []).append(edge)
    coarse_edges = []
    for (a, b), origins in projected.items():
        best = min(origins, key=lambda edge: edge["minutes"])
        coarse_edges.append({"from": a, "to": b, "minutes": best["minutes"],
                             "selected_origin": [best["from"], best["to"]],
                             "step_free": best["step_free"]})
    return {"confirmed_step_free_routes": routes_profile,
            "profile_cancelled_routes_still_obeying_edge_time_conditions": routes_relaxed,
            "unknown_K_to_L_excluded_from_confirmed_routes": routes_unknown,
            "coarse_pairwise_minimum_edges": coarse_edges,
            "directed_return_edge_does_not_create_H_to_L": not any(
                e["from"] == "H" and e["to"] == "L" for e in data["edges"])}


def e03(data):
    records = {row["id"]: row for row in data["rows"]}
    rules = data["rules"]

    def predicts(rule, row):
        spec = rules[rule]
        return row["x"] >= spec["x_gte"] or (
            row["event"] == spec["or_event_equals"] and row["x"] >= spec["and_x_gte"]
        ) if "or_event_equals" in spec else row["x"] >= spec["x_gte"]

    summaries = {}
    predictions: dict[str, dict[str, int]] = {}
    for split, ids in (("development", data["development_ids"]), ("test", data["test_ids"])):
        summaries[split] = {}
        for rule in rules:
            tp = fn = fp = tn = 0
            row_predictions = {}
            for record_id in ids:
                row = records[record_id]
                pred = int(predicts(rule, row))
                row_predictions[record_id] = pred
                if pred == 1 and row["y"] == 1: tp += 1
                elif pred == 0 and row["y"] == 1: fn += 1
                elif pred == 1 and row["y"] == 0: fp += 1
                else: tn += 1
            predictions[f"{split}_{rule}"] = row_predictions
            n = len(ids)
            summaries[split][rule] = {
                "TP": tp, "FN": fn, "FP": fp, "TN": tn,
                "accuracy": Fraction(tp + tn, n),
                "precision": Fraction(tp, tp + fp),
                "recall": Fraction(tp, tp + fn)
            }
    return {"confusion_and_metrics": summaries, "predictions": predictions,
            "fixed_split_record_counts": {"development": len(data["development_ids"]),
                                          "test": len(data["test_ids"])}}


def e04_graph(data, directed=True):
    return adjacency([tuple(edge) for edge in data], directed=directed)


def greedy_local(graph, start, goal):
    route = [start]
    cost = 0
    while route[-1] != goal:
        choices = [(weight, nxt) for nxt, weight in graph.get(route[-1], []) if nxt not in route]
        if not choices:
            return {"route": None, "cost": None}
        weight, nxt = min(choices, key=lambda item: (item[0], item[1]))
        route.append(nxt)
        cost += weight
    return {"route": route, "cost": cost}


def e04(data):
    graph_data = data["graph"]
    graph = e04_graph(graph_data["edges"])
    brute = enumerate_simple_paths(graph, graph_data["start"], graph_data["goal"])
    bfs_result = bfs(graph, graph_data["start"], graph_data["goal"])
    dijkstra_result = dijkstra(graph, graph_data["start"], graph_data["goal"])
    greedy_result = greedy_local(graph, graph_data["start"], graph_data["goal"])

    negative_edges = [tuple(edge) for edge in graph_data["edges"]]
    replacement = tuple(data["negative_variant"]["replace_edge"])
    negative_edges = [replacement if edge[:2] == replacement[:2] else edge for edge in negative_edges]
    negative_graph = e04_graph(negative_edges)
    negative_dijkstra = dijkstra(negative_graph, graph_data["start"], graph_data["goal"])
    negative_brute = enumerate_simple_paths(negative_graph, graph_data["start"], graph_data["goal"])

    counter = data["negative_counterexample"]
    counter_graph = e04_graph(counter["edges"])
    counter_dijkstra = dijkstra(counter_graph, counter["start"], counter["goal"])
    counter_paths = enumerate_simple_paths(counter_graph, counter["start"], counter["goal"])

    initial = data["records"]
    first_pass = sorted(initial, key=lambda r: r["submitted"])
    second_pass = sorted(first_pass, key=lambda r: r["priority"])
    composite = sorted(initial, key=lambda r: (r["priority"], r["submitted"]))

    worked = data["worked_graph"]
    worked_graph = e04_graph(worked["edges"])
    worked_bfs = bfs(worked_graph, worked["start"], worked["goal"])
    worked_dijkstra = dijkstra(worked_graph, worked["start"], worked["goal"])
    worked_greedy = greedy_local(worked_graph, worked["start"], worked["goal"])
    worked_paths = enumerate_simple_paths(worked_graph, worked["start"], worked["goal"])

    return {
        "exercise_graph": {"all_simple_routes": brute,
                           "bfs": {**bfs_result, "edge_count": len(bfs_result["route"]) - 1},
                           "local_greedy": greedy_result,
                           "dijkstra": dijkstra_result,
                           "negative_B_to_T_variant": {
                               "dijkstra": negative_dijkstra,
                               "all_simple_routes": negative_brute,
                               "true_minimum": min(p["cost"] for p in negative_brute)},
                           "counterexample": {
                               "dijkstra": counter_dijkstra,
                               "all_simple_routes": counter_paths,
                               "true_minimum": min(p["cost"] for p in counter_paths)}},
        "stable_sort": {"input": [r["id"] for r in initial],
                        "first_submitted_stable": [r["id"] for r in first_pass],
                        "then_priority_stable": [r["id"] for r in second_pass],
                        "composite_key_priority_submitted": [r["id"] for r in composite]},
        "worked_figure_graph": {"all_simple_routes": worked_paths,
                                "bfs": {**worked_bfs, "edge_count": len(worked_bfs["route"]) - 1,
                                        "route_minutes": sum(next(w for n, w in worked_graph[a] if n == b)
                                                             for a, b in zip(worked_bfs["route"], worked_bfs["route"][1:]))},
                                "local_greedy": worked_greedy,
                                "dijkstra": worked_dijkstra}}


def e05(data):
    penalty = data["acceptance"]["failure_penalty_minutes"]
    rows = data["rows"]
    metrics = {}
    for method in ("baseline", "candidate"):
        method_metrics = {"overall": {}, "groups": {}}
        for group in sorted({r["group"] for r in rows}):
            subset = [r for r in rows if r["group"] == group]
            successes = [r[method] for r in subset if r[method] is not None]
            method_metrics["groups"][group] = {
                "successes": len(successes), "requests": len(subset),
                "coverage": Fraction(len(successes), len(subset)),
                "successful_minutes_sum": sum(successes),
                "successful_mean_minutes": Fraction(sum(successes), len(successes))}
        successes = [r[method] for r in rows if r[method] is not None]
        method_metrics["overall"] = {
            "successes": len(successes), "requests": len(rows),
            "coverage": Fraction(len(successes), len(rows)),
            "successful_minutes_sum": sum(successes),
            "successful_mean_minutes": Fraction(sum(successes), len(successes)),
            "failure_penalty_mean_minutes": Fraction(sum(successes) + penalty * (len(rows) - len(successes)), len(rows)),
            "all_successes_at_or_under_15": all(x <= data["acceptance"]["max_success_minutes"] for x in successes)}
        method_metrics["overall"]["group_A_gate_pass"] = (
            method_metrics["groups"][data["acceptance"]["group"]]["successes"]
            >= data["acceptance"]["min_successes"])
        metrics[method] = method_metrics
    common = [r for r in rows if r["baseline"] is not None and r["candidate"] is not None]
    baseline_common = sum(r["baseline"] for r in common)
    candidate_common = sum(r["candidate"] for r in common)
    cost = data["query_cost_ms"]
    query_results = {str(q): {"baseline_ms": cost["baseline_per_query"] * q,
                              "candidate_ms": cost["candidate_preprocess"] + cost["candidate_per_query"] * q,
                              "candidate_strictly_faster": cost["candidate_preprocess"] + cost["candidate_per_query"] * q
                              < cost["baseline_per_query"] * q}
                     for q in (1, 4, 5)}
    changed_map_costs = {"baseline_per_query_ms": cost["baseline_per_query"],
                         "candidate_per_query_ms": cost["candidate_preprocess"] + cost["candidate_per_query"],
                         "candidate_strictly_faster_for_positive_query_count":
                         cost["candidate_preprocess"] + cost["candidate_per_query"]
                         < cost["baseline_per_query"]}
    return {"method_metrics": metrics,
            "common_successes": [r["id"] for r in common],
            "paired_baseline_minus_candidate_minutes": Fraction(baseline_common - candidate_common, len(common)),
            "paired_totals_minutes": {"baseline": baseline_common, "candidate": candidate_common,
                                      "n": len(common)},
            "adoption_gates": {m: metrics[m]["overall"]["group_A_gate_pass"]
                               and metrics[m]["overall"]["all_successes_at_or_under_15"]
                               for m in metrics},
            "query_costs": {"strict_faster_when_query_count_gt": Fraction(
                                cost["candidate_preprocess"],
                                cost["baseline_per_query"] - cost["candidate_per_query"]),
                            "sample_query_counts": query_results,
                            "when_map_changes_each_query": changed_map_costs},
            "unknown_outcome_handling": {
                "confirmed_received": "record success by original operation ID; do not resend",
                "confirmed_not_applied_and_quiescent": "controlled retry is only eligible under a retry/idempotency contract, same identity, current version and bounded policy",
                "not_found_but_in_flight_not_excluded": "remain UNKNOWN and pause; absence alone does not rule out a pending effect",
                "still_unknown": "remain UNKNOWN and pause",
                "no_query_capability": "remain UNKNOWN and pause; preserve the original operation ID"}}


def state_search(graph, start, goal, service_node=None, service_minutes=0,
                 service_deadline=None, max_total=None):
    """Dijkstra over (location, service_done); charge service on first arrival."""
    start_served = service_node is None
    start_state = (start, start_served)
    dist = {start_state: 0}
    parent: dict[tuple[str, bool], tuple[str, bool] | None] = {start_state: None}
    heap = [(0, start, start_served)]
    settled = set()
    goal_state = (goal, True)
    while heap:
        elapsed, node, served = heapq.heappop(heap)
        state = (node, served)
        if state in settled or elapsed != dist.get(state):
            continue
        settled.add(state)
        if state == goal_state:
            break
        for nxt, walk_minutes in graph.get(node, []):
            next_served = served
            next_elapsed = elapsed + walk_minutes
            if service_node is not None and not served and nxt == service_node:
                next_elapsed += service_minutes
                next_served = True
                if service_deadline is not None and next_elapsed > service_deadline:
                    continue
            next_state = (nxt, next_served)
            if next_state in settled or next_elapsed >= dist.get(next_state, float("inf")):
                continue
            dist[next_state] = next_elapsed
            parent[next_state] = state
            heapq.heappush(heap, (next_elapsed, nxt, next_served))
    if goal_state not in dist:
        return {"reachable": False, "minimum_minutes": None, "route": None,
                "service_completed_minute": None}
    states = []
    state: tuple[str, bool] | None = goal_state
    while state is not None:
        states.append(state)
        state = parent[state]
    states.reverse()
    route = [item[0] for item in states]
    service_index = route.index(service_node) if service_node else None
    service_time = None
    if service_node is not None:
        service_time = 0
        for left, right in zip(route, route[1:]):
            service_time += next(w for n, w in graph[left] if n == right)
            if right == service_node and service_time >= 0:
                service_time += service_minutes
                break
    total = dist[goal_state]
    return {"reachable": True, "minimum_minutes": total, "route": route,
            "service_completed_minute": service_time,
            "meets_arrival_deadline": max_total is None or total <= max_total,
            "meets_service_deadline": service_deadline is None or service_time <= service_deadline,
            "service_route_index": service_index}


def enumerate_augmented_routes(graph, start, goal, service_node, service_minutes,
                               service_deadline=None):
    routes = []

    def visit(node, served, route, elapsed, service_at, seen_states):
        if node == goal and served:
            routes.append({"route": route[:], "minutes": elapsed,
                           "service_completed_minute": service_at})
            return
        for nxt, walk in graph.get(node, []):
            next_served = served
            next_elapsed = elapsed + walk
            next_service_at = service_at
            if not served and nxt == service_node:
                next_elapsed += service_minutes
                next_service_at = next_elapsed
                next_served = True
                if service_deadline is not None and next_service_at > service_deadline:
                    continue
            state = (nxt, next_served)
            if state in seen_states:
                continue
            visit(nxt, next_served, route + [nxt], next_elapsed, next_service_at,
                  seen_states | {state})

    visit(start, False, [start], 0, None, {(start, False)})
    return routes


def bfs_augmented(graph, start, goal, service_node):
    start_state = (start, start == service_node)
    queue = [(start_state, [start])]
    seen = {start_state}
    while queue:
        (node, served), route = queue.pop(0)
        if node == goal and served:
            return {"route": route, "road_segments": len(route) - 1}
        for nxt, _ in graph.get(node, []):
            next_served = served or nxt == service_node
            state = (nxt, next_served)
            if state not in seen:
                seen.add(state)
                queue.append((state, route + [nxt]))
    return {"route": None, "road_segments": None}


def evaluate_route_minutes(graph, route, service_node, service_minutes):
    elapsed = 0
    service_done = None
    for previous, destination in zip(route, route[1:]):
        # The caller supplies the route; choose the recorded undirected adjacency edge.
        elapsed += next(w for n, w in graph[previous] if n == destination)
        if destination == service_node and service_done is None:
            elapsed += service_minutes
            service_done = elapsed
    return {"walk_and_service_minutes": elapsed, "service_completed_minute": service_done}


def e06(data):
    def make_edges(exclude=(), unknown=()):
        result = []
        excluded = {frozenset(pair) for pair in exclude}
        unknown_set = {frozenset(pair) for pair in unknown}
        for edge in data["undirected_edges"]:
            pair = frozenset((edge["a"], edge["b"]))
            if pair in excluded or pair in unknown_set:
                continue
            result.extend([(edge["a"], edge["b"], edge["minutes"]),
                           (edge["b"], edge["a"], edge["minutes"])])
        return result

    def profile_graph(exclude=(), unknown=(), allow_stairs=False):
        edges = make_edges(exclude, unknown)
        if not allow_stairs:
            stair_pairs = {frozenset((e["a"], e["b"])) for e in data["undirected_edges"] if e["stairs"]}
            edges = [edge for edge in edges if frozenset(edge[:2]) not in stair_pairs]
        return adjacency(edges, directed=True)

    ordinary = {}
    augmented = {}
    all_optimal = {}
    for allow_stairs, label in ((False, "no_stairs"), (True, "stairs_allowed")):
        graph = profile_graph(allow_stairs=allow_stairs)
        result = state_search(graph, data["start"], data["goal"], data["service_node"],
                              data["service_minutes"], data["service_deadline"], data["arrival_deadline"])
        routes = enumerate_augmented_routes(graph, data["start"], data["goal"], data["service_node"],
                                             data["service_minutes"], data["service_deadline"])
        best = min(r["minutes"] for r in routes)
        best_routes = [r for r in routes if r["minutes"] == best]
        check(f"E06 {label} state-search agrees with exhaustive augmented routes", result["minimum_minutes"], best)
        augmented[label] = result
        all_optimal[label] = best_routes
        no_service = state_search(graph, data["start"], data["goal"])
        ordinary[label] = no_service

    no_stairs_graph = profile_graph()
    bfs_result = bfs_augmented(no_stairs_graph, data["start"], data["goal"], data["service_node"])
    bfs_time = evaluate_route_minutes(no_stairs_graph, bfs_result["route"], data["service_node"], data["service_minutes"])

    closed_graph = profile_graph(exclude=[data["variants"]["close_edge"]])
    closed = state_search(closed_graph, data["start"], data["goal"], data["service_node"],
                          data["service_minutes"], data["service_deadline"], data["arrival_deadline"])
    closed_routes = enumerate_augmented_routes(closed_graph, data["start"], data["goal"], data["service_node"],
                                                data["service_minutes"], data["service_deadline"])
    closed_min = min(r["minutes"] for r in closed_routes)
    unknown_edge = data["variants"]["unknown_edge_after_close"]
    known_subgraph = profile_graph(exclude=[data["variants"]["close_edge"]], unknown=[unknown_edge])
    unknown_result = state_search(known_subgraph, data["start"], data["goal"], data["service_node"],
                                  data["service_minutes"], data["service_deadline"], data["arrival_deadline"])
    service_deadline_6 = state_search(no_stairs_graph, data["start"], data["goal"], data["service_node"],
                                      data["service_minutes"], 6, data["arrival_deadline"])
    service_deadline_7 = state_search(no_stairs_graph, data["start"], data["goal"], data["service_node"],
                                      data["service_minutes"], 7, data["arrival_deadline"])
    arrival_deadline_11 = state_search(no_stairs_graph, data["start"], data["goal"], data["service_node"],
                                       data["service_minutes"], data["service_deadline"], 11)
    arrival_deadline_12 = state_search(no_stairs_graph, data["start"], data["goal"], data["service_node"],
                                       data["service_minutes"], data["service_deadline"], 12)
    return {"deadline_contract": {"service_complete_by": data["service_deadline"],
                                  "arrive_by": data["arrival_deadline"], "map_version": data["map_version"],
                                  "rule_version": data["rule_version"]},
            "shortest_time_with_service": augmented,
            "all_exhaustively_verified_optimal_routes": all_optimal,
            "shortest_time_without_service": ordinary,
            "bfs_minimum_road_segments_no_stairs": {**bfs_result, **bfs_time,
                                                     "meets_arrival_deadline": bfs_time["walk_and_service_minutes"] <= data["arrival_deadline"]},
            "close_C_D": {"shortest_confirmed_route": closed,
                          "minimum_confirmed_route_minutes_exhaustive": closed_min,
                          "has_route_meeting_arrival_deadline": any(
                              r["minutes"] <= data["arrival_deadline"] for r in closed_routes)},
            "close_C_D_and_C_X_unknown": {"unknown_edge": "C-X",
                                          "unknown_edge_excluded_from_confirmed_subgraph": True,
                                          "shortest_confirmed_subgraph_result": unknown_result,
                                          "interpretation": "A route using C-X is unconfirmed; exclusion yields only a confirmed-subgraph result, not proof that no physical route exists."},
            "deadline_variants": {"service_by_6": service_deadline_6,
                                  "service_by_7": service_deadline_7,
                                  "arrive_by_11": arrival_deadline_11,
                                  "arrive_by_12": arrival_deadline_12}}


def derive(inputs):
    results = {"E01": e01(inputs["e01"])}

    initial = schedule(inputs["e02"]["activities"])
    changed_data = json.loads(json.dumps(inputs["e02"]["activities"]))
    changed_id = inputs["e02"]["changed_duration"]["activity"]
    for activity in changed_data:
        if activity["id"] == changed_id:
            activity["minutes"] = inputs["e02"]["changed_duration"]["minutes"]
    changed = schedule(changed_data)
    versions = inputs["e02"]["interface_versions"]
    results["E02"] = {"initial": initial, "D_duration_changed": changed,
                      "actual_map_versions_match": versions["B_map_version"] == versions["C_map_version"],
                      "interface_compatibility_decision": "cannot combine as one same-version snapshot without a verified compatibility mapping"}

    results["E03"] = e03(inputs["e03"])
    results["E04"] = e04(inputs["e04"])
    results["E05"] = e05(inputs["e05"])
    results["E06"] = e06(inputs["e06"])
    return results


def perform_checks(inputs, results):
    e1 = results["E01"]
    check("E01 confirmed step-free path and 09:57 arrival", e1["confirmed_step_free_routes"],
          [{"route": ["H", "K", "L"], "minutes": 7, "arrival_minute_of_day": 604}])
    check("E01 cancelling profile does not defeat J-L completion cutoff",
          e1["profile_cancelled_routes_still_obeying_edge_time_conditions"],
          [{"route": ["H", "K", "L"], "minutes": 7, "arrival_minute_of_day": 604}])
    check("E01 unknown K-L leaves no fully confirmed step-free route",
          e1["unknown_K_to_L_excluded_from_confirmed_routes"], [])
    check("E01 direction is not reversed", e1["directed_return_edge_does_not_create_H_to_L"], True)
    check("E01 coarse merge exposes a 4-minute but profile-invalid projection",
          [(e["from"], e["to"], e["minutes"], e["selected_origin"], e["step_free"])
           for e in e1["coarse_pairwise_minimum_edges"] if e["from"] in ("H", "P") and e["to"] in ("P", "L")],
          [("H", "P", 2, ["H", "J"], False), ("P", "L", 2, ["J", "L"], False)])

    e2 = results["E02"]
    check("E02 initial finish and critical path", (e2["initial"]["project_minutes"],
          [p["path"] for p in e2["initial"]["critical_paths"]]),
          (15, [["A", "B", "D", "F", "G"]]))
    check("E02 initial earliest start/finish values",
          {n: (v["start"], v["finish"]) for n, v in e2["initial"]["schedule"].items()},
          {"A": (0, 2), "B": (2, 6), "C": (2, 5), "D": (6, 11),
           "E": (6, 8), "F": (11, 14), "G": (14, 15)})
    check("E02 D-shortened finish and both critical paths", (e2["D_duration_changed"]["project_minutes"],
          [p["path"] for p in e2["D_duration_changed"]["critical_paths"]]),
          (12, [["A", "B", "D", "F", "G"], ["A", "B", "E", "F", "G"]]))
    check("E02 supplied map versions conflict", e2["actual_map_versions_match"], False)
    for sequence in (["A", "B", "C", "D", "E", "F", "G"],
                     ["A", "C", "B", "E", "D", "F", "G"]):
        position = {node: i for i, node in enumerate(sequence)}
        legal = all(position[p] < position[a["id"]]
                    for a in inputs["e02"]["activities"] for p in a["predecessors"])
        check(f"E02 proposed topological sequence {sequence}", legal, True)

    e3 = results["E03"]["confusion_and_metrics"]
    expected = {
        "development": {"RA": (4, 1, 0, 3, Fraction(7, 8), Fraction(1), Fraction(4, 5)),
                        "RB": (5, 0, 0, 3, Fraction(1), Fraction(1), Fraction(1))},
        "test": {"RA": (1, 1, 0, 2, Fraction(3, 4), Fraction(1), Fraction(1, 2)),
                 "RB": (1, 1, 1, 1, Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))}}
    for split, methods in expected.items():
        for rule, vals in methods.items():
            actual = e3[split][rule]
            check(f"E03 {split} {rule} confusion and exact metrics",
                  (actual["TP"], actual["FN"], actual["FP"], actual["TN"], actual["accuracy"],
                   actual["precision"], actual["recall"]), vals)
    check("E03 fixed independent split sizes",
          results["E03"]["fixed_split_record_counts"], {"development": 8, "test": 4})
    check("E03 RB test false positive is d11",
          [rid for rid, pred in results["E03"]["predictions"]["test_RB"].items()
           if pred == 1 and next(r["y"] for r in inputs["e03"]["rows"] if r["id"] == rid) == 0], ["d11"])

    e4 = results["E04"]
    check("E04 BFS deterministic order and path",
          (e4["exercise_graph"]["bfs"]["order"], e4["exercise_graph"]["bfs"]["route"],
           e4["exercise_graph"]["bfs"]["edge_count"]),
          (["S", "A", "B", "C", "T"], ["S", "A", "T"], 2))
    check("E04 local greedy path and cumulative cost",
          (e4["exercise_graph"]["local_greedy"]["route"], e4["exercise_graph"]["local_greedy"]["cost"]),
          (["S", "A", "C", "T"], 11))
    check("E04 Dijkstra path, distance and settle order",
          (e4["exercise_graph"]["dijkstra"]["route"],
           e4["exercise_graph"]["dijkstra"]["distances"]["T"],
           e4["exercise_graph"]["dijkstra"]["settled_order"]),
          (["S", "A", "B", "T"], 5, ["S", "A", "C", "B", "T"]))
    check("E04 Dijkstra agrees with exhaustive simple-route minimum",
          e4["exercise_graph"]["dijkstra"]["distances"]["T"],
          min(p["cost"] for p in e4["exercise_graph"]["all_simple_routes"]))
    check("E04 changed B-T edge violates precondition but this instance remains correct",
          (e4["exercise_graph"]["negative_B_to_T_variant"]["dijkstra"]["route"],
           e4["exercise_graph"]["negative_B_to_T_variant"]["dijkstra"]["distances"]["T"],
           e4["exercise_graph"]["negative_B_to_T_variant"]["true_minimum"]), (["S", "A", "B", "T"], 0, 0))
    check("E04 negative-edge counterexample settles a wrong target distance",
          (e4["exercise_graph"]["counterexample"]["dijkstra"]["distances"]["A"],
           e4["exercise_graph"]["counterexample"]["true_minimum"]), (2, 1))
    check("E04 stable multi-pass and composite sorts agree",
          (e4["stable_sort"]["first_submitted_stable"], e4["stable_sort"]["then_priority_stable"],
           e4["stable_sort"]["composite_key_priority_submitted"]),
          (["r3", "r4", "r2", "r1"], ["r4", "r2", "r3", "r1"], ["r4", "r2", "r3", "r1"]))
    check("Figure 2-5 BFS minimizes segments but not time",
          (e4["worked_figure_graph"]["bfs"]["route"], e4["worked_figure_graph"]["bfs"]["edge_count"],
           e4["worked_figure_graph"]["bfs"]["route_minutes"]), (["P", "A", "D"], 2, 13))
    check("Figure 2-5 local greedy and shortest-time Dijkstra results",
          (e4["worked_figure_graph"]["local_greedy"]["route"], e4["worked_figure_graph"]["local_greedy"]["cost"],
           e4["worked_figure_graph"]["dijkstra"]["route"],
           e4["worked_figure_graph"]["dijkstra"]["distances"]["D"]),
          (["P", "A", "C", "D"], 10, ["P", "B", "C", "D"], 7))
    check("Figure 2-5 Dijkstra agrees with exhaustive path minimum",
          e4["worked_figure_graph"]["dijkstra"]["distances"]["D"],
          min(p["cost"] for p in e4["worked_figure_graph"]["all_simple_routes"]))

    e5 = results["E05"]
    check("E05 overall success counts and coverage",
          {m: (e5["method_metrics"][m]["overall"]["successes"],
               e5["method_metrics"][m]["overall"]["coverage"]) for m in ("baseline", "candidate")},
          {"baseline": (7, Fraction(7, 8)), "candidate": (6, Fraction(3, 4))})
    check("E05 successful means use different denominators",
          {m: e5["method_metrics"][m]["overall"]["successful_mean_minutes"] for m in ("baseline", "candidate")},
          {"baseline": Fraction(11), "candidate": Fraction(49, 6)})
    check("E05 per-group coverage and means",
          {m: {g: (e5["method_metrics"][m]["groups"][g]["successes"],
                    e5["method_metrics"][m]["groups"][g]["coverage"],
                    e5["method_metrics"][m]["groups"][g]["successful_mean_minutes"])
               for g in ("N", "A")} for m in ("baseline", "candidate")},
          {"baseline": {"N": (4, Fraction(1), Fraction(19, 2)), "A": (3, Fraction(3, 4), Fraction(13))},
           "candidate": {"N": (4, Fraction(1), Fraction(15, 2)), "A": (2, Fraction(1, 2), Fraction(19, 2))}})
    check("E05 paired common-success mean difference", e5["paired_baseline_minus_candidate_minutes"], Fraction(7, 3))
    check("E05 failure-penalty auxiliary means",
          {m: e5["method_metrics"][m]["overall"]["failure_penalty_mean_minutes"] for m in ("baseline", "candidate")},
          {"baseline": Fraction(93, 8), "candidate": Fraction(81, 8)})
    check("E05 hard gates retain baseline and reject candidate",
          e5["adoption_gates"], {"baseline": True, "candidate": False})
    check("E05 preprocessing break-even is strictly more than four queries",
          (e5["query_costs"]["strict_faster_when_query_count_gt"],
           e5["query_costs"]["sample_query_counts"]["4"]["baseline_ms"],
           e5["query_costs"]["sample_query_counts"]["4"]["candidate_ms"],
           e5["query_costs"]["sample_query_counts"]["5"]["candidate_strictly_faster"]),
          (Fraction(4), 160, 160, True))
    check("E05 reprocessing on every map change removes the advantage",
          (e5["query_costs"]["when_map_changes_each_query"]["baseline_per_query_ms"],
           e5["query_costs"]["when_map_changes_each_query"]["candidate_per_query_ms"],
           e5["query_costs"]["when_map_changes_each_query"]["candidate_strictly_faster_for_positive_query_count"]),
          (40, 130, False))
    check("E05 ambiguous and unqueryable submit outcomes stay unknown",
          [e5["unknown_outcome_handling"][k] for k in (
              "not_found_but_in_flight_not_excluded", "still_unknown", "no_query_capability")],
          ["remain UNKNOWN and pause; absence alone does not rule out a pending effect",
           "remain UNKNOWN and pause", "remain UNKNOWN and pause; preserve the original operation ID"])

    e6 = results["E06"]
    check("E06 no-stairs augmented state reaches feasible 12-minute route",
          (e6["shortest_time_with_service"]["no_stairs"]["minimum_minutes"],
           e6["shortest_time_with_service"]["no_stairs"]["route"],
           e6["shortest_time_with_service"]["no_stairs"]["service_completed_minute"],
           e6["shortest_time_with_service"]["no_stairs"]["meets_arrival_deadline"]),
          (12, ["G", "P", "C", "D", "X"], 7, True))
    check("E06 stairs allowed has same optimum and validates alternate optimal route",
          (e6["shortest_time_with_service"]["stairs_allowed"]["minimum_minutes"],
           {tuple(r["route"]) for r in e6["all_exhaustively_verified_optimal_routes"]["stairs_allowed"]}),
          (12, {("G", "P", "C", "D", "X"), ("G", "P", "Q", "C", "D", "X")}))
    check("E06 removing service changes no-stairs optimum to 10 minutes",
          e6["shortest_time_without_service"]["no_stairs"]["minimum_minutes"], 10)
    check("E06 BFS route is three road segments but 14 minutes after service",
          (e6["bfs_minimum_road_segments_no_stairs"]["route"],
           e6["bfs_minimum_road_segments_no_stairs"]["road_segments"],
           e6["bfs_minimum_road_segments_no_stairs"]["walk_and_service_minutes"],
           e6["bfs_minimum_road_segments_no_stairs"]["meets_arrival_deadline"]),
          (["G", "P", "C", "X"], 3, 14, False))
    check("E06 closing C-D leaves confirmed shortest path 14 and misses deadline",
          (e6["close_C_D"]["minimum_confirmed_route_minutes_exhaustive"],
           e6["close_C_D"]["has_route_meeting_arrival_deadline"]), (14, False))
    check("E06 unknown C-X is not used and is not interpreted as physical impossibility",
          (e6["close_C_D_and_C_X_unknown"]["unknown_edge_excluded_from_confirmed_subgraph"],
           e6["close_C_D_and_C_X_unknown"]["shortest_confirmed_subgraph_result"]["minimum_minutes"],
           e6["close_C_D_and_C_X_unknown"]["interpretation"]),
          (True, 15, "A route using C-X is unconfirmed; exclusion yields only a confirmed-subgraph result, not proof that no physical route exists."))
    deadline_variants = e6["deadline_variants"]
    check("E06 service deadline boundary is inclusive at minute 7",
          (deadline_variants["service_by_6"]["reachable"],
           deadline_variants["service_by_7"]["service_completed_minute"],
           deadline_variants["service_by_7"]["meets_service_deadline"]), (False, 7, True))
    check("E06 arrival deadline boundary is inclusive at minute 12",
          (deadline_variants["arrive_by_11"]["minimum_minutes"],
           deadline_variants["arrive_by_11"]["meets_arrival_deadline"],
           deadline_variants["arrive_by_12"]["meets_arrival_deadline"]), (12, False, True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    script_path = Path(__file__).resolve()
    inputs = json.loads(input_path.read_text(encoding="utf-8"))
    results = derive(inputs)
    perform_checks(inputs, results)
    record = {
        "verification": "PASS",
        "scope": "Independent numeric and deterministic algorithm derivations for Chapter 2 exercises E01-E06 and the separate Figure 2-5 route graph.",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "command": f"python3 {script_path.relative_to(ROOT)} --input {input_path.relative_to(ROOT)} --output {output_path.relative_to(ROOT)}",
        "runtime": {"python": sys.version, "implementation": platform.python_implementation(),
                    "platform": platform.platform(), "dependencies": "Python standard library only"},
        "inputs": {"path": str(input_path.relative_to(ROOT)), "sha256": sha256(input_path)},
        "script": {"path": str(script_path.relative_to(ROOT)), "sha256": sha256(script_path)},
        "check_count": len(CHECKS),
        "checks": CHECKS,
        "computed_results": plain(results)
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{record['verification']}: {record['check_count']} checks")
    print(f"input sha256 {record['inputs']['sha256']}")
    print(f"script sha256 {record['script']['sha256']}")
    print(f"evidence {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

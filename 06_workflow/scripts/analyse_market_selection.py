#!/usr/bin/env python3
"""Reproduce the frozen K1–K6 evidence-fitness comparison; not a grade forecast."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "02_research/business-selection/market-selection-inputs.json"
DEFAULT_OUTPUT = ROOT / "02_research/business-selection/market-selection-results.json"
EPSILON = 1e-9


def weighted(scores: list[float], weights: list[float]) -> float:
    return sum(score * weight / 5 for score, weight in zip(scores, weights))


def evaluate(data: dict, scores: dict, weights: list[float], name: str) -> dict:
    totals = {country: weighted(values, weights) for country, values in scores.items()}
    best = max(totals.values())
    winners = sorted(country for country, value in totals.items() if abs(value - best) < EPSILON)
    eligible = [country for country in data["european_candidates"]
                if scores[country][0] >= data["data_gate_minimum"]
                and scores[country][2] >= data["data_gate_minimum"]]
    european = None
    if eligible:
        top_eu = max(totals[country] for country in eligible)
        tied = [country for country in eligible
                if top_eu - totals[country] <= data["eu_tie_margin"] + EPSILON]
        european = max(tied, key=lambda country: (scores[country][0], scores[country][2], totals[country]))
    non_eu = [country for country in scores if country not in data["european_candidates"]]
    challenger = max(non_eu, key=totals.get)
    exceeds_margin = bool(european and totals[challenger] - totals[european] > data["preference_margin"] + EPSILON)
    policy_choice = challenger if exceeds_margin else european or winners[0]
    return {"name": name, "weights": weights, "scores": scores,
            "totals": {country: round(value, 6) for country, value in totals.items()},
            "raw_winners": winners, "eligible_european": eligible,
            "preferred_european": european, "strongest_non_european": challenger,
            "non_european_margin": round(totals[challenger] - totals[european], 6) if european else None,
            "challenger_exceeds_margin": exceeds_margin, "per_run_policy_choice": policy_choice}


def analyse(data: dict) -> dict:
    weights = data["weights"]
    criteria = data["criteria"]
    scores = {country: row["scores"] for country, row in data["countries"].items()}
    if len(weights) != len(criteria) or abs(sum(weights) - 100) > EPSILON:
        raise ValueError("Criteria and weights must align and weights must sum to 100")
    if any(len(row) != len(criteria) or any(not 1 <= value <= 5 for value in row) for row in scores.values()):
        raise ValueError("Every country needs one score from 1 to 5 per criterion")
    base = evaluate(data, scores, weights, "base")
    runs = []
    for index, criterion in enumerate(criteria):
        for multiplier in (0.8, 1.2):
            changed = weights[index] * multiplier
            rest_factor = (100 - changed) / (100 - weights[index])
            adjusted = [changed if position == index else weight * rest_factor
                        for position, weight in enumerate(weights)]
            runs.append(evaluate(data, scores, adjusted, f"weight {criterion} x{multiplier}"))
    runs.append(evaluate(data, scores, [100 / len(criteria)] * len(criteria), "equal weights"))
    for country, row in scores.items():
        for index, criterion in enumerate(criteria):
            for delta in (-1, 1):
                value = min(5, max(1, row[index] + delta))
                if value == row[index]:
                    continue  # Exclude clipped no-op duplicates from the sensitivity denominator.
                changed = deepcopy(scores)
                changed[country][index] = value
                runs.append(evaluate(data, changed, weights, f"score {country} {criterion} {delta:+d}, clipped"))
    stresses = []
    for stress in data.get("stress_cases", []):
        changed = deepcopy(scores)
        for country, changes in stress["changes"].items():
            for criterion, value in changes.items():
                if not 1 <= value <= 5:
                    raise ValueError("Stress scores must remain between 1 and 5")
                changed[country][criteria.index(criterion)] = value
        stresses.append(evaluate(data, changed, weights, stress["name"]))
    challenger = base["strongest_non_european"]
    override_runs = sum(run["per_run_policy_choice"] == challenger for run in runs)
    recommendation = base["preferred_european"]
    if recommendation is None or (base["challenger_exceeds_margin"] and override_runs > len(runs) / 2):
        recommendation = base["per_run_policy_choice"]
    intervals = {}
    for country, row in scores.items():
        intervals[country] = {
            "all_scores_minus_one": round(weighted([max(1, value - 1) for value in row], weights), 6),
            "all_scores_plus_one": round(weighted([min(5, value + 1) for value in row], weights), 6)}
    return {"prepared_on": data["prepared_on"], "status": data["status"], "base": base,
            "sensitivity_runs": runs, "sensitivity_summary": {
                "runs": len(runs),
                "raw_winner_counts": dict(Counter(" / ".join(run["raw_winners"]) for run in runs)),
                "per_run_policy_choice_counts": dict(Counter(run["per_run_policy_choice"] for run in runs)),
                "raw_rank_reversals_or_ties": [run["name"] for run in runs if run["raw_winners"] != base["raw_winners"]],
                "strongest_non_european_override_runs": override_runs},
            "joint_stress_cases_excluded_from_majority_rule": stresses,
            "joint_score_bounds_not_confidence_intervals": intervals,
            "agent_recommendation_not_group_decision": recommendation,
            "interpretation": "Deterministic ordinal stress tests, not probabilities, statistical confidence or predicted marks. Joint stress cases are additional diagnostics, not extra votes in the frozen sensitivity rule."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = analyse(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Base evidence-fitness scores (NOT marks):", result["base"]["totals"])
    print("Sensitivity:", json.dumps(result["sensitivity_summary"], ensure_ascii=False))
    print("Agent recommendation (unapproved):", result["agent_recommendation_not_group_decision"])
    print("Saved:", args.output)


if __name__ == "__main__":
    main()

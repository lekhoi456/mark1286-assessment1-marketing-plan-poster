#!/usr/bin/env python3
"""Calculate explicitly unapproved marketing cost/funnel scenarios from saved inputs."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "02_research/marketing-plan/budget-scenario-inputs.json"
DEFAULT_OUTPUT = ROOT / "02_research/marketing-plan/budget-scenario-results.json"
HOUR_ITEMS = {
    "research_hours": "Research and service validation",
    "creative_hours": "Creative production and localisation",
    "management_hours": "Campaign management and optimisation",
    "partner_sales_hours": "Partner/account prospecting and consultative sales",
    "crm_support_hours": "CRM and customer-support handover",
}


def allocate(data: dict, budget: dict) -> dict:
    assumptions = data["common_assumptions"]
    sources = data["source_inputs"]
    lines = []
    for field, label in HOUR_ITEMS.items():
        hours = budget[field]
        if not hours:
            continue
        lines.append({"item": label, "quantity": hours, "unit": "hours",
                      "unit_cost": assumptions["professional_hourly_allowance"],
                      "cost": hours * assumptions["professional_hourly_allowance"],
                      "basis": "Unapproved hours and professional-cost allowance; not driver pay"})
    for field, label in (("paid_search", "Paid search"), ("paid_social", "Paid social")):
        lines.append({"item": label, "cost": budget[field], "basis": "Unapproved media envelope, not a platform quote"})
    impressions = budget["dooh_impressions"]
    if impressions:
        lines.extend([
            {"item": "Digital Copenhagen DOOH", "quantity": impressions / 1000,
             "unit": "thousand impressions", "unit_cost": sources["dooh_cpm"]["value"],
             "cost": impressions * sources["dooh_cpm"]["value"] / 1000,
             "basis": "afa-decaux-2026 p.3 list CPM; unapproved quantity, minimum order unconfirmed"},
            {"item": "DOOH setup", "quantity": 1, "unit": "assumed campaign setup",
             "unit_cost": sources["dooh_setup"]["value"], "cost": sources["dooh_setup"]["value"],
             "basis": "afa-decaux-2026 p.3; one setup assumed, creative production separately allocated"},
        ])
    lines.extend([
        {"item": "Analytics/CRM tools", "quantity": data["period_months"], "unit": "months",
         "unit_cost": budget["tools_per_month"], "cost": data["period_months"] * budget["tools_per_month"],
         "basis": "Unapproved software/data allowance; vendor procurement unconfirmed"},
        {"item": "First-ride incentive reserve", "cost": budget["incentive_reserve"],
         "basis": "Proposed capped voucher liability, not an existing European promotion"},
    ])
    contingency = budget["total"] - sum(line["cost"] for line in lines)
    if contingency < 0:
        raise ValueError("Line items exceed the proposed total")
    lines.append({"item": "Uncommitted contingency", "cost": contingency,
                  "basis": "Residual within proposed total; not forecast spending or a balancing revenue"})
    for line in lines:
        line["share_percent"] = line["cost"] / budget["total"] * 100
    return {"total": budget["total"], "lines": lines,
            "line_sum": sum(line["cost"] for line in lines),
            "share_sum_percent": sum(line["share_percent"] for line in lines),
            "professional_hours": sum(budget[field] for field in HOUR_ITEMS),
            "hours_per_month": sum(budget[field] for field in HOUR_ITEMS) / data["period_months"]}


def funnel(data: dict, budget: dict, performance: dict) -> dict:
    assumptions = data["common_assumptions"]
    sources = data["source_inputs"]
    if performance["search_cpc"] <= 0 or performance["social_cpm"] <= 0:
        raise ValueError("CPC and CPM must be positive")
    for field, value in performance.items():
        if field not in ("search_cpc", "social_cpm") and not 0 <= value <= 1:
            raise ValueError(f"{field} must be a fraction between zero and one")
    search_clicks = budget["paid_search"] / performance["search_cpc"]
    social_impressions = budget["paid_social"] / performance["social_cpm"] * 1000
    social_clicks = social_impressions * performance["social_ctr"]
    search_first = search_clicks * performance["search_click_to_first_paid_ride"]
    social_first = social_clicks * performance["social_click_to_first_paid_ride"]
    first_payers = (search_first + social_first) * (1 - performance["duplicate_acquisition_fraction"])
    mature = first_payers * assumptions["retention_eligible_fraction"]
    repeaters = mature * performance["repeat_90_day_fraction"]
    repeat_rides = repeaters * assumptions["extra_rides_per_repeater"]
    active_accounts = budget["qualified_b2b_leads"] * performance["b2b_lead_to_active_account"]
    account_rides = active_accounts * assumptions["b2b_rides_per_account_month"] * assumptions["b2b_average_active_months"]
    rides = first_payers + repeat_rides + account_rides
    voucher_capacity = math.floor(budget["incentive_reserve"] / assumptions["voucher_per_first_payer"])
    voucher_users = min(first_payers, voucher_capacity)
    voucher_cost = voucher_users * assumptions["voucher_per_first_payer"]
    media = budget["paid_search"] + budget["paid_social"]
    acquisition_cost = (media + voucher_cost) / first_payers if first_payers else None
    fare = (sources["fare_start"]["value"] + sources["fare_per_km"]["value"] * assumptions["illustrative_trip_km"]
            + sources["fare_per_minute"]["value"] * assumptions["illustrative_trip_minutes"])
    margins = []
    for margin in assumptions["contribution_margin_cases"]:
        per_ride = fare * margin
        margins.append({"assumed_contribution_fraction_before_marketing": margin,
                        "illustrative_contribution_per_ride": per_ride,
                        "contribution_before_programme_cost": rides * per_ride,
                        "contribution_less_full_reserved_programme_budget": rides * per_ride - budget["total"],
                        "rides_to_cover_full_reserved_budget": math.ceil(budget["total"] / per_ride),
                        "rides_per_new_payer_to_cover_paid_media_and_redeemed_incentive": acquisition_cost / per_ride if acquisition_cost is not None else None})
    return {"search_clicks": search_clicks, "social_impressions": social_impressions,
            "social_clicks": social_clicks, "search_attributed_first_payers_before_dedup": search_first,
            "social_attributed_first_payers_before_dedup": social_first,
            "deduplicated_first_payers": first_payers, "retention_eligible_first_payers": mature,
            "repeaters_within_90_days": repeaters, "additional_repeat_rides": repeat_rides,
            "active_b2b_accounts": active_accounts, "b2b_rides": account_rides,
            "total_attributed_ride_equivalents": rides,
            "voucher_user_capacity": voucher_capacity, "voucher_users": voucher_users,
            "voucher_redemption_cost": voucher_cost,
            "unused_incentive_reserve": budget["incentive_reserve"] - voucher_cost,
            "paid_media_cost_per_first_payer": media / first_payers if first_payers else None,
            "paid_media_plus_redeemed_incentive_cost_per_first_payer": acquisition_cost,
            "illustrative_trip_fare_not_average_revenue": fare,
            "illustrative_gross_booking_value_before_incentives": rides * fare,
            "contribution_scenarios": margins,
            "warning": "Fractional outputs are conditional arithmetic, not realised riders/accounts. No DOOH conversions attributed. Full-programme economics are not a fully allocated B2C CAC; B2B costs and accounts are separate. Gross booking value is not profit or incremental causal revenue."}


def model(data: dict) -> dict:
    result = {"prepared_on": data["prepared_on"], "status": data["status"],
              "selected_plan": data.get("selected_plan"),
              "currency": data["currency"], "period_months": data["period_months"], "budgets": {}}
    for name, budget in data["budgets"].items():
        result["budgets"][name] = {"allocation": allocate(data, budget),
                                  "performance_cases": {case: funnel(data, budget, assumptions)
                                                        for case, assumptions in data["performance_assumptions"].items()}}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = model(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, row in result["budgets"].items():
        case = row["performance_cases"]["illustrative"]
        print(f"{name}: DKK{row['allocation']['total']:,.0f}; allocation {row['allocation']['share_sum_percent']:.6f}%; "
              f"conditional first payers {case['deduplicated_first_payers']:.1f}; "
              f"ride equivalents {case['total_attributed_ride_equivalents']:.1f}; "
              f"gross booking-value proxy DKK{case['illustrative_gross_booking_value_before_incentives']:,.0f}")
    print("UNAPPROVED scenarios. Not company budgets, forecasts or demonstrated financial feasibility.")
    print("Saved:", args.output)


if __name__ == "__main__":
    main()

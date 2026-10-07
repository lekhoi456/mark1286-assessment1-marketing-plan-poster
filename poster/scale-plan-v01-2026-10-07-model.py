"""Scale-plan numbers for the D-163 rebuild (DKK30M market-entry plan).

Every poster figure in the scaled plan comes from this file. Inputs marked
ASSUMPTION are the group's planning assumptions and must be labelled as such;
inputs marked with an E-/DK- ID come from registered evidence.

Usage: python3 -B poster/scale-plan-v01-2026-10-07-model.py [OUT.json]
"""
import json
import sys

A = {
    'registered_cars': 590,             # E-020 / DK-20
    'avg_active_cars_year1': 450,       # ASSUMPTION: ramp to 590 by M6
    'trips_per_car_day': {'low': 10, 'base': 15, 'high': 20},  # ASSUMPTION
    'avg_fare_dkk': 200,                # ASSUMPTION (published 10 km/12 min trip = DKK227, E-015)
    'trips_per_active_rider_year': 24,  # ASSUMPTION: two rides a month
    'first_to_active_ratio': 1.5,       # ASSUMPTION: churn allowance
    'dooh_cpm_dkk': 191,                # E-029 (AFA Decaux Digital Copenhagen rate card)
    'dooh_impressions': 20_000_000,     # ASSUMPTION
    'adults_copenhagen': 72_396 + 269_277 + 143_668 + 74_728,  # E-031 bands (18+)
    'core_25_44': 269_277,              # E-031
}

BUDGET = [  # DKK million; ASSUMPTION allocations, objective-and-task
    ('Search & app ads', 7.0),
    ('Social', 6.0),
    ('City screens & video', 5.0),
    ('Rider incentives', 4.6),
    ('Team & creative', 2.4),
    ('B2B sales', 2.0),
    ('CRM & research', 1.0),
    ('Contingency', 2.0),
]
GATES = {'M3 test': 4.5, 'M4 cumulative cap': 7.5, 'M6 cumulative cap': 13.5,
         'M7-12 scale release': 14.5, 'contingency held': 2.0}
KPI = {
    'first_paid_riders_m12': 150_000, 'first_paid_riders_m4': 25_000, 'first_paid_riders_m6': 55_000,
    'paid_trips_year1': 2_500_000, 'trips_per_car_day_m6': 10, 'trips_per_car_day_avg_year1': 15,  # plan average; M6 value is a release floor
    'repeat_90d_m6': 0.35, 'repeat_90d_m12': 0.50,
    'media_cac_cap_m4_m6': 120, 'media_cac_cap_m12': 100,
    'aided_awareness_m12': 0.50, 'business_accounts_m12': 100,
}


def main():
    out = {'assumptions': A, 'budget_dkk_m': dict(BUDGET), 'gates_dkk_m': GATES, 'kpi': KPI}
    total = round(sum(v for _, v in BUDGET), 3)
    shares = {k: round(v / total * 100) for k, v in BUDGET}
    s = {}
    for name, tpd in A['trips_per_car_day'].items():
        trips = A['avg_active_cars_year1'] * tpd * 365
        rev = trips * A['avg_fare_dkk']
        s[name] = {'trips': trips, 'revenue_dkk_m': round(rev / 1e6, 1),
                   'budget_share_of_revenue_pct': round(total * 1e6 / rev * 100, 1),
                   'old_600k_share_pct': round(600_000 / rev * 100, 2)}
    base_trips = s['base']['trips']
    active = base_trips / A['trips_per_active_rider_year']
    media = dict(BUDGET)['Search & app ads'] + dict(BUDGET)['Social']
    checks = {
        'budget_total_30': total == 30.0,
        'shares_sum_100': sum(shares.values()) == 100,
        'gates_reconcile': round(GATES['M6 cumulative cap'] + GATES['M7-12 scale release'] + GATES['contingency held'], 3) == total,
        'gate_order': GATES['M3 test'] < GATES['M4 cumulative cap'] < GATES['M6 cumulative cap'],
        'trips_target_matches_base': abs(KPI['paid_trips_year1'] - base_trips) / base_trips < 0.03,
        'm6_floor_below_plan_average': KPI['trips_per_car_day_m6'] < KPI['trips_per_car_day_avg_year1'] == A['trips_per_car_day']['base'],
        'media_cac_m12_dkk': round(media * 1e6 / KPI['first_paid_riders_m12'], 1),
        'media_cac_within_cap': media * 1e6 / KPI['first_paid_riders_m12'] <= KPI['media_cac_cap_m12'],
        'all_in_cost_per_first_rider_dkk': round(total * 1e6 / KPI['first_paid_riders_m12']),
        'incentive_ceiling_dkk_m': round(KPI['first_paid_riders_m12'] * 30 / 1e6, 2),
        'incentive_ceiling_within_line': KPI['first_paid_riders_m12'] * 30 / 1e6 <= dict(BUDGET)['Rider incentives'],
        'dooh_cost_dkk_m': round(A['dooh_impressions'] / 1000 * A['dooh_cpm_dkk'] / 1e6, 2),
        'dooh_within_brand_line': A['dooh_impressions'] / 1000 * A['dooh_cpm_dkk'] / 1e6 <= dict(BUDGET)['City screens & video'],
        'active_riders_base': round(active),
        'first_riders_base': round(active * A['first_to_active_ratio']),
        'first_rider_target_matches_base': abs(KPI['first_paid_riders_m12'] - active * A['first_to_active_ratio']) / KPI['first_paid_riders_m12'] < 0.05,
        'active_share_of_core_25_44_pct': round(active / A['core_25_44'] * 100, 1),
        'active_share_of_copenhagen_adults_pct': round(active / A['adults_copenhagen'] * 100, 1),
        'fleet_capacity_590_at_15_per_day': A['registered_cars'] * 15 * 365,
    }
    out.update({'budget_total_dkk_m': total, 'budget_shares_pct': shares, 'scenarios': s, 'checks': checks})
    ok = all(v for k, v in checks.items() if isinstance(v, bool))
    out['pass'] = ok
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if len(sys.argv) > 1:
        open(sys.argv[1], 'w').write(text)
    print(text)


if __name__ == '__main__':
    main()

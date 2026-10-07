"""Scale-plan numbers for the final poster (D-166), superseding model v01.

Every poster figure in the final version comes from this file. Inputs marked
ASSUMPTION are the group's planning assumptions and are labelled as such on
the poster or in the script; inputs marked with an E-/DK- ID come from
registered evidence.

Changes from v01: the trips target is the M12 annualised run-rate, not a
year-one total; riders follow a monthly cohort model built on the M4/M6/M12
rider targets; the M6 floor counts paid trips a day; DKK1.0M moves from
Social to Team & creative.

Usage: python3 -B poster/scale-plan-v02-2026-10-07-model.py [OUT.json]
"""
import json
import sys

A = {
    'registered_cars': 590,               # E-020 / DK-20
    'cars_in_service_run_rate': 450,      # ASSUMPTION: run-rate base (590 registered = potential capacity)
    'trips_per_car_day': {'low': 10, 'base': 15, 'high': 20},  # ASSUMPTION
    'avg_fare_dkk': 200,                  # ASSUMPTION (published 10 km/12 min trip = DKK227, E-015)
    'regular_share_of_first_riders': 0.5,  # ASSUMPTION, equal to the >=50% 90-day repeat target
    'trips_per_regular_rider_month': 2.7,  # ASSUMPTION
    'first_ride_offer_dkk': (15, 30),     # test arms, one per rider
    'dooh_cpm_dkk': 191,                  # E-029 (AFA Decaux Digital Copenhagen rate card)
    'dooh_impressions': 20_000_000,       # ASSUMPTION
    'adults_copenhagen': 72_396 + 269_277 + 143_668 + 74_728,  # E-031 bands (18+)
    'core_25_44': 269_277,                # E-031
    'days_per_month': 365 / 12,
}

BUDGET = [  # DKK million; ASSUMPTION allocations, objective-and-task
    ('Search & app ads', 7.0),
    ('Social', 5.0),
    ('City screens & video', 5.0),
    ('Rider incentives', 4.6),
    ('Team & creative', 3.4),
    ('B2B sales', 2.0),
    ('CRM & research', 1.0),
    ('Contingency', 2.0),
]
GATES = {'M3 test': 4.5, 'M4 cumulative cap': 7.5, 'M6 cumulative cap': 13.5,
         'M7-12 scale release': 14.5, 'contingency held': 2.0}
KPI = {
    'first_paid_riders_m12': 150_000, 'first_paid_riders_m4': 25_000, 'first_paid_riders_m6': 55_000,
    'paid_trips_run_rate_m12': 2_500_000, 'paid_trips_per_day_m6_floor': 2_500,
    'repeat_90d_m6': 0.35, 'repeat_90d_m12': 0.50,
    'media_cac_cap_m4_m6': 120, 'media_cac_cap_m12': 100,
    'aided_awareness_m12': 0.50, 'business_accounts_m12': 100,
}


def cohorts():
    """First paid riders by month, spread evenly inside each gate phase."""
    k = KPI
    return ([k['first_paid_riders_m4'] / 4] * 4
            + [(k['first_paid_riders_m6'] - k['first_paid_riders_m4']) / 2] * 2
            + [(k['first_paid_riders_m12'] - k['first_paid_riders_m6']) / 6] * 6)


def daily_trips(adds, month):
    """Paid trips a day in a month (1-12): regular riders acquired so far plus that month's first rides."""
    regular = sum(adds[:month]) * A['regular_share_of_first_riders']
    return (regular * A['trips_per_regular_rider_month'] + adds[month - 1]) / A['days_per_month']


def main():
    out = {'assumptions': A, 'budget_dkk_m': dict(BUDGET), 'gates_dkk_m': GATES, 'kpi': KPI}
    b = dict(BUDGET)
    total = round(sum(b.values()), 3)
    shares = {k: round(v / total * 100) for k, v in BUDGET}
    scen = {}
    for name, tpd in A['trips_per_car_day'].items():
        trips = A['cars_in_service_run_rate'] * tpd * 365
        rev = trips * A['avg_fare_dkk']
        scen[name] = {'run_rate_trips': trips, 'run_rate_revenue_dkk_m': round(rev / 1e6, 1),
                      'budget_share_of_run_rate_revenue_pct': round(total * 1e6 / rev * 100, 1)}
    adds = cohorts()
    share, per_month = A['regular_share_of_first_riders'], A['trips_per_regular_rider_month']
    year1 = sum(a + a * share * per_month * (11 - m + 0.5) for m, a in enumerate(adds))
    run_rate_m12 = daily_trips(adds, 12) * 365
    m6_day = daily_trips(adds, 6)
    regular_m12 = KPI['first_paid_riders_m12'] * share
    media = b['Search & app ads'] + b['Social']
    lo, hi = A['first_ride_offer_dkk']
    checks = {
        'budget_total_30': total == 30.0,
        'shares_sum_100': sum(shares.values()) == 100,
        'gates_reconcile': round(GATES['M6 cumulative cap'] + GATES['M7-12 scale release'] + GATES['contingency held'], 3) == total,
        'gate_order': GATES['M3 test'] < GATES['M4 cumulative cap'] < GATES['M6 cumulative cap'],
        'run_rate_target_matches_base_case': abs(KPI['paid_trips_run_rate_m12'] - scen['base']['run_rate_trips']) / KPI['paid_trips_run_rate_m12'] < 0.03,
        'cohort_run_rate_m12': round(run_rate_m12),
        'cohort_run_rate_supports_target': run_rate_m12 >= KPI['paid_trips_run_rate_m12'],
        'cohort_trips_per_day_m12': round(run_rate_m12 / 365),
        'cohort_trips_per_car_day_m12_at_450': round(run_rate_m12 / 365 / A['cars_in_service_run_rate'], 1),
        'cohort_trips_per_day_m6': round(m6_day),
        'm6_floor_below_cohort_path': KPI['paid_trips_per_day_m6_floor'] < m6_day,
        'year_one_trips_plan_riders': round(year1),
        'year_one_revenue_dkk_m': round(year1 * A['avg_fare_dkk'] / 1e6, 1),
        'budget_share_of_year_one_revenue_pct': round(total * 1e6 / (year1 * A['avg_fare_dkk']) * 100, 1),
        'budget_share_of_run_rate_revenue_pct': scen['base']['budget_share_of_run_rate_revenue_pct'],
        'regular_riders_m12': round(regular_m12),
        'regular_share_of_25_44_pct': round(regular_m12 / A['core_25_44'] * 100, 1),
        'regular_share_of_copenhagen_adults_pct': round(regular_m12 / A['adults_copenhagen'] * 100, 1),
        'regular_share_within_repeat_target': share <= KPI['repeat_90d_m12'],
        'media_cac_m12_dkk': round(media * 1e6 / KPI['first_paid_riders_m12'], 1),
        'media_cac_within_cap': media * 1e6 / KPI['first_paid_riders_m12'] <= KPI['media_cac_cap_m12'],
        'all_in_cost_per_first_rider_dkk': round(total * 1e6 / KPI['first_paid_riders_m12']),
        'incentive_ceiling_dkk_m': round(KPI['first_paid_riders_m12'] * hi / 1e6, 2),
        'incentive_ceiling_within_line': KPI['first_paid_riders_m12'] * hi / 1e6 <= b['Rider incentives'],
        'incentive_expected_dkk_m': round(KPI['first_paid_riders_m12'] * (lo + hi) / 2 / 1e6, 3),
        'referral_headroom_at_expected_dkk_m': round(b['Rider incentives'] - KPI['first_paid_riders_m12'] * (lo + hi) / 2 / 1e6, 3),
        'dooh_cost_dkk_m': round(A['dooh_impressions'] / 1000 * A['dooh_cpm_dkk'] / 1e6, 2),
        'dooh_within_screens_line': A['dooh_impressions'] / 1000 * A['dooh_cpm_dkk'] / 1e6 <= b['City screens & video'],
    }
    out.update({'budget_total_dkk_m': total, 'budget_shares_pct': shares, 'scenarios': scen,
                'cohort_first_riders_by_month': [round(a) for a in adds], 'checks': checks})
    out['pass'] = all(v for v in checks.values() if isinstance(v, bool))
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if len(sys.argv) > 1:
        open(sys.argv[1], 'w').write(text)
    print(text)


if __name__ == '__main__':
    main()

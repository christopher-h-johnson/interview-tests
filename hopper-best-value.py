import itertools as it
from unittest import TestCase

packages = [
    {
        'name': 'seat',
        'value': 30,
        'cost': 15
    },
    {
        'name': 'luggage',
        'value': 100,
        'cost': 65
    },
    {
        'name': 'meal',
        'value': 30,
        'cost': 10
    },
    {
        'name': 'legroom',
        'value': 30,
        'cost': 20
    }
]


def get_combinations(pkgs):
    names = [o['name'] for o in pkgs]

    name_combinations = []
    for r in range(1, len(names) + 1):
        name_combinations += it.combinations(names, r)
    return name_combinations


def get_best_value(pkgs, budget: int):
    combination_aggs = []

    name_combinations = get_combinations(pkgs)
    for c in name_combinations:
        sum_values = 0
        sum_costs = 0
        for p in pkgs:
            if p['name'] in c:
                sum_values += p['value']
                sum_costs += p['cost']
                combination_aggs.append({'costs': sum_costs, 'values': sum_values, 'combination': c})

    aggs_filtered = ([agg for agg in combination_aggs if agg['costs'] < budget])
    best_combination = max(aggs_filtered, key=lambda agg: agg['values'])

    return best_combination['combination'], best_combination['costs'], best_combination['values']


class Test(TestCase):
    def test_best_value(self):
        results = get_best_value(packages, 85)
        assert (results[0] == ('seat', 'luggage'))
        print(
            f"highest value combination is {results[0]} with cost {results[1]} and value {results[2]}")

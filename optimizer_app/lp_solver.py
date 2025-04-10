from pulp import LpProblem, LpVariable, LpMaximize

COTTON_GRADE_FACTORS = {
    'A': {'efficiency': 1.0, 'cost_multiplier': 1.0},
    'B': {'efficiency': 0.9, 'cost_multiplier': 0.95},
    'C': {'efficiency': 0.8, 'cost_multiplier': 0.9},
}

def optimize_production(inputs):
    x = LpVariable("yarn_units", lowBound=0, cat='Integer')

    grade_factors = COTTON_GRADE_FACTORS[inputs['cotton_grade']]

    base_labor = 97 / 22500
    base_power = 21600 / 22500
    base_cost = (172800 + 250000 + 22500) / 22500  # ~20.35 Rs/kg
    machine_capacity = 9750

    labor_per_unit = base_labor / grade_factors['efficiency']
    power_per_unit = base_power / grade_factors['efficiency']
    cost_per_unit = base_cost * grade_factors['cost_multiplier']
    capacity = machine_capacity * grade_factors['efficiency']

    model = LpProblem("Cotton-Yarn-Optimization", LpMaximize)
    if inputs['optimize_for'] == 'profit':
        model += inputs['selling_price'] * x - cost_per_unit * x
    else:
        model += x

    model += labor_per_unit * x <= inputs['available_labor']
    model += x <= capacity

    model.solve()

    x_val = x.varValue

    stages = {
        'Carding': {'wages': 1200, 'power': 2534.4, 'maint': 50000, 'prod': 12000},
        'Draw Frame': {'wages': 2400, 'power': 307.2, 'maint': 35000, 'prod': 11500},
        'Speed Frame': {'wages': 5400, 'power': 2304, 'maint': 50000, 'prod': 11000},
        'Ring Frame': {'wages': 22500, 'power': 21600, 'maint': 300000, 'prod': 10000},
        'Auto Coner': {'wages': 14400, 'power': 2880, 'maint': 250000, 'prod': 9750},
    }

    cost_breakdown = {}
    for name, data in stages.items():
        cost_per_kg = (data['wages'] + data['power'] + (data['maint'] / 30)) / data['prod']
        cost_breakdown[name] = round(cost_per_kg, 2)

    return {
        'status': model.status,
        'production': x_val,
        'profit': (inputs['selling_price'] * x_val - cost_per_unit * x_val)
                  if inputs['optimize_for'] == 'profit' else None,
        'power_consumed': power_per_unit * x_val,
        'cost_breakdown': cost_breakdown
    }

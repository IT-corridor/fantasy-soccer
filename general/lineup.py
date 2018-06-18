from ortools.linear_solver import pywraplp

from general.models import *


class Roster:
    POSITION_ORDER = {
        "F": 0,
        "M": 1,
        "D": 2,
        "GK": 3
    }

    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def spent(self):
        return sum(map(lambda x: x.salary, self.players))

    def projected(self):
        return sum(map(lambda x: x.points, self.players))

    def position_order(self, player):
        return self.POSITION_ORDER[player.position]

    def sorted_players(self):
        return sorted(self.players, key=self.position_order)

    def __repr__(self):
        s = '\n'.join(str(x) for x in self.sorted_players())
        s += "\n\nProjected Score: %s" % self.projected()
        s += "\tCost: $%s" % self.spent()
        return s


POSITION_LIMITS = [
    ["F", 2, 2],
    ["M", 3, 3],
    ["D", 2, 2],
    ["GK", 1, 1]
]

ROSTER_SIZE = 8


def get_lineup(players, SALARY_CAP, MAX_POINT):
    solver = pywraplp.Solver('FanDuel-FIFA-2018', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    variables = []

    for player in players:
        variables.append(solver.IntVar(0, 1, str(player.name)))

    objective = solver.Objective()
    objective.SetMaximization()

    for i, player in enumerate(players):
        objective.SetCoefficient(variables[i], player.points)

    salary_cap = solver.Constraint(0, SALARY_CAP)
    for i, player in enumerate(players):
        salary_cap.SetCoefficient(variables[i], player.salary)

    point_cap = solver.Constraint(0, MAX_POINT)
    for i, player in enumerate(players):
        point_cap.SetCoefficient(variables[i], player.points)

    for position, min_limit, max_limit in POSITION_LIMITS:
        position_cap = solver.Constraint(min_limit, max_limit)

        for i, player in enumerate(players):
            if position == player.position:
                position_cap.SetCoefficient(variables[i], 1)

    size_cap = solver.Constraint(ROSTER_SIZE, ROSTER_SIZE)
    for variable in variables:
        size_cap.SetCoefficient(variable, 1)

    solution = solver.Solve()

    if solution == solver.OPTIMAL:
        roster = Roster()

        for i, player in enumerate(players):
            if variables[i].solution_value() == 1:
                roster.add_player(player)

        print "Optimal roster for: $%s\n" % SALARY_CAP
        print roster
        return roster
    else:
        print "No solution :("


def calc_lineups(players, num_lineups):
    result = []
    SALARY_CAP = 60000
    MAX_POINT = 10000
    for i in range(num_lineups):
        roster = get_lineup(players, SALARY_CAP, MAX_POINT)
        result.append(roster)
        MAX_POINT = roster.projected() - 0.001
    return result
import itertools

def calculate_N_payoffs(player_index: int, payoff_table: dict[tuple, tuple], mixed_strategies: list[dict], decimals: int = 2):
    players = range(len(mixed_strategies))
    all_strategies = [list(mixed_strategies[i].keys()) for i in players]

    expected_payoff = 0.0

    for profile in itertools.product(*all_strategies):
        print(profile)

        prob = 1.0
        for i, action in enumerate(profile):
            prob *= mixed_strategies[i][action]
        payoff = payoff_table[profile][player_index]
        expected_payoff += prob * payoff

    return round(expected_payoff, decimals)

def test_calc_N_payoffs():
    payoff_table = {
        ('A1', 'B1'): (2, 3),
        ('A1', 'B2'): (0, 5),
        ('A2', 'B1'): (1, 1),
        ('A2', 'B2'): (4, 2),
    }

    mixed_strategies = [
        {'A1': 0, 'A2': 1},  # Player 1 (pure strategy)
        {'B1': 0.3, 'B2': 0.7},  # Player 2
    ]

    print(calculate_N_payoffs(0, payoff_table, mixed_strategies))  # Player 1's expected payoff

# if __name__ == "__main__":
#     test_calc_N_payoffs()
import pandas as pd
import matplotlib.pyplot as plt

# Define the payoff matrix for Prisoner's Dilemma
strategies_p1 = ['C', 'D']
strategies_p2 = ['C', 'D']

payoff_matrix = {
    ('C', 'C'): (5, 5),
    ('C', 'D'): (0, 20),
    ('D', 'C'): (20, 0),
    ('D', 'D'): (1, 1),
}

# Convert to DataFrame
df = pd.DataFrame([[payoff_matrix[(r, c)] for c in strategies_p2] for r in strategies_p1],
                  index=strategies_p1, columns=strategies_p2)


def print_payoff_matrix(df):
    print("Payoff Matrix (Player 1 payoff, Player 2 payoff):")
    formatted = df.apply(lambda col: col.map(str))
    print(formatted.to_string())
    print()

    # Display nicely formatted table using matplotlib
    fig, ax = plt.subplots()
    ax.axis('off')
    table_data = [[str(cell) for cell in row] for row in df.values]
    col_labels = df.columns.tolist()
    row_labels = df.index.tolist()

    table = ax.table(cellText=table_data,
                     rowLabels=row_labels,
                     colLabels=col_labels,
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.5, 1.5)

    plt.title("Prisoner's Dilemma Payoff Matrix")
    plt.show()


def check_dominance(player, df, mode='strict', ignore_strategies=None):
    if ignore_strategies is None:
        ignore_strategies = set()

    strategies = df.index if player == 1 else df.columns
    dominated = set()
    relation = "strictly" if mode == 'strict' else "weakly"

    for s1 in strategies:
        if s1 in ignore_strategies:
            continue  # Skip already dominated strategies

        for s2 in strategies:
            if s1 == s2:
                continue

            if player == 1:
                s1_payoffs = [df.loc[s1, c][0] for c in df.columns]
                s2_payoffs = [df.loc[s2, c][0] for c in df.columns]
            else:
                s1_payoffs = [df.loc[r, s1][1] for r in df.index]
                s2_payoffs = [df.loc[r, s2][1] for r in df.index]

            if mode == 'strict':
                if all(p2 > p1 for p1, p2 in zip(s1_payoffs, s2_payoffs)):
                    print(f"{s1} is {relation} dominated by {s2} (Player {player})")
                    dominated.add(s1)
                    break
            elif mode == 'weak':
                if all(p2 >= p1 for p1, p2 in zip(s1_payoffs, s2_payoffs)) and any(p2 > p1 for p1, p2 in zip(s1_payoffs, s2_payoffs)):
                    print(f"{s1} is {relation} dominated by {s2} (Player {player})")
                    dominated.add(s1)
                    break

    return dominated


def best_responses(player, df):
    best_resp = {}
    if player == 1:
        for col in df.columns:
            payoffs = {row: df.loc[row, col][0] for row in df.index}
            max_payoff = max(payoffs.values())
            best_resp[col] = [s for s, p in payoffs.items() if p == max_payoff]
    else:
        for row in df.index:
            payoffs = {col: df.loc[row, col][1] for col in df.columns}
            max_payoff = max(payoffs.values())
            best_resp[row] = [s for s, p in payoffs.items() if p == max_payoff]
    return best_resp


def rationalizable_strategies(df):
    df_rat = df.copy()
    while True:
        strict_dom_p1 = check_dominance(1, df_rat, 'strict')
        strict_dom_p2 = check_dominance(2, df_rat, 'strict')

        if strict_dom_p1 or strict_dom_p2:
            if strict_dom_p1:
                df_rat = df_rat.drop(index=strict_dom_p1)
            if strict_dom_p2:
                df_rat = df_rat.drop(columns=strict_dom_p2)
            continue

        weak_dom_p1 = check_dominance(1, df_rat, 'weak', ignore_strategies=strict_dom_p1)
        weak_dom_p2 = check_dominance(2, df_rat, 'weak', ignore_strategies=strict_dom_p2)

        if weak_dom_p1 or weak_dom_p2:
            if weak_dom_p1:
                df_rat = df_rat.drop(index=weak_dom_p1)
            if weak_dom_p2:
                df_rat = df_rat.drop(columns=weak_dom_p2)
            continue

        break

    return df_rat



print_payoff_matrix(df)

print("Checking Strict Dominance...")
strict_dom_p1 = check_dominance(1, df, 'strict')
strict_dom_p2 = check_dominance(2, df, 'strict')

print("\nChecking Weak Dominance...")
weak_dom_p1 = check_dominance(1, df, 'weak', ignore_strategies=strict_dom_p1)
weak_dom_p2 = check_dominance(2, df, 'weak', ignore_strategies=strict_dom_p2)

print("\nBest Responses:")
br1 = best_responses(1, df)
br2 = best_responses(2, df)
print("Player 1:", br1)
print("Player 2:", br2)

print("\nRationalizable Strategies (Remaining Matrix):")
rat_df = rationalizable_strategies(df)
print_payoff_matrix(rat_df)
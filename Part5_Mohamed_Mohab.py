import pandas as pd
import matplotlib.pyplot as plt

strategies_p1 = ['C', 'D']
strategies_p2 = ['C', 'D']

payoff_matrix = {
    ('C', 'C'): (5, 5),
    ('C', 'D'): (0, 20),
    ('D', 'C'): (20, 0),
    ('D', 'D'): (1, 1),
}

df = pd.DataFrame([[payoff_matrix[(r, c)] for c in strategies_p2] for r in strategies_p1],
                  index=strategies_p1, columns=strategies_p2)

fig, ax = plt.subplots()
ax.axis('off')
table_data = [[str(cell) for cell in row] for row in df.values]

table = ax.table(cellText=table_data,
                 rowLabels=df.index,
                 colLabels=df.columns,
                 loc='center',
                 cellLoc='center')

table.scale(1.3, 1.3)
table.set_fontsize(12)
plt.title("Prisoner's Dilemma Payoff Matrix")
plt.show()

def get_best_responses(df, player_index):
    best_responses = set()
    if player_index == 0:  # Player 1
        for col in df.columns:
            col_values = [(row, df.loc[row, col][0]) for row in df.index]
            max_val = max(v for r, v in col_values)
            for r, v in col_values:
                if v == max_val:
                    best_responses.add((r, col))
    else:  # Player 2
        for row in df.index:
            row_values = [(col, df.loc[row, col][1]) for col in df.columns]
            max_val = max(v for c, v in row_values)
            for c, v in row_values:
                if v == max_val:
                    best_responses.add((row, c))
    return best_responses

def find_nash_equilibria(df):
    p1_br = get_best_responses(df, player_index=0)
    p2_br = get_best_responses(df, player_index=1)
    nash_eq = p1_br.intersection(p2_br)
    return nash_eq

nash_eqs = find_nash_equilibria(df)

print("=== Nash Equilibria ===")
if nash_eqs:
    for eq in nash_eqs:
        print(f"Strategy: Player 1 = {eq[0]}, Player 2 = {eq[1]}, Payoff = {df.loc[eq[0], eq[1]]}")
else:
    print("No pure strategy Nash Equilibrium found.")

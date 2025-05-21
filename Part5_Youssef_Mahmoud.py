import matplotlib.pyplot as plt

# Define the payoff matrix
payoff_matrix = {
    ('C', 'C'): (5, 5),
    ('C', 'D'): (0, 20),
    ('D', 'C'): (20, 0),
    ('D', 'D'): (1, 1),
}

# Players' actions
actions = ['C', 'D']

# Find pure strategy Nash equilibriam
def find_nash_equilibrium(matrix):
    nash_equilibriam = []
    for a1 in actions:
        for a2 in actions:
            p1_payoff = matrix[(a1, a2)][0]
            p2_payoff = matrix[(a1, a2)][1]

            # Check if Player 1 can't improve
            p1_best = all(p1_payoff >= matrix[(alt, a2)][0] for alt in actions)

            # Check if Player 2 can't improve
            p2_best = all(p2_payoff >= matrix[(a1, alt)][1] for alt in actions)

            if p1_best and p2_best:
                nash_equilibriam.append((a1, a2))

    return nash_equilibriam

# Find Nash equilibrium(s)
nash_equilibriam = find_nash_equilibrium(payoff_matrix)
print("Nash Equilibriam:", nash_equilibriam)

# Create a figure for the table
fig, ax = plt.subplots()
ax.set_axis_off()
ax.set_title("Prisoner's Dilemma", fontweight="bold")

# Create the data grid for the table
cell_text = []
row_labels = []
for row_action in actions:
    row = []
    row_labels.append(row_action)
    for col_action in actions:
        row.append(str(payoff_matrix[(row_action, col_action)]))
    cell_text.append(row)

# Create the table
table = ax.table(
    cellText=cell_text,
    rowLabels=row_labels,
    colLabels=actions,
    cellLoc='center',
    loc='center'
)

# Format the table
table.scale(1.5, 1.5)
table.auto_set_font_size(False)
table.set_fontsize(12)

# Highlight Nash equilibrium cells
for eq in nash_equilibriam:
    row_idx = actions.index(eq[0]) + 1  # table rows start at 1 (after header)
    col_idx = actions.index(eq[1])
    cell_pos = (row_idx, col_idx)
    cell = table.get_celld().get(cell_pos)
    if cell:
        cell.set_facecolor('#FFCCCC')     # light red
        cell.set_edgecolor('red')
        cell.set_linewidth(2)
        cell.set_fontsize(13)
        cell.set_text_props(weight='bold')
    else:
        print(f"Cell {cell_pos} not found!")

# Show the plot
plt.tight_layout()
plt.show()

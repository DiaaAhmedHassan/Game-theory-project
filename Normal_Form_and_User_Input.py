import pandas as pd
import matplotlib.pyplot as plt

# Prisoner's Dilemma Game Data
strategies_p1 = ['C', 'D']
strategies_p2 = ['C', 'D']

# Payoff matrix for each strategy combination
payoff_matrix = {
    ('C', 'C'): (5, 5),
    ('C', 'D'): (0, 20),
    ('D', 'C'): (20, 0),
    ('D', 'D'): (1, 1),
}

# Build the DataFrame
data = []
for p1 in strategies_p1:
    
    row = []
    for p2 in strategies_p2:
        row.append(payoff_matrix[(p1, p2)])
    data.append(row)

df = pd.DataFrame(data, columns=strategies_p2, index=strategies_p1)
df.index.name = "Player 1"
df.columns.name = "Player 2"

# Print the matrix
print("Prisoner's Dilemma (Normal Form):\n", df)

# Display the matrix as a table
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
table.scale(1.2, 1.2)
table.auto_set_font_size(False)
table.set_fontsize(12)
plt.title("Prisoner's Dilemma")
plt.show()

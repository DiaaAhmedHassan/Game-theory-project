import networkx as nx
import numpy as np
import matplotlib.pyplot as plt



class Games:

    def plot_tree(self, tree, pos, node_labels, highlight_path=None):
        # Draw all edges in default color
        nx.draw(tree, pos, with_labels=False, node_color='lightgreen', node_size=2000, arrows=True)
        nx.draw_networkx_labels(tree, pos, labels=node_labels)

        # Draw all edge labels
        edge_labels = {(u, v): d['action'] for u, v, d in tree.edges(data=True)}
        nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels)

        # Highlight the selected path in red if provided
        if highlight_path:
            nx.draw_networkx_edges(
                tree, pos,
                edgelist=highlight_path,
                edge_color='red',
                width=2,
                arrows=True
            )

        plt.title("Game tree")
        plt.axis('off')
        plt.show()
    
    def add_labels(self, game_tree):
        node_labels = {}
        for node, attr in game_tree.nodes(data=True):
            if 'payoff' in attr:
                node_labels[node] = f"{node}\nPayoff:{attr['payoff']}"
            elif 'player' in attr:
                node_labels[node] = f"{node}\n({attr['player']})"
            else:
                node_labels[node] = node
        return node_labels


    def build_prisoners_dilemma(self, p1_decision, p2_decision, show_plot=False):
        game_tree = nx.DiGraph()

        # create nodes
        game_tree.add_node("Start", player='p1', label='Start')
        game_tree.add_node('p1_c', player='p2')
        game_tree.add_node('p1_d', player='p2')

        # add edges between previous nodes
        game_tree.add_edge('Start', 'p1_c', action='c')
        game_tree.add_edge('Start', 'p1_d', action='d')

        game_tree.add_node('cc', payoff=(5, 5))
        game_tree.add_node('cd', payoff=(0, 20))
        game_tree.add_node('dc', payoff=(20, 0))
        game_tree.add_node('dd', payoff=(1, 1))

        # add edges
        game_tree.add_edge('p1_c', 'cc', action='c')
        game_tree.add_edge('p1_c', 'cd', action='d')
        game_tree.add_edge('p1_d', 'dc', action='c')
        game_tree.add_edge('p1_d', 'dd', action='d')

        node_labels = Games().add_labels(game_tree)
        
        pos = {
            "Start": (0, 2),
            "p1_c": (-1.5, 1),
            "p1_d": (1.5, 1),
            "cc": (-2, 0),
            "cd": (-1, 0),
            "dc": (1, 0),
            "dd": (2, 0),
        }


        # Determine the path to highlight based on decisions
        highlight_path = []
        if p1_decision == 'c':
            highlight_path.append(('Start', 'p1_c'))
            if p2_decision == 'c':
                highlight_path.append(('p1_c', 'cc'))
            elif p2_decision == 'd':
                highlight_path.append(('p1_c', 'cd'))
        elif p1_decision == 'd':
            highlight_path.append(('Start', 'p1_d'))
            if p2_decision == 'c':
                highlight_path.append(('p1_d', 'dc'))
            elif p2_decision == 'd':
                highlight_path.append(('p1_d', 'dd'))

        if show_plot:
            Games().plot_tree(game_tree, pos, node_labels, highlight_path=highlight_path)

        if p1_decision == 'c' and p2_decision == 'c':
            return (5, 5)
        elif p1_decision == 'c' and p2_decision == 'd':
            return (0, 20)
        elif p1_decision == 'd' and p2_decision == 'c':
            return (20, 0)
        elif p1_decision == 'd' and p2_decision == 'd':
            return (1, 1)
        
    
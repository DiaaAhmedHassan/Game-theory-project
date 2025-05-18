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

    def build_game_tree(self, nodes, edges):
            game_tree = nx.DiGraph()
            for node, attrs in nodes:
                game_tree.add_node(node, **attrs)
                for u, v, attrs in edges:
                    game_tree.add_edge(u, v, **attrs)
            return game_tree

    def build_prisoners_dilemma(self, p1_decision, p2_decision, show_plot=False):
        

        # create nodes
        nodes = [
            ("Start", {'player': 'p1', 'label': 'Start'}),
            ('p1_c', {'player': 'p2'}),
            ('p1_d', {'player': 'p2'}),
            ('cc', {'payoff': (5, 5)}),
            ('cd', {'payoff': (0, 20)}),
            ('dc', {'payoff': (20, 0)}),
            ('dd', {'payoff': (1, 1)}),
        ]
        edges = [
            ('Start', 'p1_c', {'action': 'c'}),
            ('Start', 'p1_d', {'action': 'd'}),
            ('p1_c', 'cc', {'action': 'c'}),
            ('p1_c', 'cd', {'action': 'd'}),
            ('p1_d', 'dc', {'action': 'c'}),
            ('p1_d', 'dd', {'action': 'd'}),
        ]
        game_tree = self.build_game_tree(nodes, edges)
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
        
    def build_battle_of_sexes(self, m, w, show_plot = False):
        nodes = [
            ('Start', {'player': 'm', 'label': 'Start'}), 
            ('m_f', {'player': 'w'}),
            ('m_b', {'player': 'w'}), 
            ('ff', {'payoff': (3, 2)}), 
            ('fb', {'payoff': (0, 0)}), 
            ('bf', {'payoff': (0, 0)}), 
            ('bb', {'payoff': (2, 3)}), 
        ]

        edges = [
            ('Start', 'm_f', {'action': 'f'}), 
            ('Start', 'm_b', {'action': 'b'}), 
            ('m_f', 'ff', {'action': 'f'}), 
            ('m_f', 'fb', {'action': 'b'}), 
            ('m_b', 'bf', {'action': 'f'}), 
            ('m_b', 'bb', {'action': 'b'}), 
        ]

        game_tree = self.build_game_tree(nodes, edges)


        node_labels = Games().add_labels(game_tree)

        pos = {
            "Start": (0, 2),
            "m_f": (-1.5, 1),
            "m_b": (1.5, 1),
            "ff": (-2, 0),
            "fb": (-1, 0),
            "bf": (1, 0),
            "bb": (2, 0),
        }

        highlight_path = []
        if m == 'f':
            highlight_path.append(('Start', 'm_f'))
            if w == 'f':
                highlight_path.append(('m_f', 'ff'))
            elif w == 'd':
                highlight_path.append(('m_f', 'fb'))
        elif m == 'd':
            highlight_path.append(('Start', 'm_b'))
            if w == 'c':
                highlight_path.append(('m_b', 'bf'))
            elif m == 'd':
                highlight_path.append(('m_b', 'bb'))
                
        if show_plot:
            Games().plot_tree(game_tree, pos, node_labels, highlight_path=highlight_path)

        if m=='f' and w=='f':
            return (3, 2)
        elif m=='f' and w=='b':
            return (0, 0)
        elif m=='b' and w=='f':
            return (0, 0)
        elif m=='b' and w=='b':
            return (2, 3)
    
    def build_matching_pennies(self, p1, p2, show_plot):
        
        nodes = [
            ('Start', {'player': 'p1', 'label': 'Start'}), 
            ('p1_h', {'player': 'p2'}), 
            ('p1_t', {'player': 'p2'}), 
            ('hh', {'payoff': (1, -1)}), 
            ('ht', {'payoff': (-1, 1)}), 
            ('th', {'payoff': (-1, 1)}), 
            ('tt', {'payoff': (1, -1)}), 
        ]

        edges = [
            ('Start', 'p1_h', {'action': 'h'}), 
            ('Start', 'p1_t', {'action': 't'}), 
            ('p1_h', 'hh', {'action': 'h'}),
            ('p1_h', 'ht', {'action': 't'}),
            ('p1_t', 'th', {'action': 'h'}),
            ('p1_t', 'tt', {'action': 't'}),
        ]

        game_tree = self.build_game_tree(nodes, edges)

        node_labels = self.add_labels(game_tree)

        pos = {
            "Start": (0, 2),
            "p1_h": (-1.5, 1),
            "p1_t": (1.5, 1),
            "hh": (-2, 0),
            "ht": (-1, 0),
            "th": (1, 0),
            "tt": (2, 0),
        }

        highlighted_path = []
        if p1 == 'h':
            highlighted_path.append(("Start", "p1_h"))
            if p2== 'h':
                highlighted_path.append(("p1_h", "hh"))
            elif p2 == 't':
                highlighted_path.append(("p1_h", 'ht'))
        elif p1 == 't':
            highlighted_path.append(('Start', 'p1_t'))
            if p2 == 'h':
                highlighted_path.append(("p1_t", 'th'))
            elif p2 == 't':
                highlighted_path.append(("p1_t", 'tt'))
        
        if show_plot:
            Games().plot_tree(game_tree, pos, node_labels, highlighted_path)

        if p1 == 'h' and p2 == 'h':
            return (1, -1)
        elif p1=='h' and p2 == 't':
            return (-1, 1)
        elif p1=='t' and p2 == 'h':
            return (-1, 1)
        elif p1 == 't' and p2=='t':
            return (1, -1)
        
    def build_hawk_dove(self, p1, p2, show_plot = False):

        nodes = [
            ('Start', {'player': 'p1', 'label': 'Start'}), 
            ('p1_h', {'player': 'p2'}),
            ('p1_d', {'player': 'p2'}), 
            ('hh', {'payoff': (-5, -5)}), 
            ('hd', {'payoff': (40, 0)}), 
            ('dh', {'payoff': (0, 40)}), 
            ('dd', {'payoff': (20, 20)})
        ]

        edges = [
            ('Start', 'p1_h', {'action': 'h'}), 
            ('Start', 'p1_d', {'action': 'd'}), 
            ('p1_h', 'hh', {'action': 'h'}), 
            ('p1_h', 'hd', {'action': 'd'}), 
            ('p1_d', 'dh', {'action': 'h'}), 
            ('p1_d', 'dd', {'action': 'd'}), 
        ]

        game_tree = self.build_game_tree(nodes, edges)
        nodes_labels = self.add_labels(game_tree)

        pos = {
            "Start": (0, 2),
            "p1_h": (-1.5, 1),
            "p1_d": (1.5, 1),
            "hh": (-2, 0),
            "hd": (-1, 0),
            "dh": (1, 0),
            "dd": (2, 0),
        }

        highlighted_path = []
        if p1 == 'h':
            highlighted_path.append(('Start', 'p1_h'))
            if p2 == 'h':
                highlighted_path.append(('p1_h', 'hh'))
            elif p2 == 'd':
                highlighted_path.append(('p1_h', 'hd'))
        elif p1 == 'd':
            highlighted_path.append(('Start', 'p1_d'))
            if p2 == 'h':
                highlighted_path.append(('p1_d', 'dh'))
            elif p2 == 'd':
                highlighted_path.append(('p1_d', 'dd'))
        
        if show_plot:
            self.plot_tree(game_tree, pos, nodes_labels, highlighted_path)
        
        if p1 == 'h' and p2 == 'h':
            return (-5, -5)
        elif p1 == 'h' and p2 == 'd':
            return (40, 0)
        elif p1 == 'd' and p2 == 'h':
            return (0, 40)
        elif p1 == 'd' and p2 == 'd':
            return (20, 20)
        

##** use this for user input design

# print("Select game to simulate: ")
# print("Prisoners dilemma (1) \n battle of sexes (2) \n matching penis (3) \n Hawk dove (4) \n")

# selected_game = str(input("Enter your selection: "))

# if selected_game == '1':
#     print("Start prisoner dilemma scenario. ")
#     p1 = str(input("Enter prisoner1 decision: "))
#     p2 = str(input("Enter prisoner2 decision: "))
#     payoff = Games().build_prisoners_dilemma(p1, p2)
#     print(f"The payoff of your scenario: {payoff}")
#     Games().build_prisoners_dilemma(p1, p2, 1)
# elif selected_game == '2':
#     print("Start battle of sexes scenario. ")
#     man = str(input("Enter man decision: "))
#     woman = str(input("Enter woman decision: "))
#     payoff = Games().build_battle_of_sexes(man, woman)
#     print(f"The payoffs of your scenario is: {payoff}")
#     Games().build_battle_of_sexes(man, woman, 1)
# elif selected_game == '3':
#     print("Start matching penis scenario. ")
#     pens1 = str(input("Enter pens 1 (h/t): "))
#     pens2 = str(input("Enter pens 2: (h/t): "))
#     payoff = Games().build_matching_pennies(pens1, pens2)
#     print(f"The payoffs of your scenario is: {payoff}")
#     Games().build_battle_of_sexes(pens1, pens2, 1)
# elif selected_game == '4':
#     print("Start hawk dove scenario. ")
#     p1 = str(input("Enter player1 decision: "))
#     p2 = str(input("Enter player2 decision: "))
#     payoff = Games().build_battle_of_sexes(p1, p2)
#     print(f"The payoffs of your scenario is: {payoff}")
#     Games().build_battle_of_sexes(p1, p2, 1)
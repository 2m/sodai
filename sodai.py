import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

DEADHEAD = {"color": "blue"}
POWER = {"color": "red"}
STRIP_END = {"color": "red", "style": "filled"}
LAST_STRIP_END = {"color": "tomato", "style": "filled"}

node_head = [(1, STRIP_END)]
node_neck = [2, (3, LAST_STRIP_END), 4, 5]
node_hips = [6, (7, STRIP_END), 8, 9, 10, 11, (12, STRIP_END), 13, 14]
node_legs = [(15, STRIP_END), (16, STRIP_END), 17, 18]

edge_neck = [(1, 2), (1, 3, POWER), (1, 4), (1, 5, POWER)]
edge_collar = [
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 2),
    (2, 3, DEADHEAD),
    (4, 5, DEADHEAD),
]

edge_belly = [
    # down from node 2
    (2, 6),
    (2, 7),
    (2, 14),
    (2, 13),
    # down from node 3
    (3, 7, POWER),
    (3, 8),
    (3, 9),
    (3, 14),
    # down from node 4
    (4, 9),
    (4, 10),
    (4, 11),
    (4, 14),
    # down from node 5
    (5, 11),
    (5, 12, POWER),
    (5, 13, POWER),
    (5, 14),
]

edge_belt = [(6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 6)]

edge_cross = [
    (7, 14),
    (9, 14),
    (11, 14),
    (13, 14),
    (7, 14, DEADHEAD),
    (9, 14, DEADHEAD),
    (11, 14, DEADHEAD),
    (13, 14, DEADHEAD),
]

edge_legs = [
    # up from 15
    (15, 6),
    (15, 7),
    (15, 14),
    (15, 13, POWER),
    # up from 16
    (16, 7, POWER),
    (16, 8),
    (16, 9),
    (16, 14),
    # up from 17
    (17, 9),
    (17, 10),
    (17, 11),
    (17, 14),
    # up from 18
    (18, 11),
    (18, 12),
    (18, 13),
    (18, 14),
]

sodas = nx.MultiGraph()

sodas.add_nodes_from(node_head)
sodas.add_nodes_from(node_neck)
sodas.add_nodes_from(node_hips)
sodas.add_nodes_from(node_legs)

sodas.add_edges_from(edge_neck)
sodas.add_edges_from(edge_collar)
sodas.add_edges_from(edge_belly)
sodas.add_edges_from(edge_belt)
sodas.add_edges_from(edge_cross)
sodas.add_edges_from(edge_legs)

print("Nodes:", sodas.number_of_nodes())
print("Edges:", sodas.number_of_edges())

print("Is eulerean:", nx.is_eulerian(sodas))

i = 0
for edge in nx.eulerian_circuit(sodas, keys=True):

    if edge[2] != 1:
        i += 1

    print(edge)

    if i % 10 == 0:
        print("End of a led strip")


viz = to_agraph(sodas)
viz.layout('sfdp')
viz.draw('sodas.png')

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import argparse
import numpy as np
import matplotlib.pyplot as plt

def c(x, y, z):
    return {"coords": np.array([x, y, z])}

DEADHEAD = {"color": "blue"}
POWER = {"color": "red"}
POWER_INJECT = {"color": "red", "style": "filled"}

# 1: 0 1.732 0

# 2: -0.5 0.866  0.5
# 3:  0.5 0.866  0.5
# 4:  0.5 0.866 -0.5
# 5: -0.5 0.866 -0.5

#  6: -1  0  1
#  7:  0  0  1
#  8:  1  0  1
#  9:  1  0  0
# 10:  1  0 -1
# 11:  0  0 -1
# 12: -1  0 -1
# 13: -1  0  0
# 14:  0  0  0

# 15: -0.5 -0.866  0.5
# 16:  0.5 -0.866  0.5
# 17:  0.5 -0.866 -0.5
# 18: -0.5 -0.866 -0.5

node_head = [(1, {**c(0, 1.732, 0), **POWER_INJECT})]
node_neck = [
    (2, c(-0.5, 0.866, 0.5)),
    (3, c(0.5, 0.866, 0.5)),
    (4, c(0.5, 0.866, -0.5)),
    (5, c(-0.5, 0.866, -0.5))]
node_hips = [
    (6, c(-1, 0, 1)),
    (7, c(0, 0, 1)),
    (8, {**c(1, 0, 1), **POWER_INJECT}),
    (9, c(1, 0, 0)),
    (10, c(1, 0, -1)),
    (11, c(0, 0, -1)),
    (12, c(-1, 0, -1)),
    (13, {**c(-1, 0, 0), **POWER_INJECT}),
    (14, c(0, 0, 0))
]
node_legs = [
    (15, c(-0.5, -0.866, 0.5)),
    (16, c(0.5, -0.866, 0.5)),
    (17, c(0.5, -0.866, -0.5)),
    (18, c(-0.5, -0.866, -0.5))
]

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
    (3, 7),
    (3, 8, POWER),
    (3, 9),
    (3, 14),
    # down from node 4
    (4, 9),
    (4, 10),
    (4, 11),
    (4, 14),
    # down from node 5
    (5, 11),
    (5, 12),
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
    (15, 13),
    # up from 16
    (16, 7),
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

def eul_path():
    print("Nodes:", sodas.number_of_nodes())
    print("Edges:", sodas.number_of_edges())

    print("Is eulerean:", nx.is_eulerian(sodas))

    i = 0
    for edge in nx.eulerian_circuit(sodas, keys=True):

        if edge[2] != 1:
            i += 1

        print(edge)

        if i % 18 == 0:
            print("Power here")


def visualize():
    viz = to_agraph(sodas)
    viz.layout('sfdp')
    viz.draw('sodas.png')
    print("Graph visualized in sodas.png")


def coordinates():
    OFFSET = 0.07

    xs = []
    ys = []
    zs = []

    with open('coords.csv', 'w') as coords_file:

        for (start, end, deadhead) in nx.eulerian_circuit(sodas, keys=True):
            if not deadhead:
                start_coord = sodas.nodes[start]["coords"]
                end_coord = sodas.nodes[end]["coords"]

                direction = end_coord - start_coord

                # Sample 27 points along the line
                points = [start_coord + t * direction for t in np.linspace(0 + OFFSET, 1 - OFFSET, 27)]
                for point in points:
                    xs.append(point[0])
                    ys.append(point[1])
                    zs.append(point[2])

                    coords_file.write(f"{point[0]},{point[1]},{point[2]}\n")

    fig = plt.figure()
    viz = fig.add_subplot(projection='3d')
    viz.scatter(xs, ys, zs, marker='o', zdir='y')
    plt.show()


parser = argparse.ArgumentParser(prog='Sodai')
subparsers = parser.add_subparsers(required=True)

parser_eulpath = subparsers.add_parser('eulpath', help='print eulerian path')
parser_eulpath.set_defaults(func=eul_path)

parser_viz = subparsers.add_parser('viz', help='visualize graph')
parser_viz.set_defaults(func=visualize)

parser_coords = subparsers.add_parser('coords', help='print coordinates')
parser_coords.set_defaults(func=coordinates)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func()

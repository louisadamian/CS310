import sys

import networkx as nx
import osm
import plotter
from location_search import get_location_nodes

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) > 2:
        start = sys.argv[1]
        end = sys.argv[2]
    else:
        start = input("please enter your starting location ")
        end = input("please enter your ending location ")
    graph = osm.get_graph()
    start_nodes = get_location_nodes(start, graph)
    end_nodes = get_location_nodes(end, graph)
    print(start_nodes)
    print(end_nodes)
    # TODO: replace this with dijkstra or A*
    path = nx.shortest_path(graph, start_nodes[0], end_nodes[0])
    plotter.plot_route(path, graph, crop_to_route=True, show=True)

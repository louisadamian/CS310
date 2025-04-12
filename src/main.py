import networkx as nx
import numpy as np

import osm
import plotter
from matplotlib import pyplot as plt

if __name__ == "__main__":
    # if sys.argv.__len__() < 2:
    #     start = input("starting location ")
    #     if "," in start:
    #         split_str = ","
    #     else:
    #         split_str = " "
    #     lat0, lon0 = start.split(split_str)
    #     end = input("end location")
    #     if "," in end:
    #         split_str = ","
    #     else:
    #         split_str = " "
    #     lat1, lon1 = end.split()
    # elif sys.argv.__len__() > 3:
    #     lat0 = sys.argv[1]
    #     lon0 = sys.argv[2]
    #     lat1 = sys.argv[3]
    #     lon1 = sys.argv[4]

    graph = osm.get_graph(force_download=True)
    print(f"8566264264 edges {graph.edges(9959766314)}")
    path = nx.astar_path(graph, 12662908164, 12660081417)
    points = []
    print("path: ", path)
    for i in range(1, len(path)):
        points.append(np.array(graph.get_edge_data(path[i - 1], path[i])["points"]))
    plotter.plot_route(points, "", crop_to_route=True)
    plt.show()
    # run astar from start to finish

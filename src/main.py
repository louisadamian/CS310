import networkx as nx
import osm
import plotter

if __name__ == "__main__":
    graph = osm.get_graph(force_download=False)
    # replace this with dijkstra or A*
    path = nx.shortest_path(graph, 7671135318, 12677458704)
    # path = nx.astar_path(graph,  327832796, 9393605759)
    plotter.plot_route(path, graph, crop_to_route=True, show=True)

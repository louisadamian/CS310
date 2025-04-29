import networkx as nx
import osm
import plotter

if __name__ == "__main__":
    graph = osm.get_graph()
    # TODO: replace this with dijkstra or A*
    path = nx.shortest_path(graph, 7671135318, 12677458704)
    plotter.plot_route(path, graph, crop_to_route=True, show=True)

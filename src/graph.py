from src import osm 
# from . import osm
import networkx as nx


def build_osm_graph(remove_component_size: int = 10) -> nx.Graph:
    """
    wrapper function to osm.py
    creates a networkc graph from osm way data
    :param remove_component_size: minimum number of nodes for a connected component to not be removed
    :return: networkx graph object with node IDs and weighted edges
    """

    osm_data = osm.get_ways()
    if not osm_data:
        raise ValueError("No osm data")

    graph = osm.convert_ways_to_graph(osm_data, remove_component_size)

    for node_id in graph.nodes:
        node = osm_data.get_node(node_id)
        graph.nodes[node_id]['coord'] = (float(node.lat), float(node.lon))

    return graph

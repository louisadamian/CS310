import os.path
import time
import warnings
import overpy
import numpy as np
import networkx as nx
import pickle

UMB_REGION = [
    (42.31984190454275, -71.05251184318851),
    (42.3202193, -71.0510167),
    (42.3175209, -71.0415681),
    (42.3134307, -71.0430135),
    (42.3099378, -71.0373486),
    (42.3133297, -71.0324853),
    (42.3189148, -71.0332685),
    (42.3235297, -71.0451844),
    (42.32119679444875, -71.05265041751876),
    (42.31984190454275, -71.05251184318851),
]


def __gcdist(lat0: np.double, lon0: np.double, lat1: np.double, lon1: np.double) -> np.single:
    """
    Calculate the great circle distance in km between two points in meters using a haversine formula.
    :param lat0:
    :param lon0:
    :param lat1:
    :param lon1:
    :return:
    """
    # radius of earth from WGS84 https://en.wikipedia.org/wiki/World_Geodetic_System
    # equation from https://en.wikipedia.org/wiki/Haversine_formula#Formulation
    delta_lat = np.radians(lat1 - lat0)
    delta_lon = np.radians(lon1 - lon0)
    a = (
        1
        - np.cos(delta_lat)
        + np.cos(np.radians(lat0)) * np.cos(np.radians(lat1)) * (1 - np.cos(delta_lon))
    ) / 2
    return 6378137 * 2 * np.arcsin(np.sqrt(a))


def __weight(way: overpy.Way, node1: int = None, node2: int = None) -> (float, np.ndarray):
    """
    Calculate the weight of a way using the haversine distance between the points on the path and adds returns the weight and points
    :param way: overpy.Way to for weight to be computed on
    :param node1: starting node in the way
    :param node2: ending node in the way
    :return: (weight ,points) the weight of a way and a list of points in the way
    """
    n1 = 0
    n2 = 0
    if node1 is not None and node2 is not None:
        for i, node in enumerate(way.nodes):
            if node.id == node1:
                n1 = i
            if node.id == node2:
                n2 = i
            if n1 != 0 and n2 != 0:
                break
        if n1 > n2:
            (n1, n2) = (n2, n1)
    else:
        n1 = 0
        n2 = len(way.nodes)
    weight = 0
    points = []
    if (n2 - n1) < 2:
        points.append([way.nodes[n1].lat, way.nodes[n1].lon])
        weight += __gcdist(
            np.double(way.nodes[n1].lat),
            np.double(way.nodes[n1].lon),
            np.double(way.nodes[n2].lat),
            np.double(way.nodes[n2].lon),
        )
    for i in range(n1, n2 - 1):
        points.append([way.nodes[i].lat, way.nodes[i].lon])
        weight += __gcdist(
            np.double(way.nodes[i].lat),
            np.double(way.nodes[i].lon),
            np.double(way.nodes[i + 1].lat),
            np.double(way.nodes[i + 1].lon),
        )
    points.append([way.nodes[n2].lat, way.nodes[n2].lon])
    points = np.array(points, dtype=np.single)
    if weight == 0:
        warnings.warn(f"edge ({node1}, {node2}) has 0 weight")
    return weight, points


def __coords_list_to_str(coords_list: [(float, float)]) -> str:
    """
    convert a list of (lat, lon) coordinates to a string representation separated by whitespace for the overpass API query
    :param coords_list: list of (lat, lon) coordinate tuples
    :return: string of lat lon coordinates
    """
    coord_str = ""
    for coord in coords_list:
        if coord_str != "":
            coord_str += " "
        coord_str += str(coord[0]) + " " + str(coord[1])
    return coord_str


def get_ways(filepath="umb_way_data.pkl", force_download=False) -> overpy.Result:
    """
    gets OpenStreetMap ways from Overpass API or local cache
    :param filepath: path to pickle file with openstreetmap data
    :param force_download: force download new data from OpenStreetMaps
    :return: overpy.Result with pedestrian ways and points
    """
    # check if we already have OpenStreetMap data downloaded if it is less than 24 hours old we import it
    if (
        os.path.isfile(filepath) and time.time() - os.path.getctime(filepath) > 24 * 60 * 60
    ) and not force_download:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    api = overpy.Overpass()
    ways = api.query(
        'way["highway"~"pedestrian|footway|steps|sidewalk|cycleway|path|corridor"](poly: "'
        + __coords_list_to_str(UMB_REGION)
        + '");(._;>;);out;'
    )
    with open(filepath, "wb") as f:
        pickle.dump(ways, f)
    return ways


def convert_ways_to_graph(osm_data: overpy.Result, remove_component_size=10) -> nx.Graph:
    """
    creates a networkx graph of ways from OpenStreetMap where the weight is the GC distance between the points along the points of the way
    :param osm_data: OpenStreetMap data from overpy
    :param remove_component_size: minimum number of nodes for a connected component to not be removed
    :return:
    """
    nodes_count = np.zeros((len(osm_data.nodes), 5), dtype=np.int64)
    nodes_count[:, 0] = np.array(osm_data.node_ids)
    for way in osm_data.ways:
        for node in way.nodes:
            if "entrance" in node.tags.keys():
                if (
                    node.tags["entrance"] != "no"
                    and node.tags["entrance"] != "exit"
                    and node.tags["entrance"] != "emergency"
                ):
                    nodes_count[np.where(nodes_count == node.id)[0][0], 1] += 2
            nodes_count[np.where(nodes_count == node.id)[0][0], 1] += 1
    graph_nodes = nodes_count[nodes_count[:, 1] > 1][:, 0]
    graph = nx.Graph()
    graph.add_nodes_from(graph_nodes)
    for way in osm_data.ways:
        if "area" in way.tags.keys() and way.tags["area"] == "yes":
            nodes = np.array(way._node_ids, dtype=np.int64)
        else:
            _, _, node_indices = np.intersect1d(graph_nodes, way._node_ids, return_indices=True)
            nodes = np.take(np.array(way._node_ids), np.sort(node_indices))
        for i in range(len(nodes) - 1):
            weight, points = __weight(way, nodes[i], nodes[i + 1])
            graph.add_edge(nodes[i], nodes[i + 1], weight=weight, points=points)
    if remove_component_size > 0:
        components_set = list(nx.connected_components(graph))
        for components in components_set:
            if len(components) < remove_component_size:
                graph.remove_nodes_from(components)
    return graph


def get_graph(
    filepath="umb_graph.pkl", force_download=False, remove_component_size=10
) -> nx.Graph:
    """
    gets data from OpenStreetMaps and converts it into a networkx graph
    :param filepath: the path to the pickle file containing the networkx graph
    :param force_download: force download new data from OpenStreetMap
    :param remove_component_size: remove connected components with size less than this number of nodes
    :return: a networkx graph of points from OpenStreetMap
    """
    if not force_download and os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)
    data = get_ways(force_download=force_download)
    graph = convert_ways_to_graph(data, remove_component_size=remove_component_size)

    for node_id in graph.nodes:
        node = data.get_node(node_id)
        graph.nodes[node_id]['coord']=(float(node.lat), float(node.lon))

    with open(filepath, "wb") as f:
        pickle.dump(graph, f)
    return graph


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    graph = get_graph()
    print(f"created graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    nx.draw(graph, with_labels=True)
    plt.show()

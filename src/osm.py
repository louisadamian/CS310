import os.path
import json
import time
import overpy
import numpy as np
import networkx as nx
import pickle

UMB_REGION = [
    (42.3196561, -71.0520413),
    (42.3202193, -71.0510167),
    (42.3175209, -71.0415681),
    (42.3134307, -71.0430135),
    (42.3099378, -71.0373486),
    (42.3133297, -71.0324853),
    (42.3189148, -71.0332685),
    (42.3235297, -71.0451844),
    (42.3212511, -71.0521287),
    (42.3196561, -71.0520413),
]
api = overpy.Overpass()

#modified by erika to make __gcdist to public
def gcdist(lat0: np.single, lon0: np.single, lat1: np.single, lon1: np.single) -> np.single:
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
    delta_lat = np.radians(lat1) - np.radians(lat0)
    delta_lon = np.radians(lon1) - np.radians(lon0)
    a = (
        1
        - np.cos(delta_lat)
        + np.cos(np.radians(lat0)) * np.cos(np.radians(lat1)) * (1 - np.cos(delta_lon))
    )
    return 6378137 * 2 * np.arcsin(np.sqrt(a / 2))

# modified by to make __weight public
def weight(way: overpy.Way, node1: int = None, node2: int = None):
    if node1 is not None and node2 is not None:
        i1 = way.nodes.index(node1)
        i2 = way.nodes.index(node2)
        if i1 > i2:
            i1, i2 = i2, i1
    else:
        n1 = 0
        n2 = len(way.nodes)
    weight = 0
    for i in range(n1, n2 - 1):
        weight += gcdist(
            float(way.nodes[i].lat),
            float(way.nodes[i].lon),
            float(way.nodes[i + 1].lat),
            float(way.nodes[i + 1].lon),
        )
    return weight


def __coords_list_to_str(coords_list: [(float, float)]) -> str:
    coord_str = ""
    for coord in coords_list:
        if coord_str != "":
            coord_str += " "
        coord_str += str(coord[0]) + " " + str(coord[1])
    return coord_str


def get_points(filepath="umb_point_data.geojson") -> dict:
    """
    gets all the points on UMB campus from OSM
    :param filepath: geojson file path to read from or write to
    :return: dictionary of geoJSON data of points
    """
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return json.loads(f.read())
    query = 'node["entrance"](poly: "' + __coords_list_to_str(UMB_REGION) + '");'
    json_data = api.get(query)
    with open(filepath, "w") as f:
        f.write(json.dumps(json_data))
    return json_data


def get_buildings(filepath="umb_building_data.geojson") -> dict:
    """
    gets the polygon outlines of buildings from OSM
    :param filepath: geojson file path to read from or write to
    :return: dict of geojson building polygons
    """
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return json.loads(f.read())
    query = 'way["building"](poly: "' + __coords_list_to_str(UMB_REGION) + '");(._;>;);out;'
    json_data = api.get(query)
    with open(filepath, "w") as f:
        f.write(json.dumps(json_data))
    return json_data


def get_ways(filepath="umb_way_data.pkl", force_download=False) -> overpy.Result:
    """
    gets openstreetmap ways from Overpass API or local cache
    :param filepath: path to pickle file with openstreetmap data
    :param force_download: force download new data from OpenStreetMaps
    :return: overpy.Result with pedestrian ways and points
    """
    if (
        os.path.isfile(filepath) and time.time() - os.path.getctime(filepath) > 24 * 60 * 60
    ) or force_download:
        with open(filepath, "rb") as f:
            return pickle.load(f)
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
    :param osm_data: OpenStreetMaps data from overpy
    :param remove_component_size: minimum number of nodes for a connected component to not be removed
    :return:
    """
    nodes_count = np.zeros((len(osm_data.nodes), 5), dtype=np.int64)
    nodes_count[:, 0] = np.array(osm_data.node_ids)
    for way in osm_data.ways:
        for node in way.nodes:
            if "entrance" in node.tags.keys():
                if node.tags["entrance"] == "yes":
                    nodes_count[np.where(nodes_count == node.id)[0][0], 1] += 2
            nodes_count[np.where(nodes_count == node.id)[0][0], 1] += 1
    graph_nodes = nodes_count[nodes_count[:, 1] > 1][:, 0]
    graph = nx.Graph()
    graph.add_nodes_from(graph_nodes)
    for way in osm_data.ways:
        if "area" in way.tags.keys() and way.tags["area"] == "yes":
            nodes = np.array(way._node_ids, dtype=np.int64)
        else:
            nodes = np.intersect1d(graph_nodes, way._node_ids)
        for i in range(len(nodes) - 1):
            #weight=__weight(way
            graph.add_edge(nodes[i], nodes[i + 1], weight=weight(way))
    if remove_component_size > 0:
        components_set = list(nx.connected_components(graph))
        for components in components_set:
            if len(components) < remove_component_size:
                graph.remove_nodes_from(components)
    return graph

UMB_LANDMARKS = {
    "campus center": (42.312688, -71.036640),
    "healy library": (42.313421, -71.039625),
    "wheatly hall": (42.312116, -71.038258),
    "mccormack hall": (42.312743, -71.039448),
    "integrated sciences complex": (42.313794, -71.040958),
    "university hall": (42.313184, -71.035274),
    "beacon fitness center":(42.312743, -71.039448),
    "residence hall east": (42.316210, -71.038650),
    "residence hall west": (42.316345, -71.039641),
    "clark athletic center": (42.314877, -71.039325),
    "quinn admin": (42.314255, -71.039772), 
    "quad": (42.313870, -71.038546),
}

UMB_TRANSPO ={
    "bayside lot": (42.320589, -71.046610),
    "jfk / umass": (42.320614, -71.052382),
    "west garage": (42.315300, -71.041588),
    "quad lot": (42.313948, -71.036797),
    "campus center garage": (42.313079, -71.036145),
    "lot D":(42.317099, -71.038048),
}

from matplotlib import pyplot as plt

if __name__ == "__main__":
    ways = get_ways()
    graph = convert_ways_to_graph(ways)
    print(f"created graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    nx.draw(graph, with_labels=True)
    plt.show()

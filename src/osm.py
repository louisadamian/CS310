import os.path
import json
import overpass

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
api = overpass.API()


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
    query = (
        'way["building"](poly: "' + __coords_list_to_str(UMB_REGION) + '");(._;>;);out;'
    )
    json_data = api.get(query)
    with open(filepath, "w") as f:
        f.write(json.dumps(json_data))
    return json_data


def get_ways(filepath="umb_way_data.geojson") -> dict:
    """
    imports a dictionary of OpenStreetMap ways either from a locally cached file or from the Overpass API
    :param filepath: geojson file path to read from or write to
    :return: dictionary of geoJSON data of pedestrian paths
    """
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return json.loads(f.read())
    query = (
        'way["highway"~"pedestrian|footway|steps|sidewalk|cycleway"](poly: "'
        + __coords_list_to_str(UMB_REGION)
        + '");(._;>;);out;'
    )
    json_data = api.get(query)
    with open(filepath, "w") as f:
        f.write(json.dumps(json_data))
    return json_data

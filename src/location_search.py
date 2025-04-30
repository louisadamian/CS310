import requests
import overpy
import networkx as nx


def location_search(query: str):
    query.replace(" ", "+")
    headers = {"User-Agent": "CS310-Navigation"}
    res = requests.get(
        f"https://nominatim.openstreetmap.org/search.php?q={query}&viewbox=-71.06081%2C42.32107%2C-71.03228%2C42.31029&bounded=1&format=jsonv2",
        headers=headers,
    )
    ids =[]
    for result in res.json():
        ids.append(result["osm_id"])
    return ids
    # return res.json()["osm_id"], res.json()


def get_entrances(id):
    api = overpy.Overpass()
    res = api.query(f'way({id});node(area)[entrance~"main|yes"];out;')
    return res


def get_location_nodes(query: str, graph: nx.Graph):
    ids = location_search(query)
    for id in ids:
        osm = get_entrances(id)
        nodes = []
        for node in osm.nodes:
            if node.id in graph.nodes:
                nodes.append(node.id)
        if len(nodes) >0:
            return nodes


if __name__ == "__main__":
    osm_id, res = location_search("university hall")
    print(osm_id)
    print(res)

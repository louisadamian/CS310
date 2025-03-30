import pickle
import numpy as np
import overpy
class Way:
    def __init__(self, points:np.ndarray, id):
        self.points = points
        self.id = id

if __name__ == "__main__":
    api = overpy.Overpass()
    result = api.query(
        'way["highway"~"pedestrian|footway|steps|sidewalk|cycleway|path|corridor"](poly: "42.3196561 -71.0520413 42.3202193 -71.0510167 42.3175209 -71.0415681 42.3134307 -71.0430135 42.3099378 -71.0373486 42.3133297 -71.0324853 42.3189148 -71.0332685 42.3235297 -71.0451844 42.3212511 -71.0521287 42.3196561 -71.0520413");(._;>;);out;'
    )
    print(result)

    ways = []
    for way in result.ways:
        way_points = np.zeros(shape=(len(way.nodes), 2))
        for i, point in enumerate(way.nodes):
            way_points[i, 0] = point.lat.real
            way_points[i, 1] = point.lon.real

        ways.append(Way(way_points, way.id))
    print(ways)
    with open("umb_data.pkl", "wb") as f:
        pickle.dump(result, f)
    with open("ways.pkl","wb") as w:
        pickle.dump(ways,w)
    # with open('overpy.geojson', 'w') as f:
    #     f.write(json.dumps(result))

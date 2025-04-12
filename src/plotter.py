import pickle
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np


def __zoom_level(extent: np.ndarray):
    m = np.max([np.abs(extent[1] - extent[0]), np.abs(extent[3] - extent[2])])
    if m > 0.0055:  # if :
        return 18
    elif m > 0.007749:
        return 17
    else:
        return 16


def plot_points(ways: [np.ndarray], directions: str, crop_to_route=True):
    request = cimgt.OSM()
    fig = plt.figure(figsize=(10, 10))
    # Bounds: (lon_min, lon_max, lat_min, lat_max):
    if crop_to_route:
        allways = np.concat(ways, axis=0, dtype=np.double)
        extent = [
            allways[:, 1].min() - 0.002,
            allways[:, 1].max() + 0.002,
            allways[:, 0].min() - 0.002,
            allways[:, 0].max() + 0.002,
        ]
    else:
        extent = [-71.0324853, -71.0521287, 42.3099378, 42.3235297]
    ax = plt.axes(projection=request.crs)
    ax.set_extent(extent)
    ax.add_image(request, __zoom_level(extent))
    for way in ways:
        ax.plot(way[:, 1], way[:, 0], transform=ccrs.PlateCarree(), linewidth=2.0, color="red")
    ax.text(
        0.5,
        0.0,
        "© OpenStreetMap contributors",
        size=8,
        ha="center",
        transform=ax.transAxes,
        backgroundcolor="white",
    )
    ax.text(1.01, 0.9, directions, va="top", ha="left", transform=ax.transAxes, wrap=True)
    ax.margins(x=5)
    plt.margins(x=1)
    fig.tight_layout()


def plot_route(path: [], graph, crop_to_route=True, show=True):
    """
    plots a route given by a list of nodes in the graph onto OpenStreetMap
    :param path: the list of nodes in the graph onto which to plot
    :param graph: the networkx graph
    :param crop_to_route: crops the map to only show the route if false it shows the entire UMass Boston campus
    :param show: the plot window
    :return:
    """
    points = []
    for i in range(1, len(path)):
        points.append(np.array(graph.get_edge_data(path[i - 1], path[i])["points"]))
    plot_points(points, "", crop_to_route=crop_to_route)
    if show:
        plt.show()


if __name__ == "__main__":
    with open("ways.pkl", "rb") as f:
        ways = pickle.load(f)
    way0 = ways[287].points
    way1 = [x for x in ways if x.id == 1367084178][0].points
    way2 = [x for x in ways if x.id == 1368829688][0].points
    plot_points(
        [way0, way1, way2],
        "exit Campus Center\nturn right\nturn left on the quad path",
        True,
    )
    plt.savefig("demo.png", dpi=300)
    plt.show()

import pickle
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np


def plot_astar_path(path_coords: list[tuple[float, float]]):
    """
    erika:
    temp helper function to plot astar
    accepts a list of lat,lon tuples
    """
    path_arr = np.array(path_coords)
    request = cimgt.OSM()
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=request.crs)

    extent = [
        path_arr[:, 1].min() - 0.002,
        path_arr[:, 1].max() + 0.002,
        path_arr[:, 0].min() - 0.002,
        path_arr[:, 0].max() + 0.002,
    ]
    ax.set_extent(extent)
    ax.add_image(request, 18)  # 18 = zoom level
    ax.plot(path_arr[:, 1], path_arr[:, 0], transform=ccrs.PlateCarree(), linewidth=2.0, color="blue")
    ax.text(
        0.5,
        0.025,
        "© OpenStreetMap contributors",
        size=8,
        ha="center",
        transform=ax.transAxes,
    )

    fig.tight_layout()
    plt.savefig("astar_path.png", dpi=300)
    plt.show()



def plot_route(ways: [np.ndarray], directions: str, crop_to_route=True):
    request = cimgt.OSM()
    fig = plt.figure(figsize=(10, 10))
    # Bounds: (lon_min, lon_max, lat_min, lat_max):
    if crop_to_route:
        allways = np.concat(ways, axis=0)
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
    ax.add_image(request, 18)  # 18 = zoom level
    for way in ways:
        ax.plot(way[:, 1], way[:, 0], transform=ccrs.PlateCarree(), linewidth=2.0, color="red")
    ax.text(
        0.5,
        0.025,
        "© OpenStreetMap contributors",
        size=8,
        ha="center",
        transform=ax.transAxes,
    )
    ax.text(1.01, 0.9, directions, va="top", ha="left", transform=ax.transAxes, wrap=True)
    ax.margins(x=5)
    plt.margins(x=1)
    fig.tight_layout()


if __name__ == "__main__":
    with open("ways.pkl", "rb") as f:
        ways = pickle.load(f)
    way0 = ways[287].points
    way1 = [x for x in ways if x.id == 1367084178][0].points
    way2 = [x for x in ways if x.id == 1368829688][0].points
    plot_route(
        [way0, way1, way2],
        "exit Campus Center\nturn right\nturn left on the quad path",
        True,
    )

    plt.savefig("demo.png", dpi=300)
    plt.show()

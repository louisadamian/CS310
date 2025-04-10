from src.graph import build_osm_graph
from src.algorithms.astar import astar
from src.osm import gcdist, UMB_LANDMARKS
from src.plotter import plot_astar_path


def find_node(graph, lat, lon):
    """
    given a coord, find the closest graph node with coord data
    """

    closest = None
    min = float("inf")
    for node, data in graph.nodes(data = True):
        if 'coord' not in data:
            continue
        dist = gcdist(lat, lon, *data['coord'])
        if dist < min :
            min = dist
            closest = node

    if closest is None:
        raise RuntimeError("node near coord not found")
    return closest


if __name__ == "__main__":
    try:
        graph = build_osm_graph()

        start = "university hall"
        goal = "wheatly hall"

        # test a landmark
        start_coord = UMB_LANDMARKS.get(start)
        goal_coord = UMB_LANDMARKS.get(goal)
        if not start_coord or not goal_coord:
            raise KeyError("landmark not found")

        #map to node id
        start_node = find_node(graph, *start_coord)
        goal_node = find_node(graph, *goal_coord)

        print(f"Start: {start_node} ({start})" )
        print(f"goal: {goal_node} ({goal})" )

        path = astar(graph, start_node, goal_node)
        if not path:
            raise RuntimeError("no path found between landmarks")

        path_coords =[]
        for node in path:
            if 'coord' not in graph.nodes[node]:
                raise KeyError(f"node {node} missing in 'coord' data.")
            path_coords.append(graph.nodes[node]['coord'])

        directions = f"{start.title()} to {goal.title()}"
        print(f" start: {start_coord}")
        print(f" end: {goal_coord}")
        print(path_coords)
        plot_astar_path(path_coords)
    except Exception as e:
        print(f"excetion {type(e).__name__}:{e}")

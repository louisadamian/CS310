import sys
import osm
import plotter
from location_search import get_location_nodes
from algorithms.astar import astar
from algorithms.dijkstras import dijkstra


if __name__ == "__main__":
    if len(sys.argv) > 3:
        start = sys.argv[1]
        end = sys.argv[2]
        algorithm = sys.argv[3]
    else:
        start = input("please enter your starting location: ")
        end = input("please enter your ending location: ")
        algorithm = input("please choose an algorithm ('dijkstra', 'astar'): ")

    graph = osm.get_graph()
    start_nodes = get_location_nodes(start, graph)
    end_nodes = get_location_nodes(end, graph)

    if len(start_nodes) == 0 or len(end_nodes) == 0:
        print("No roads near your location were found")
        sys.exit(1)

    match algorithm:
        case "dijkstra":
            print("\nComputing shortest path using Dijkstra's algorithm...\n")
            path, explored_nodes = dijkstra(graph, start_nodes[0], end_nodes[0])
        case "astar":
            print("\nComputing shortest path using A* algorithm...\n")
            path, explored_nodes = astar(graph, start_nodes[0], end_nodes[0])
        case _:
            raise ValueError("Invalid choice")

    walking_distance = 0
    for i in range(len(path) - 1):
        walking_distance += graph[path[i]][path[i + 1]]["weight"]
    estimate_walk_speed = 5000 / 60
    estimate_walk_time = walking_distance / estimate_walk_speed
    miles = walking_distance * 0.000621371

    print(f"Estimated walk time: {estimate_walk_time:.1f} minutes")
    print(f"Walking distance: {miles:.2f} miles \n")
    plotter.plot_route(
        path,
        graph,
        text=f"- Estimated walk time: {estimate_walk_time:.1f} minutes\n\n"
        f"- Walking distance: {miles:.2f} miles \n\n"
        f"- Expanded nodes: {explored_nodes}",
        crop_to_route=True,
        show=True,
    )


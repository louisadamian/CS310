import networkx as nx
import osm
import plotter
from algorithms.astar import astar
from osm import get_graph
from location_search import get_location_nodes
from algorithms.dijkstras import dijkstra
import time


if __name__ == "__main__":
    # Erases the generated pkl file before new compilation
    try:
        os.remove("umb_way_data.pkl")
        os.remove("umb_graph.pkl")
    except:
        print("\nUMass Boston CS310 Project\n")

    get_start = input("Input starting point: \n")
    get_goal = input("\nInput destination: \n")

    algo_choice = input("\nChoose algorithm ('dijkstra', 'astar'): \n")
    graph = get_graph()

    # Query for node from user standard input
    start_node = get_location_nodes(get_start, graph)
    if not start_node:
        raise ValueError(f"Node not found for '{get_start}'")

    goal_node = get_location_nodes(get_goal, graph)
    if not goal_node:
        raise ValueError(f"Node not found for '{get_goal}'")

    start_id = start_node[0]
    goal_id = goal_node[0]

    match algo_choice:
        case 'dijkstra':
            print("\nComputing shortest path using Dijkstra's algorithm...\n")
            path = dijkstra(graph, start_id, goal_id)
        case 'astar':
            print("\nComputing shortest path using A* algorithm...\n")
            path = astar(graph, start_id, goal_id)
        case _:
            raise ValueError("Invalid choice")

    # Calculate actual walking distance in time between the two points
    walking_distance = 0
    for i in range(len(path) - 1):
        walking_distance += graph[path[i]][path[i + 1]]['weight']

    # Wikipedia 'preferred walking speed' 5 km/h ~ 1.39 meters per seconds
    estimate_walk_speed= 5000 / 60
    estimate_walk_time = walking_distance / estimate_walk_speed
    miles = walking_distance * 0.000621371

    print(f"Estimated walk time: {estimate_walk_time:.1f} minutes")
    print(f"Walking distance: {miles:.2f} miles \n")

    plotter.plot_route(path, graph, crop_to_route=True, show=True)

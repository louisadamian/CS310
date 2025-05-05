import heapq
import networkx as nx
import time
from typing import List
from osm import __gcdist


def reconstruct_path(cameFrom: dict[int, int], current: int, start: int) -> List[int]:
    """
    Reconstructs the shortest path from cameFrom map
    """
    path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        path.append(current)
    return path[::-1]


def dijkstra(graph: nx.Graph, start_id: int, goal_id: int) -> list[int]:
    """
    Finds the single shortest path between two nodes using Dijkstra's algorithm

    Source: Pseudocode from https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm and A*

    :param graph:
    :param start_id:
    :param goal_id:
    :return:
    """
    if start_id not in graph.nodes or goal_id not in graph.nodes:
        raise ValueError("start or goal id not found in graph ")

    start_time = time.time()

    openSet: List[tuple[float, int]] = [(0.0, start_id)]
    cameFrom: Dict[int, int]={}

    # Cost from start node to each node
    gScore: Dict[int, float] = {node: float('inf') for node in graph.nodes}
    gScore[start_id] = 0.0

    nodes_explored =0
    while openSet:
        _, current = heapq.heappop(openSet)
        nodes_explored +=1
        if current == goal_id:
            end_time = time.time()
            print(f"Expanded nodes: {nodes_explored}")
            print(f"{end_time - start_time:.4f} seconds")
            return reconstruct_path(cameFrom, current, start_id), nodes_explored

        for neighbor in graph.neighbors(current):
            edgeWeight = graph[current][neighbor]['weight']
            tentative_gScore = gScore[current] + edgeWeight

            # If a better path is found
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                heapq.heappush(openSet, (tentative_gScore, neighbor))
        # no path found
    raise RuntimeError(f"No path found between node {start_id} and node {goal_id}")

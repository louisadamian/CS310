import heapq
import networkx as nx
import time
from typing import List
from osm import __gcdist
from algorithms.dijkstras import reconstruct_path


def heuristic(graph: nx.Graph, node0: int, node1: int) -> float:
    """
    Heuristic function that estimates the distance between two nodes
    using the haversince distance between their coord
    """
    return __gcdist(
        *graph.nodes[node0]['coord'],
        *graph.nodes[node1]['coord']
    )


def astar(graph: nx.Graph, start_id: int, goal_id: int) -> (List[int], int):
    """
    Finds the shortest path between two nodes using the A* algorithm

    Source: A* pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm

    :param graph: networkx graph with osm node ids and weighted edges
    :param start_id: starting node
    :param goal_id: goal node
    :return: a list of node ids representing the path from start to goal. empty list
    if no path found.
    """

    if start_id not in graph.nodes or goal_id not in graph.nodes:
        raise ValueError("start or goal id not found in graph ")

    start_time = time.time()

    openSet: list[tuple[float, int]] = [(heuristic(graph, start_id, goal_id), start_id)]

    cameFrom: dict[int, int] = {}

    # Cost from start node to each node
    gScore: dict[int, float] = {node: float("inf") for node in graph.nodes}
    gScore[start_id] = 0.0

    # Est total cost from start to goal through each node
    fScore: dict[int, float] = {node: float("inf") for node in graph.nodes}
    fScore[start_id] = heuristic(graph, start_id, goal_id)

    nodes_explored:int =0
    while openSet:
        # Pop the node with the lowest fScore
        _, current = heapq.heappop(openSet)
        nodes_explored += 1
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
                fScore[neighbor] = tentative_gScore + heuristic(graph, neighbor, goal_id)
                heapq.heappush(openSet, (fScore[neighbor], neighbor))
    # no path found
    raise RuntimeError(f"No path found between node {start_id} and node {goal_id}")

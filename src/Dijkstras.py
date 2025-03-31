import math
import heapq
def dijkstras(graph, start_node, destination):
    global current_node, current_distance
    nodes = ['a', 'b', 'c', 'd', 'e']           #these will be filled with all our locations
    distances_to_node = {}                      #distances from start node to destination
    priority_queue = [(0, start_node)]
    visited = set()

    for node in nodes:                          #populating the intial distances
        if node == start_node:
            distances_to_node[node] = 0
        else:
            distances_to_node[node] = math.inf

    while priority_queue:                       #initialized to (0, a)
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)               #add a to set. this makes sure we dont visit nodes twice

        for neighbor, weight in graph[current_node].items():    #check the items in the graph, grap neighbor and weight ie (b, 4)                                                              #ie. (b, 4)
            new_distance = current_distance + weight            #take the distance traveled and add the edge weight o get new distance
            if new_distance < distances_to_node[neighbor]:      #if this path is smaller than a previous update distance
                distances_to_node[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor)) #add the neighbors of A to the minpq
    return distances_to_node

    # Example Graph
graph = {
    'a': {'b': 4, 'c': 1},
    'b': {'a': 4, 'c': 2, 'd': 5},
    'c': {'a': 1, 'b': 2, 'd': 8, 'e': 10},
    'd': {'b': 5, 'c': 8, 'e': 2},
    'e': {'c': 10, 'd': 2}
}

shortest_paths = dijkstras(graph, 'a', 'e')
print(shortest_paths)









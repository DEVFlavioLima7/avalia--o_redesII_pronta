import heapq

def Dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_dist, current_node = heapq.heappop(queue)
        for neighbor, weight in graph[current_node].items():
            alt = current_dist + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = current_node
                heapq.heappush(queue, (alt, neighbor))

    paths = {}
    for node in graph:
        if node == start:
            continue
        path = []
        current = node
        while current and current != start:
            path.insert(0, current)
            current = previous[current]
        paths[node] = path if current == start else []
    return paths

if __name__ == "__main__":
    graph = {
        'router1': {'router2': 1},
        'router2': {'router1': 1, 'router3': 1},
        'router4': {'router3': 1, 'router5': 1},
        'router5': {'router4': 1},
        'router3': {'router2': 1, 'router4': 1}
    }
    start_router = 'router3'
    shortest_paths = Dijkstra(graph, start_router)
    print(f"Shortest paths from {start_router}:")
    for destination, path in shortest_paths.items():
        print(f"  To {destination}: {path}")
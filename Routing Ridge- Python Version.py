import turtle as t
import math as m
import heapq

windowwidth, windowheight = t.screensize()

nodes = []
t.bgpic("ridgemapfinal.gif")

# Permanent nodes
permanent_nodes = [
    [-278, 246, []], [-232, 174, []], [-303, 124, []],
    [-210, -11, []], [-214, -55, []], [-171, -122, []],
    [-203, -154, []], [-195, -180, []], [-174, -24, []],
    [-23, -55, []], [-23, -156, []], [-22, -87, []],
    [-168, 76, []], [-168, 7, []], [-21, 46, []],
    [103, 47, []], [202, 51, []], [201, -18, []],
    [-60, -159, []], [104, -86, []], [208, -90, []],
    [274, -88, []], [-190, 25, []],
]

# Re-adding edges to make the graph
permanent_edges = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
    [6, 7], [7, 18], [18, 10], [10, 11], [11, 9], [9, 8],
    [8, 13], [11, 19], [19, 20], [20, 21], [9, 14], [14, 12],
    [14, 15], [15, 16], [16, 17], [19, 15], [1, 12],
    [12, 22], [13, 22], [22, 3]
]

graph = {}

# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def build_graph():
    for i in range(len(permanent_nodes)):
        graph[i] = []
    for edge in permanent_edges:
        i, j = edge
        n1 = permanent_nodes[i]
        n2 = permanent_nodes[j]
        dist = calculate_distance(n1[0], n1[1], n2[0], n2[1])
        graph[i].append((j, dist))
        graph[j].append((i, dist))

def dijkstra(start, end):
    queue = [(0, start)]
    distances = {start: 0}
    prev = {}
    visited = set()

    while queue:
        cost, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)

        if node == end:
            break

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                prev[neighbor] = node

    # Remake path
    path = []
    current = end
    while current in prev:
        path.insert(0, current)
        current = prev[current]
    if path:
        path.insert(0, start)
    return path

def draw_path(path):
    t.pencolor("green")
    t.width(3)
    t.up()
    t.goto(permanent_nodes[path[0]][0], permanent_nodes[path[0]][1])
    t.down()
    for i in path[1:]:
        t.goto(permanent_nodes[i][0], permanent_nodes[i][1])
    t.width(1)
    t.pencolor("blue")
    t.up()

# Draw perma node index markers
def setup():
    t.speed(8)
    t.fillcolor("blue")
    for i, node in enumerate(permanent_nodes):
        t.up()
        t.pencolor("red")
        t.goto(node[0], node[1] + 5)
        t.down()
        t.write(i)
        t.up()

setup()

# Choosing startpoint and endpoint
selected_nodes = []

def handle_click(x, y):
    global selected_nodes
    
    # Nearest perma node to clicked point
    nearest_node = None
    min_distance = float("inf")
    for i, node in enumerate(permanent_nodes):
        node_x, node_y = node[0], node[1]
        distance = calculate_distance(x, y, node_x, node_y)
        if distance < min_distance:
            min_distance = distance
            nearest_node = i

    selected_nodes.append(nearest_node)
    t.goto(permanent_nodes[nearest_node][0], permanent_nodes[nearest_node][1])
    t.dot(10, "blue")
    print(f"Selected node: {nearest_node}")

    if len(selected_nodes) == 2:
        start, end = selected_nodes[0], selected_nodes[1]
        print(f"Finding shortest path from {start} to {end}")
        path = dijkstra(start, end)
        print(f"Path: {path}")
        draw_path(path)
        selected_nodes.clear()

build_graph()
t.onscreenclick(handle_click)
t.listen()
t.mainloop()

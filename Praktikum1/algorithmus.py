from collections import deque
import math
from heapq import heappush, heappop

G = {
    "Augsburg": {"München", "Nürnberg"},
    "Erfurt": {"Würzburg"},
    "Frankfurt": {"Würzburg", "Kassel", "Mannheim"},
    "Karlsruhe": {"Mannheim", "Stuttgart"},
    "Kassel": {"Frankfurt", "Würzburg"},
    "Mannheim": {"Karlsruhe", "Würzburg", "Frankfurt"},
    "München": {"Augsburg", "Nürnberg"},
    "Nürnberg": {"Würzburg", "Stuttgart", "München", "Augsburg"},
    "Stuttgart": {"Karlsruhe", "Würzburg", "Nürnberg"},
    "Würzburg": {"Frankfurt", "Mannheim", "Stuttgart", "Nürnberg", "Kassel", "Erfurt"},
}

start = "Würzburg"
goal = "München"

h_km = {
    "Augsburg": 0,
    "Erfurt": 400,
    "Frankfurt": 100,
    "Karlsruhe": 10,
    "Kassel": 460,
    "Mannheim": 200,
    "München": 0,
    "Nürnberg": 537,
    "Stuttgart": 300,
    "Würzburg": 170,
}

# Correct a step-heuristic for unit-cost edges: ceil(km / 300)
# (Assume any single road edge on the map is <= 300 km.)
h_steps = {n: math.ceil(h_km[n] / 300) for n in h_km}

def dfs_graph(start, goal):
    #depht-first search (graph-search): uses a stack and a visited set
    stack = [(start, [start])]
    visited = set([start])
    max_ds = 1
    pops = 0
    while stack:
        node, path = stack.pop()
        pops += 1
        if node == goal:
            return path, pops, max_ds
        # push neighbors in reverse alphabetical order so that pop() makes alphabetical first
        for nb in sorted(G[node], reverse=True):
            if nb not in visited:
                visited.add(nb)
                stack.append((nb, path + [nb]))
        max_ds = max(max_ds, len(stack))
    return None, pops, max_ds

def bfs_graph(start, goal):
    # breadth-first search (graph-search): uses a queue and a visited set
    q = deque([(start, [start])])
    visited = set([start])
    max_q = 1
    pops = 0
    while q:
        node, path = q.popleft()
        pops += 1
        if node == goal:
            return path, pops, max_q
        for nb in sorted(G[node]):  # alphabetical enqueue
            if nb not in visited:
                visited.add(nb)
                q.append((nb, path + [nb]))
        max_q = max(max_q, len(q))
    return None, pops, max_q

def astar_tree_no_cycles(start, goal, heuristic):
    # A* tree-search with no cycels: no revisit any node already on the current path
    counter = 0
    frontier = []
    heappush(frontier, (heuristic[start], counter, start, [start], 0))  # (f, tiebreak, node, path, g)
    max_frontier = 1
    pops = 0
    while frontier:
        f, _, node, path, g = heappop(frontier)
        pops += 1
        if node == goal:
            return path, pops, max_frontier
        for nb in sorted(G[node]):  # alphabetical tiebreak
            if nb in path:  # avoid any cycele
                continue
            g2 = g + 1                      # unit step cost
            f2 = g2 + heuristic[nb]
            counter += 1
            heappush(frontier, (f2, counter, nb, path + [nb], g2))
        max_frontier = max(max_frontier, len(frontier))
    return None, pops, max_frontier

# start all searchings
dfs_path, dfs_pops, dfs_max = dfs_graph(start, goal)
bfs_path, bfs_pops, bfs_max = bfs_graph(start, goal)
astar_bad_path, astar_bad_pops, astar_bad_max = astar_tree_no_cycles(start, goal, h_km)
astar_ok_path, astar_ok_pops, astar_ok_max = astar_tree_no_cycles(start, goal, h_steps)

print("DFS (graph-search):")
print("  Path:", " → ".join(dfs_path))
print("  pops:", dfs_pops, " | max stack size:", dfs_max)
print()

print("BFS (graph-search):")
print("  Path:", " → ".join(bfs_path))
print("  pops:", bfs_pops, " | max queue size:", bfs_max)
print()

print("A* with given h_km (tree-search, no cycles):")
print("  Path:", " → ".join(astar_bad_path))
print("  pops:", astar_bad_pops, " | max frontier size:", astar_bad_max)
print()

print("A* with corrected h_steps = ceil(h_km/300) (tree-search, no cycles):")
print("  Path:", " → ".join(astar_ok_path))
print("  pops:", astar_ok_pops, " | max frontier size:", astar_ok_max)

print()
print()
print("""
Gegebene h(n) (in km) dürfen nicht für A* mit Schrittkosten=1 benutzt werden weil
die Einheiten passen nicht, Heuristik überschätzt (z.B. Nürnberg 537 > 1). Man müsste machen: 
h_steps = ceil(h_km / 300)
""")
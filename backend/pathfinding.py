"""
Pathfinding algorithms for maze navigation
Includes: BFS, DFS, A*, Dijkstra
"""

from typing import List, Dict, Optional, Set, Tuple
from collections import deque
import heapq

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def manhattan_distance(self, other: 'Position') -> int:
        """Calculate Manhattan distance to another position"""
        return abs(self.x - other.x) + abs(self.y - other.y)


class Maze:
    def __init__(self, grid: List[List[int]], spawn: Position, goal: Position):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0
        self.spawn = spawn
        self.goal = goal

    def is_walkable(self, pos: Position) -> bool:
        """Check if position is walkable (0 = walkable, 1 = wall)"""
        if 0 <= pos.y < self.height and 0 <= pos.x < self.width:
            return self.grid[pos.y][pos.x] == 0
        return False

    def get_neighbors(self, pos: Position) -> List[Position]:
        """Get valid neighbor positions (up, right, down, left)"""
        directions = [
            Position(pos.x, pos.y - 1),  # Up
            Position(pos.x + 1, pos.y),  # Right
            Position(pos.x, pos.y + 1),  # Down
            Position(pos.x - 1, pos.y)   # Left
        ]
        return [p for p in directions if self.is_walkable(p)]


def bfs_search(maze: Maze) -> Optional[List[Position]]:
    """
    Breadth-First Search (BFS)
    - Guarantees shortest path
    - Explores level by level
    - Good for unweighted graphs
    """
    start = maze.spawn
    goal = maze.goal

    if start == goal:
        return [start]

    queue = deque([(start, [start])])
    visited: Set[Position] = {start}

    while queue:
        current, path = queue.popleft()

        for neighbor in maze.get_neighbors(current):
            if neighbor in visited:
                continue

            new_path = path + [neighbor]

            if neighbor == goal:
                return new_path

            visited.add(neighbor)
            queue.append((neighbor, new_path))

    return None  # No path found


def dfs_search(maze: Maze) -> Optional[List[Position]]:
    """
    Depth-First Search (DFS)
    - Does NOT guarantee shortest path
    - Explores deeply before backtracking
    - Memory efficient
    """
    start = maze.spawn
    goal = maze.goal

    if start == goal:
        return [start]

    stack = [(start, [start])]
    visited: Set[Position] = {start}

    while stack:
        current, path = stack.pop()

        for neighbor in maze.get_neighbors(current):
            if neighbor in visited:
                continue

            new_path = path + [neighbor]

            if neighbor == goal:
                return new_path

            visited.add(neighbor)
            stack.append((neighbor, new_path))

    return None  # No path found


def a_star_search(maze: Maze) -> Optional[List[Position]]:
    """
    A* Search Algorithm
    - Guarantees shortest path
    - Uses heuristic (Manhattan distance)
    - Most efficient for shortest path
    """
    start = maze.spawn
    goal = maze.goal

    if start == goal:
        return [start]

    # Priority queue: (f_score, counter, current_pos, path)
    counter = 0
    heap = [(0, counter, start, [start])]
    visited: Set[Position] = set()
    g_scores: Dict[Position, int] = {start: 0}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path

        current_g = g_scores[current]

        for neighbor in maze.get_neighbors(current):
            if neighbor in visited:
                continue

            new_g = current_g + 1

            if neighbor not in g_scores or new_g < g_scores[neighbor]:
                g_scores[neighbor] = new_g
                h_score = neighbor.manhattan_distance(goal)
                f_score = new_g + h_score

                counter += 1
                new_path = path + [neighbor]
                heapq.heappush(heap, (f_score, counter, neighbor, new_path))

    return None  # No path found


def dijkstra_search(maze: Maze) -> Optional[List[Position]]:
    """
    Dijkstra's Algorithm
    - Guarantees shortest path
    - Does not use heuristic
    - Similar to BFS but with priority queue
    """
    start = maze.spawn
    goal = maze.goal

    if start == goal:
        return [start]

    # Priority queue: (cost, counter, current_pos, path)
    counter = 0
    heap = [(0, counter, start, [start])]
    visited: Set[Position] = set()
    costs: Dict[Position, int] = {start: 0}

    while heap:
        cost, _, current, path = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path

        for neighbor in maze.get_neighbors(current):
            if neighbor in visited:
                continue

            new_cost = cost + 1

            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                counter += 1
                new_path = path + [neighbor]
                heapq.heappush(heap, (new_cost, counter, neighbor, new_path))

    return None  # No path found


def solve_maze(maze: Maze, algorithm: str = "bfs") -> Optional[List[Dict]]:
    """
    Solve maze using specified algorithm

    Args:
        maze: Maze object with grid, spawn, and goal
        algorithm: One of ["bfs", "dfs", "astar", "dijkstra"]

    Returns:
        List of positions as dicts [{"x": int, "y": int}, ...]
        or None if no path found
    """
    algorithms = {
        "bfs": bfs_search,
        "dfs": dfs_search,
        "astar": a_star_search,
        "dijkstra": dijkstra_search
    }

    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}. Choose from {list(algorithms.keys())}")

    path = algorithms[algorithm](maze)

    if path is None:
        return None

    # Convert Position objects to dicts
    return [{"x": pos.x, "y": pos.y} for pos in path]


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    # Test maze (L-shaped)
    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    maze = Maze(
        grid=grid,
        spawn=Position(1, 1),
        goal=Position(8, 7)
    )

    print("🧪 Testing Pathfinding Algorithms\n")

    for algo in ["bfs", "dfs", "astar", "dijkstra"]:
        path = solve_maze(maze, algo)
        if path:
            print(f"✅ {algo.upper():10} → Path length: {len(path)} steps")
        else:
            print(f"❌ {algo.upper():10} → No path found")

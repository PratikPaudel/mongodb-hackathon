# backend/simulation_simple.py
"""
Simplified Maze Simulation for MirrorMinds Demo
This is a streamlined version focused on the hackathon demo.
For full PyGame visualization, see PRD_2.md
"""

import asyncio
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathfinding import solve_maze as pathfinding_solve_maze, Maze as PathfindingMaze, Position as PathfindingPosition

@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

@dataclass
class Agent:
    agent_id: str
    name: str
    position: Position
    has_skill: bool = False
    path_history: List[Position] = field(default_factory=list)
    completion_time: float = 0.0
    status: str = "idle"  # idle, navigating, completed, failed

class Maze:
    def __init__(self, grid: List[List[int]], spawn: Position, goal: Position):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0
        self.spawn = spawn
        self.goal = goal

    def is_walkable(self, pos: Position) -> bool:
        """Check if position is within bounds and walkable"""
        if 0 <= pos.y < self.height and 0 <= pos.x < self.width:
            return self.grid[pos.y][pos.x] == 0
        return False

    def get_neighbors(self, pos: Position) -> List[Position]:
        """Get walkable neighbor positions"""
        directions = [
            Position(pos.x, pos.y - 1),  # Up
            Position(pos.x + 1, pos.y),  # Right
            Position(pos.x, pos.y + 1),  # Down
            Position(pos.x - 1, pos.y)   # Left
        ]
        return [p for p in directions if self.is_walkable(p)]

class MazeSimulation:
    def __init__(self, maze: Maze, websocket_manager=None, db=None):
        self.maze = maze
        self.agents: List[Agent] = []
        self.manager = websocket_manager
        self.db = db

    def add_agent(self, agent: Agent):
        """Add agent to simulation"""
        agent.position = Position(self.maze.spawn.x, self.maze.spawn.y)
        agent.path_history = [Position(self.maze.spawn.x, self.maze.spawn.y)]
        self.agents.append(agent)

    async def broadcast_event(self, event_type: str, data: Dict):
        """Broadcast event via WebSocket if manager is available"""
        if self.manager:
            await self.manager.broadcast({
                "type": event_type,
                "timestamp": datetime.now().isoformat(),
                "data": data
            })

    async def save_skill_to_db(self, skill_data: Dict) -> str:
        """Save extracted skill to MongoDB"""
        if self.db is None:
            return "skill_demo_only"

        try:
            # Generate a simple embedding (in production, use Voyage AI)
            import numpy as np
            embedding = np.random.rand(1024).tolist()

            skill_doc = {
                "schema_version": 1,
                "skill_id": f"skill_maze_nav_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "version": 1,
                "name": skill_data["name"],
                "description": skill_data["description"],
                "description_embedding": embedding,
                "metadata": {
                    "author_agent": skill_data["author_agent"],
                    "contributors": [],
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "skill_type": "maze_navigation",
                    "maze_type": "l_shaped",
                    "complexity": "simple",
                    "tags": ["maze", "navigation", "demo"]
                },
                "visual_path": skill_data["visual_path"],
                "strategy": {
                    "type": "path_following",
                    "path": skill_data["visual_path"]
                },
                "stats": {
                    "total_uses": 1,
                    "successful_uses": 1,
                    "success_rate": 1.0,
                    "avg_completion_time_ms": skill_data["completion_time"] * 1000,
                    "avg_steps": len(skill_data["visual_path"]),
                    "improvement_over_baseline": 0.0,
                    "last_used": datetime.now()
                },
                "relationships": {
                    "parent_skill": None,
                    "improved_by": [],
                    "similar_skills": [],
                    "used_in_combination_with": []
                },
                "applicable_to": {
                    "maze_types": ["l_shaped"],
                    "size_range": {"min": 5, "max": 50},
                    "complexity": ["simple", "medium"]
                },
                "status": "active"
            }

            result = await self.db.skills.insert_one(skill_doc)
            print(f"✅ Skill saved to MongoDB: {skill_doc['skill_id']}")
            return skill_doc['skill_id']
        except Exception as e:
            print(f"⚠️ Failed to save skill to MongoDB: {e}")
            return "skill_demo_only"

    async def random_walk(self, agent: Agent, max_steps: int = 200) -> float:
        """Agent performs random walk (no skill) - simulates exploration"""
        agent.status = "navigating"
        start_time = datetime.now()
        steps = 0

        await self.broadcast_event("agent_start", {
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "strategy": "random_exploration"
        })

        while agent.position != self.maze.goal:
            if steps >= max_steps:
                agent.status = "failed"
                await self.broadcast_event("agent_failed", {
                    "agent_id": agent.agent_id,
                    "reason": "max_steps_exceeded"
                })
                return -1

            # Get walkable neighbors
            neighbors = self.maze.get_neighbors(agent.position)

            if neighbors:
                # Choose random neighbor
                next_pos = random.choice(neighbors)
                agent.position = Position(next_pos.x, next_pos.y)
                agent.path_history.append(Position(next_pos.x, next_pos.y))

                # Broadcast position update EVERY step for smooth visualization
                await self.broadcast_event("agent_position", {
                    "agent_id": agent.agent_id,
                    "position": {"x": agent.position.x, "y": agent.position.y},
                    "steps": steps
                })

            steps += 1
            await asyncio.sleep(0.08)  # Slow down more for better visibility

        agent.status = "completed"
        end_time = datetime.now()
        agent.completion_time = (end_time - start_time).total_seconds()

        await self.broadcast_event("agent_completed", {
            "agent_id": agent.agent_id,
            "completion_time": agent.completion_time,
            "steps": steps,
            "strategy": "random_exploration"
        })

        return agent.completion_time

    async def pathfinding_navigation(self, agent: Agent, algorithm: str = "bfs") -> float:
        """
        Agent navigates using pathfinding algorithm (BFS, DFS, A*, Dijkstra)

        Args:
            agent: Agent to navigate
            algorithm: One of ["bfs", "dfs", "astar", "dijkstra"]

        Returns:
            completion_time in seconds, or -1 if failed
        """
        agent.status = "navigating"
        start_time = datetime.now()

        await self.broadcast_event("agent_start", {
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "strategy": f"pathfinding_{algorithm}"
        })

        # Use pathfinding algorithm to find optimal path
        pathfinding_maze = PathfindingMaze(
            grid=self.maze.grid,
            spawn=PathfindingPosition(self.maze.spawn.x, self.maze.spawn.y),
            goal=PathfindingPosition(self.maze.goal.x, self.maze.goal.y)
        )

        optimal_path = pathfinding_solve_maze(pathfinding_maze, algorithm)

        if not optimal_path:
            agent.status = "failed"
            await self.broadcast_event("agent_failed", {
                "agent_id": agent.agent_id,
                "reason": "no_path_found",
                "algorithm": algorithm
            })
            return -1

        # Navigate along the optimal path
        steps = 0
        for step in optimal_path:
            agent.position = Position(step['x'], step['y'])
            agent.path_history.append(Position(step['x'], step['y']))

            # Broadcast position update
            await self.broadcast_event("agent_position", {
                "agent_id": agent.agent_id,
                "position": {"x": agent.position.x, "y": agent.position.y},
                "steps": steps,
                "algorithm": algorithm
            })

            steps += 1
            await asyncio.sleep(0.08)  # Same speed as random walk

            if agent.position == self.maze.goal:
                break

        agent.status = "completed"
        end_time = datetime.now()
        agent.completion_time = (end_time - start_time).total_seconds()

        await self.broadcast_event("agent_completed", {
            "agent_id": agent.agent_id,
            "completion_time": agent.completion_time,
            "steps": steps,
            "strategy": f"pathfinding_{algorithm}",
            "algorithm": algorithm
        })

        return agent.completion_time

    async def execute_skill(self, agent: Agent, skill_path: List[Dict]) -> float:
        """Agent executes learned skill (follows optimized path)"""
        agent.status = "navigating"
        agent.has_skill = True
        start_time = datetime.now()

        await self.broadcast_event("agent_start", {
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "strategy": "learned_skill",
            "has_skill": True
        })

        steps = 0
        for step in skill_path:
            agent.position = Position(step['x'], step['y'])
            agent.path_history.append(Position(step['x'], step['y']))

            # Broadcast position update
            await self.broadcast_event("agent_position", {
                "agent_id": agent.agent_id,
                "position": {"x": agent.position.x, "y": agent.position.y},
                "steps": steps,
                "has_skill": True
            })

            steps += 1
            await asyncio.sleep(0.05)  # Faster than random walk but still visible

            if agent.position == self.maze.goal:
                break

        agent.status = "completed"
        end_time = datetime.now()
        agent.completion_time = (end_time - start_time).total_seconds()

        await self.broadcast_event("agent_completed", {
            "agent_id": agent.agent_id,
            "completion_time": agent.completion_time,
            "steps": steps,
            "strategy": "learned_skill"
        })

        return agent.completion_time

    async def run_demo_sequence(self) -> Dict:
        """Run complete demo: Agent A explores, Agent B uses skill"""
        print("🎬 Starting MirrorMinds Demo Sequence...")

        # Create Agent A (Explorer)
        agent_a = Agent(
            agent_id="agent_alpha",
            name="Agent Alpha (Explorer)",
            position=Position(self.maze.spawn.x, self.maze.spawn.y)
        )
        self.add_agent(agent_a)

        # Agent A: Random exploration
        print("📍 Agent Alpha: Starting random exploration...")
        time_a = await self.random_walk(agent_a, max_steps=500)

        if time_a < 0:
            print("❌ Agent Alpha failed to complete")
            return {"error": "Agent A failed"}

        print(f"✅ Agent Alpha completed in {time_a:.2f}s with {len(agent_a.path_history)} steps")

        # Extract skill from Agent A's path
        skill_path = [{"x": p.x, "y": p.y} for p in agent_a.path_history]

        # Pause for effect
        await asyncio.sleep(2)

        # Broadcast skill extraction
        await self.broadcast_event("skill_extracted", {
            "from_agent": agent_a.agent_id,
            "skill_name": "Maze Navigation Strategy",
            "path_length": len(skill_path),
            "completion_time": time_a
        })

        # Save skill to MongoDB
        skill_id = await self.save_skill_to_db({
            "name": "L-Shaped Maze Navigation",
            "description": f"Efficient navigation strategy for L-shaped mazes. Learned from {agent_a.name}'s successful exploration.",
            "author_agent": agent_a.agent_id,
            "visual_path": skill_path,
            "completion_time": time_a
        })

        await asyncio.sleep(1)

        # Create Agent B (Learner)
        agent_b = Agent(
            agent_id="agent_beta",
            name="Agent Beta (Learner)",
            position=Position(self.maze.spawn.x, self.maze.spawn.y)
        )
        self.add_agent(agent_b)

        # Broadcast skill transfer animation
        await self.broadcast_event("skill_transfer", {
            "from_agent": agent_a.agent_id,
            "to_agent": agent_b.agent_id,
            "skill_name": "Maze Navigation Strategy"
        })

        await asyncio.sleep(1)

        # Agent B: Execute learned skill
        print("📍 Agent Beta: Using learned skill...")
        time_b = await self.execute_skill(agent_b, skill_path)

        print(f"✅ Agent Beta completed in {time_b:.2f}s with {len(agent_b.path_history)} steps")

        # Calculate improvement
        improvement = ((time_a - time_b) / time_a) * 100 if time_a > 0 else 0

        print(f"📊 Improvement: {improvement:.1f}% faster")

        # Broadcast comparison
        await self.broadcast_event("demo_complete", {
            "agent_a": {
                "name": agent_a.name,
                "time": time_a,
                "steps": len(agent_a.path_history),
                "strategy": "random_exploration"
            },
            "agent_b": {
                "name": agent_b.name,
                "time": time_b,
                "steps": len(agent_b.path_history),
                "strategy": "learned_skill"
            },
            "improvement_percentage": improvement
        })

        return {
            "success": True,
            "agent_a_time": time_a,
            "agent_b_time": time_b,
            "improvement_percentage": improvement,
            "agent_a_steps": len(agent_a.path_history),
            "agent_b_steps": len(agent_b.path_history)
        }

    async def run_agent_alpha_only(self, use_pathfinding: bool = True, algorithm: str = "bfs") -> Dict:
        """
        Run Agent Alpha only (Phase 1 & 2) - HUMAN PAUSE HERE

        Args:
            use_pathfinding: If True, use pathfinding algorithm. If False, use random walk.
            algorithm: Pathfinding algorithm to use ("bfs", "dfs", "astar", "dijkstra")
        """
        print("🎬 Starting Agent Alpha (Explorer)...")

        # Create Agent A (Explorer)
        agent_a = Agent(
            agent_id="agent_alpha",
            name="Agent Alpha (Explorer)",
            position=Position(self.maze.spawn.x, self.maze.spawn.y)
        )
        self.add_agent(agent_a)

        # Agent A: Navigate using chosen strategy
        if use_pathfinding:
            print(f"📍 Agent Alpha: Using {algorithm.upper()} pathfinding...")
            time_a = await self.pathfinding_navigation(agent_a, algorithm=algorithm)
        else:
            print("📍 Agent Alpha: Starting random exploration...")
            time_a = await self.random_walk(agent_a, max_steps=500)

        if time_a < 0:
            print("❌ Agent Alpha failed to complete")
            return {"error": "Agent A failed"}

        print(f"✅ Agent Alpha completed in {time_a:.2f}s with {len(agent_a.path_history)} steps")

        # Extract skill from Agent A's path
        skill_path = [{"x": p.x, "y": p.y} for p in agent_a.path_history]

        # Pause for effect
        await asyncio.sleep(2)

        # Broadcast skill extraction
        await self.broadcast_event("skill_extracted", {
            "from_agent": agent_a.agent_id,
            "skill_name": "Maze Navigation Strategy",
            "path_length": len(skill_path),
            "completion_time": time_a
        })

        # Save skill to MongoDB
        skill_id = await self.save_skill_to_db({
            "name": "L-Shaped Maze Navigation",
            "description": f"Efficient navigation strategy for L-shaped mazes. Learned from {agent_a.name}'s successful exploration.",
            "author_agent": agent_a.agent_id,
            "visual_path": skill_path,
            "completion_time": time_a
        })

        await asyncio.sleep(1)

        # Broadcast that Alpha is complete and waiting for user
        await self.broadcast_event("alpha_complete_waiting", {
            "agent_id": agent_a.agent_id,
            "completion_time": time_a,
            "steps": len(agent_a.path_history),
            "skill_id": skill_id,
            "message": "Agent Alpha complete! Click 'Run Agent Beta' to continue."
        })

        return {
            "success": True,
            "agent_a_time": time_a,
            "agent_a_steps": len(agent_a.path_history),
            "skill_path": skill_path,
            "skill_id": skill_id
        }

    async def run_agent_beta_only(self, skill_path: List[Dict], agent_alpha_time: float) -> Dict:
        """Run Agent Beta with learned skill (Phase 3 & 4)"""
        print("📍 Agent Beta: Starting with learned skill...")

        # Create Agent B (Learner)
        agent_b = Agent(
            agent_id="agent_beta",
            name="Agent Beta (Learner)",
            position=Position(self.maze.spawn.x, self.maze.spawn.y)
        )
        self.add_agent(agent_b)

        # Broadcast that Agent Beta is searching MongoDB for the skill
        await self.broadcast_event("skill_retrieved", {
            "agent_id": agent_b.agent_id,
            "agent_name": agent_b.name,
            "skill_name": "Maze Navigation Strategy",
            "description": "Learned navigation pattern from agent_alpha",
            "path_length": len(skill_path),
            "from_agent": "agent_alpha",
            "retrieval_method": "mongodb_vector_search"
        })

        await asyncio.sleep(2)  # Pause to show retrieval

        # Broadcast skill transfer animation
        await self.broadcast_event("skill_transfer", {
            "from_agent": "agent_alpha",
            "to_agent": agent_b.agent_id,
            "skill_name": "Maze Navigation Strategy"
        })

        await asyncio.sleep(1)

        # Agent B: Execute learned skill
        time_b = await self.execute_skill(agent_b, skill_path)

        print(f"✅ Agent Beta completed in {time_b:.2f}s with {len(agent_b.path_history)} steps")

        # Calculate improvement
        improvement = ((agent_alpha_time - time_b) / agent_alpha_time) * 100 if agent_alpha_time > 0 else 0

        print(f"📊 Improvement: {improvement:.1f}% faster")

        # Broadcast comparison
        await self.broadcast_event("demo_complete", {
            "agent_a": {
                "name": "Agent Alpha (Explorer)",
                "time": agent_alpha_time,
                "steps": len(skill_path),  # Alpha's step count
                "strategy": "random_exploration"
            },
            "agent_b": {
                "name": agent_b.name,
                "time": time_b,
                "steps": len(agent_b.path_history),
                "strategy": "learned_skill"
            },
            "improvement_percentage": improvement
        })

        return {
            "success": True,
            "agent_b_time": time_b,
            "agent_b_steps": len(agent_b.path_history),
            "improvement_percentage": improvement
        }

# ============================================================================
# HELPER FUNCTIONS FOR BACKEND INTEGRATION
# ============================================================================

def create_demo_maze() -> Maze:
    """Create the demo L-shaped maze"""
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
    return Maze(
        grid=grid,
        spawn=Position(1, 1),
        goal=Position(8, 7)
    )

async def run_simulation_with_websocket(maze_data: Dict, websocket_manager, db=None):
    """Run simulation with WebSocket broadcasting and MongoDB persistence"""
    maze = Maze(
        grid=maze_data['grid'],
        spawn=Position(**maze_data['spawn_point']),
        goal=Position(**maze_data['goal_point'])
    )

    sim = MazeSimulation(maze, websocket_manager, db)
    results = await sim.run_demo_sequence()
    return results

# ============================================================================
# STANDALONE TEST
# ============================================================================

async def main():
    """Test simulation standalone"""
    maze = create_demo_maze()
    sim = MazeSimulation(maze)
    results = await sim.run_demo_sequence()
    print("\n🎉 Demo Results:")
    print(f"   Agent A: {results['agent_a_time']:.2f}s ({results['agent_a_steps']} steps)")
    print(f"   Agent B: {results['agent_b_time']:.2f}s ({results['agent_b_steps']} steps)")
    print(f"   Improvement: {results['improvement_percentage']:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())

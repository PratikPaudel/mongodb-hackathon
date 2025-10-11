# backend/simulation_simple.py
"""
Simplified Maze Simulation for MirrorMinds Demo
This is a streamlined version focused on the hackathon demo.
For full PyGame visualization, see PRD_2.md
"""

import asyncio
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from datetime import datetime

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
    def __init__(self, maze: Maze, websocket_manager=None):
        self.maze = maze
        self.agents: List[Agent] = []
        self.manager = websocket_manager

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

                # Broadcast position update every 5 steps
                if steps % 5 == 0:
                    await self.broadcast_event("agent_position", {
                        "agent_id": agent.agent_id,
                        "position": {"x": agent.position.x, "y": agent.position.y},
                        "steps": steps
                    })

            steps += 1
            await asyncio.sleep(0.05)  # Slow down for demo visibility

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
            await asyncio.sleep(0.03)  # Faster than random walk

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

async def run_simulation_with_websocket(maze_data: Dict, websocket_manager):
    """Run simulation with WebSocket broadcasting"""
    maze = Maze(
        grid=maze_data['grid'],
        spawn=Position(**maze_data['spawn_point']),
        goal=Position(**maze_data['goal_point'])
    )

    sim = MazeSimulation(maze, websocket_manager)
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

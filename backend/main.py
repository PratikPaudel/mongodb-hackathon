# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import asyncio
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
from simulation_simple import run_simulation_with_websocket

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="MirrorMinds API",
    description="Multi-Agent Procedural Memory System",
    version="2.0.0"
)

# CORS - allow both local and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mongodb-hackathon.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
mongodb_client = AsyncIOMotorClient(MONGODB_URI)
db = mongodb_client["mirrorminds"]

# Voyage AI client (will be initialized if API key is provided)
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY", "")
voyage_client = None

if VOYAGE_API_KEY:
    try:
        import voyageai
        voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)
    except Exception as e:
        print(f"⚠️ Voyage AI initialization failed: {e}")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

manager = ConnectionManager()

# Demo state for human-in-the-loop flow
demo_state = {
    "maze": None,
    "agent_alpha_result": None,
    "skill_path": None,
    "skill_id": None,
    "in_progress": False
}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class Position(BaseModel):
    x: int
    y: int

class SkillCreate(BaseModel):
    name: str
    description: str
    skill_type: str
    maze_type: str
    visual_path: List[Dict]
    strategy: Dict
    author_agent: str
    tags: List[str] = []

class SkillSearchRequest(BaseModel):
    query: str
    maze_type: Optional[str] = None
    min_success_rate: float = 0.7
    limit: int = 5

class AgentCreate(BaseModel):
    agent_name: str
    agent_type: str
    color: Dict[str, int]

class TaskExecutionRequest(BaseModel):
    agent_id: str
    maze_id: str
    skill_id: Optional[str] = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def generate_embedding(text: str) -> List[float]:
    """Generate embedding using Voyage AI"""
    if not voyage_client:
        # Return dummy embedding for testing without API key
        print("⚠️ No Voyage AI client, returning dummy embedding")
        return np.random.rand(1024).tolist()

    try:
        result = voyage_client.embed(
            [text],
            model="voyage-3",
            input_type="document"
        )
        return result.embeddings[0]
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return np.random.rand(1024).tolist()

async def generate_query_embedding(text: str) -> List[float]:
    """Generate query embedding using Voyage AI"""
    if not voyage_client:
        return np.random.rand(1024).tolist()

    try:
        result = voyage_client.embed(
            [text],
            model="voyage-3",
            input_type="query"
        )
        return result.embeddings[0]
    except Exception as e:
        print(f"❌ Query embedding error: {e}")
        return np.random.rand(1024).tolist()

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "MirrorMinds API v2.0 🧠",
        "status": "running",
        "endpoints": {
            "skills": "/api/skills",
            "agents": "/api/agents",
            "mazes": "/api/mazes",
            "executions": "/api/executions",
            "analytics": "/api/analytics",
            "websocket": "/ws"
        }
    }

@app.get("/api/health")
async def health_check():
    """Enhanced health check with database status"""
    try:
        # Ping database
        await db.command("ping")
        db_status = "connected"
    except:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "websocket_connections": len(manager.active_connections),
        "voyage_ai": "configured" if voyage_client else "not configured"
    }

# ============================================================================
# SKILL ENDPOINTS
# ============================================================================

@app.get("/api/skills")
async def list_skills(
    skill_type: Optional[str] = None,
    maze_type: Optional[str] = None,
    min_success_rate: float = 0.0,
    limit: int = 20
):
    """List available skills with optional filters"""
    query = {"status": "active"}

    if skill_type:
        query["metadata.skill_type"] = skill_type
    if maze_type:
        query["metadata.maze_type"] = maze_type
    if min_success_rate > 0:
        query["stats.success_rate"] = {"$gte": min_success_rate}

    skills = await db.skills.find(query).sort("stats.total_uses", -1).limit(limit).to_list(length=limit)

    # Convert ObjectId to string
    for skill in skills:
        skill["_id"] = str(skill["_id"])

    return {
        "skills": skills,
        "count": len(skills),
        "filters": {
            "skill_type": skill_type,
            "maze_type": maze_type,
            "min_success_rate": min_success_rate
        }
    }

@app.post("/api/skills/search")
async def search_skills(request: SkillSearchRequest):
    """Semantic search for skills using vector embeddings"""

    # Generate query embedding
    query_embedding = await generate_query_embedding(request.query)

    # Build vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "description_embedding",
                "queryVector": query_embedding,
                "numCandidates": request.limit * 10,
                "limit": request.limit,
                "filter": {
                    "status": {"$eq": "active"},
                    "stats.success_rate": {"$gte": request.min_success_rate}
                }
            }
        },
        {
            "$project": {
                "skill_id": 1,
                "name": 1,
                "description": 1,
                "metadata": 1,
                "visual_path": 1,
                "strategy": 1,
                "stats": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    # Add maze_type filter if specified
    if request.maze_type:
        pipeline[0]["$vectorSearch"]["filter"]["metadata.maze_type"] = request.maze_type

    try:
        results = await db.skills.aggregate(pipeline).to_list(length=request.limit)

        for result in results:
            result["_id"] = str(result["_id"])

        return {
            "results": results,
            "count": len(results),
            "query": request.query
        }
    except Exception as e:
        # Fallback to text search if vector search fails
        print(f"⚠️ Vector search failed, using text search: {e}")
        text_results = await db.skills.find(
            {
                "$text": {"$search": request.query},
                "status": "active",
                "stats.success_rate": {"$gte": request.min_success_rate}
            }
        ).limit(request.limit).to_list(length=request.limit)

        for result in text_results:
            result["_id"] = str(result["_id"])
            result["score"] = 0.5  # Dummy score

        return {
            "results": text_results,
            "count": len(text_results),
            "query": request.query,
            "fallback": "text_search"
        }

@app.post("/api/skills/create")
async def create_skill(skill_data: SkillCreate, background_tasks: BackgroundTasks):
    """Create a new skill in the library"""

    # Generate embedding for description
    description_text = f"{skill_data.name} {skill_data.description}"
    embedding = await generate_embedding(description_text)

    # Build skill document
    skill_doc = {
        "schema_version": 1,
        "skill_id": f"skill_{skill_data.skill_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "version": 1,
        "name": skill_data.name,
        "description": skill_data.description,
        "description_embedding": embedding,
        "metadata": {
            "author_agent": skill_data.author_agent,
            "contributors": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "skill_type": skill_data.skill_type,
            "maze_type": skill_data.maze_type,
            "complexity": "simple",
            "tags": skill_data.tags
        },
        "visual_path": skill_data.visual_path,
        "strategy": skill_data.strategy,
        "stats": {
            "total_uses": 0,
            "successful_uses": 0,
            "success_rate": 1.0,
            "avg_completion_time_ms": 0,
            "avg_steps": len(skill_data.visual_path),
            "improvement_over_baseline": 0.0,
            "last_used": None
        },
        "relationships": {
            "parent_skill": None,
            "improved_by": [],
            "similar_skills": [],
            "used_in_combination_with": []
        },
        "applicable_to": {
            "maze_types": [skill_data.maze_type],
            "size_range": {"min": 5, "max": 50},
            "complexity": ["simple", "medium"]
        },
        "status": "active"
    }

    # Insert into database
    result = await db.skills.insert_one(skill_doc)
    skill_doc["_id"] = str(result.inserted_id)

    # Broadcast new skill to connected clients
    background_tasks.add_task(
        manager.broadcast,
        {
            "type": "skill_created",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "skill_id": skill_doc["skill_id"],
                "name": skill_doc["name"],
                "author": skill_data.author_agent
            }
        }
    )

    return {
        "success": True,
        "skill_id": skill_doc["skill_id"],
        "message": "Skill created successfully"
    }

@app.get("/api/skills/{skill_id}")
async def get_skill(skill_id: str):
    """Get detailed information about a specific skill"""
    skill = await db.skills.find_one({"skill_id": skill_id})

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill["_id"] = str(skill["_id"])
    return skill

# ============================================================================
# AGENT ENDPOINTS
# ============================================================================

@app.get("/api/agents")
async def list_agents(status: Optional[str] = None):
    """List all registered agents"""
    query = {}
    if status:
        query["current_state.status"] = status

    agents = await db.agents.find(query).to_list(length=100)

    for agent in agents:
        agent["_id"] = str(agent["_id"])

    return {
        "agents": agents,
        "count": len(agents)
    }

@app.post("/api/agents/create")
async def create_agent(agent_data: AgentCreate):
    """Register a new agent"""
    agent_doc = {
        "agent_id": f"agent_{agent_data.agent_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "agent_name": agent_data.agent_name,
        "agent_type": agent_data.agent_type,
        "color": agent_data.color,
        "current_state": {
            "status": "idle",
            "position": {"x": 0, "y": 0},
            "facing_direction": "right",
            "current_task": None
        },
        "memory": {
            "known_skills": [],
            "currently_executing_skill": None,
            "learned_from_agents": [],
            "taught_to_agents": []
        },
        "performance": {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "success_rate": 0.0,
            "avg_completion_time_ms": 0,
            "skills_contributed": 0,
            "skills_learned": 0,
            "total_runtime_ms": 0
        },
        "last_heartbeat": datetime.now(),
        "created_at": datetime.now()
    }

    result = await db.agents.insert_one(agent_doc)
    agent_doc["_id"] = str(result.inserted_id)

    # Broadcast new agent
    await manager.broadcast({
        "type": "agent_created",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "agent_id": agent_doc["agent_id"],
            "name": agent_data.agent_name,
            "type": agent_data.agent_type
        }
    })

    return {
        "success": True,
        "agent_id": agent_doc["agent_id"]
    }

# ============================================================================
# MAZE ENDPOINTS
# ============================================================================

@app.get("/api/mazes")
async def list_mazes():
    """List available mazes"""
    mazes = await db.mazes.find({}).to_list(length=50)

    for maze in mazes:
        maze["_id"] = str(maze["_id"])

    return {
        "mazes": mazes,
        "count": len(mazes)
    }

@app.get("/api/mazes/{maze_id}")
async def get_maze(maze_id: str):
    """Get maze definition"""
    maze = await db.mazes.find_one({"maze_id": maze_id})

    if not maze:
        raise HTTPException(status_code=404, detail="Maze not found")

    maze["_id"] = str(maze["_id"])
    return maze

# ============================================================================
# EXECUTION ENDPOINTS
# ============================================================================

@app.post("/api/execute")
async def execute_task(request: TaskExecutionRequest, background_tasks: BackgroundTasks):
    """Start agent task execution"""

    # Validate agent exists
    agent = await db.agents.find_one({"agent_id": request.agent_id})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Validate maze exists
    maze = await db.mazes.find_one({"maze_id": request.maze_id})
    if not maze:
        raise HTTPException(status_code=404, detail="Maze not found")

    # Create execution record
    execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.agent_id[-6:]}"

    execution_doc = {
        "execution_id": execution_id,
        "agent_id": request.agent_id,
        "skill_id": request.skill_id,
        "task_id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "task_context": {
            "maze_id": request.maze_id,
            "maze_type": maze.get("type"),
            "maze_size": maze.get("dimensions"),
            "start_position": maze.get("spawn_point"),
            "goal_position": maze.get("goal_point")
        },
        "execution": {
            "started_at": datetime.now(),
            "completed_at": None,
            "duration_ms": None,
            "status": "running",
            "steps_taken": 0,
            "collisions": 0,
            "backtracks": 0
        },
        "path_taken": [],
        "performance_comparison": {},
        "feedback": {}
    }

    result = await db.executions.insert_one(execution_doc)

    # Broadcast task start
    await manager.broadcast({
        "type": "task_started",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "execution_id": execution_id,
            "agent_id": request.agent_id,
            "maze_id": request.maze_id,
            "skill_id": request.skill_id
        }
    })

    return {
        "success": True,
        "execution_id": execution_id,
        "message": "Task execution started"
    }

@app.get("/api/executions")
async def list_executions(
    agent_id: Optional[str] = None,
    limit: int = 20
):
    """List execution history"""
    query = {}
    if agent_id:
        query["agent_id"] = agent_id

    executions = await db.executions.find(query).sort("execution.started_at", -1).limit(limit).to_list(length=limit)

    for execution in executions:
        execution["_id"] = str(execution["_id"])

    return {
        "executions": executions,
        "count": len(executions)
    }

# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/leaderboard")
async def get_leaderboard():
    """Get top-performing skills"""
    skills = await db.skills.find(
        {"status": "active"}
    ).sort("stats.improvement_over_baseline", -1).limit(10).to_list(length=10)

    for skill in skills:
        skill["_id"] = str(skill["_id"])

    return {
        "top_skills": skills,
        "count": len(skills)
    }

@app.get("/api/analytics/agents")
async def get_agent_analytics():
    """Get agent performance analytics"""
    agents = await db.agents.find({}).to_list(length=100)

    for agent in agents:
        agent["_id"] = str(agent["_id"])

    # Calculate aggregate stats
    total_tasks = sum(a["performance"]["tasks_completed"] for a in agents)
    avg_success_rate = sum(a["performance"]["success_rate"] for a in agents) / len(agents) if agents else 0

    return {
        "agents": agents,
        "aggregate": {
            "total_tasks": total_tasks,
            "avg_success_rate": avg_success_rate,
            "total_agents": len(agents)
        }
    }

# ============================================================================
# DEMO ENDPOINT
# ============================================================================

@app.post("/api/demo/start")
async def start_demo(background_tasks: BackgroundTasks):
    """LEGACY: Start the full automated demonstration sequence"""

    # Get the demo maze
    maze = await db.mazes.find_one({"maze_id": "maze_labyrinth_challenge"})

    if not maze:
        raise HTTPException(status_code=404, detail="Demo maze not found")

    # Broadcast demo start event
    await manager.broadcast({
        "type": "demo_starting",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "message": "MirrorMinds demo sequence starting...",
            "maze_id": maze["maze_id"]
        }
    })

    # Run simulation in background
    async def run_demo():
        try:
            results = await run_simulation_with_websocket(maze, manager, db)
            print(f"✅ Demo completed: {results}")
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            await manager.broadcast({
                "type": "demo_failed",
                "timestamp": datetime.now().isoformat(),
                "data": {"error": str(e)}
            })

    # Schedule the demo to run in background
    background_tasks.add_task(run_demo)

    return {
        "success": True,
        "message": "Demo started - watch the Activity Feed for real-time updates!",
        "maze_id": maze["maze_id"]
    }

@app.post("/api/demo/run-alpha")
async def run_agent_alpha(background_tasks: BackgroundTasks):
    """Run Agent Alpha only (Phase 1 & 2) - Human-in-the-loop"""

    if demo_state["in_progress"]:
        raise HTTPException(status_code=400, detail="Demo already in progress")

    # Get the demo maze
    maze = await db.mazes.find_one({"maze_id": "maze_labyrinth_challenge"})

    if not maze:
        raise HTTPException(status_code=404, detail="Demo maze not found")

    # Store maze for later
    demo_state["maze"] = maze
    demo_state["in_progress"] = True

    # Broadcast demo start event
    await manager.broadcast({
        "type": "demo_starting",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "message": "Starting Agent Alpha...",
            "maze_id": maze["maze_id"]
        }
    })

    # Run Agent Alpha in background
    async def run_alpha():
        try:
            from simulation_simple import Maze, Position, MazeSimulation

            maze_obj = Maze(
                grid=maze['grid'],
                spawn=Position(**maze['spawn_point']),
                goal=Position(**maze['goal_point'])
            )

            sim = MazeSimulation(maze_obj, manager, db)
            results = await sim.run_agent_alpha_only()

            if results.get("success"):
                # Store results for Agent Beta
                demo_state["agent_alpha_result"] = results
                demo_state["skill_path"] = results["skill_path"]
                demo_state["skill_id"] = results["skill_id"]

                print(f"✅ Agent Alpha completed: {results}")
            else:
                demo_state["in_progress"] = False

        except Exception as e:
            print(f"❌ Agent Alpha failed: {e}")
            demo_state["in_progress"] = False
            await manager.broadcast({
                "type": "demo_failed",
                "timestamp": datetime.now().isoformat(),
                "data": {"error": str(e)}
            })

    # Schedule Alpha to run in background
    background_tasks.add_task(run_alpha)

    return {
        "success": True,
        "message": "Agent Alpha starting...",
        "maze_id": maze["maze_id"]
    }

@app.post("/api/demo/run-beta")
async def run_agent_beta(background_tasks: BackgroundTasks):
    """Run Agent Beta with learned skill (Phase 3 & 4) - Human-in-the-loop"""

    if not demo_state["in_progress"]:
        raise HTTPException(status_code=400, detail="No demo in progress. Run Agent Alpha first.")

    if not demo_state["agent_alpha_result"]:
        raise HTTPException(status_code=400, detail="Agent Alpha has not completed yet")

    # Run Agent Beta in background
    async def run_beta():
        try:
            from simulation_simple import Maze, Position, MazeSimulation

            maze = demo_state["maze"]
            maze_obj = Maze(
                grid=maze['grid'],
                spawn=Position(**maze['spawn_point']),
                goal=Position(**maze['goal_point'])
            )

            sim = MazeSimulation(maze_obj, manager, db)
            results = await sim.run_agent_beta_only(
                demo_state["skill_path"],
                demo_state["agent_alpha_result"]["agent_a_time"],
                demo_state["agent_alpha_result"]["agent_a_steps"]
            )

            print(f"✅ Agent Beta completed: {results}")

            # Clear demo state
            demo_state["in_progress"] = False
            demo_state["agent_alpha_result"] = None
            demo_state["skill_path"] = None
            demo_state["skill_id"] = None

        except Exception as e:
            print(f"❌ Agent Beta failed: {e}")
            demo_state["in_progress"] = False
            await manager.broadcast({
                "type": "demo_failed",
                "timestamp": datetime.now().isoformat(),
                "data": {"error": str(e)}
            })

    # Schedule Beta to run in background
    background_tasks.add_task(run_beta)

    return {
        "success": True,
        "message": "Agent Beta starting with learned skill..."
    }

# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive commands from client
            data = await websocket.receive_json()
            command_type = data.get("type")

            if command_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })

            elif command_type == "subscribe":
                # Client subscribes to specific events
                await websocket.send_json({
                    "type": "subscribed",
                    "timestamp": datetime.now().isoformat(),
                    "message": "You are now subscribed to MirrorMinds events"
                })

            elif command_type == "get_stats":
                # Send current system stats
                agent_count = await db.agents.count_documents({})
                skill_count = await db.skills.count_documents({"status": "active"})
                execution_count = await db.executions.count_documents({})

                await websocket.send_json({
                    "type": "stats",
                    "data": {
                        "agents": agent_count,
                        "skills": skill_count,
                        "executions": execution_count,
                        "timestamp": datetime.now().isoformat()
                    }
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data if needed"""
    print("🚀 MirrorMinds API starting up...")

    # Check if database is empty and seed with demo data
    skill_count = await db.skills.count_documents({})

    if skill_count == 0:
        print("📦 Seeding database with demo data...")
        await seed_demo_data()

    print("✅ MirrorMinds API ready!")

async def seed_demo_data():
    """Seed database with demo mazes and skills"""

    # Create complex demo maze - "Labyrinth Challenge"
    demo_maze = {
        "maze_id": "maze_labyrinth_challenge",
        "name": "Labyrinth Challenge",
        "type": "labyrinth",
        "difficulty": "medium",
        "dimensions": {"width": 15, "height": 15, "cell_size_px": 35},
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "spawn_point": {"x": 1, "y": 1},
        "goal_point": {"x": 13, "y": 13},
        "created_at": datetime.now()
    }

    await db.mazes.insert_one(demo_maze)
    print("✅ Demo maze created: Labyrinth Challenge")

# ============================================================================
# KEEP-ALIVE (from your existing setup)
# ============================================================================

@app.on_event("startup")
async def startup_keep_alive():
    """Start keep-alive ping for Render free tier"""
    asyncio.create_task(keep_alive_ping())

async def keep_alive_ping():
    """Ping self every 14 minutes to prevent spin-down"""
    import httpx
    await asyncio.sleep(60)  # Wait 1 minute before starting

    while True:
        await asyncio.sleep(14 * 60)  # 14 minutes
        try:
            async with httpx.AsyncClient() as client:
                await client.get("https://mongodb-hackathon.onrender.com/api/health", timeout=10.0)
            print("🏓 Keep-alive ping sent")
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# MIRRORMINDS: COMPLETE PRD & TECHNICAL IMPLEMENTATION GUIDE
## Multi-Agent System with Shared Procedural Memory - 2D Simulation Version

**Project:** MongoDB Agentic Memory Hackathon
**Version:** 2.0 (2D Simulation Approach)
**Last Updated:** October 11, 2025 - 1:50 PM
**Target:** 12-16 hour hackathon build
**Implementation Status:** ✅ Phase 4 Complete (Backend + Frontend Running)
test
---

# 🚦 IMPLEMENTATION STATUS TRACKER

## ✅ COMPLETED (Phases 1-4)

### Infrastructure & Configuration
- ✅ Backend FastAPI server running (http://localhost:8000)
- ✅ Frontend Next.js app running (http://localhost:3000)
- ✅ MongoDB Atlas connected and tested
- ✅ Voyage AI embeddings configured
- ✅ Environment variables configured (.env files)
- ✅ WebSocket bidirectional communication active

### Backend API (15+ Endpoints)
- ✅ `/api/health` - System health with DB status
- ✅ `/api/skills` - List/create skills with filters
- ✅ `/api/skills/search` - Semantic search (vector + text fallback)
- ✅ `/api/agents` - List/create agents
- ✅ `/api/mazes` - List/retrieve maze definitions
- ✅ `/api/execute` - Start agent task execution
- ✅ `/api/executions` - Execution history
- ✅ `/api/analytics/leaderboard` - Top skills by improvement
- ✅ `/api/analytics/agents` - Agent performance stats
- ✅ `/ws` - WebSocket real-time events

### Frontend Dashboard
- ✅ AgentCard component (status, position, metrics)
- ✅ ActivityFeed component (real-time events with auto-scroll)
- ✅ SkillLibrary component (search, filter, display)
- ✅ PerformanceChart component (aggregate stats)
- ✅ WebSocket hook with auto-reconnect
- ✅ Responsive mobile-friendly layout

### Simulation Engine (simulation_simple.py)
- ✅ Maze class with grid representation
- ✅ Agent class with position tracking
- ✅ Random walk algorithm (baseline - slow)
- ✅ Skill execution algorithm (optimized - fast)
- ✅ Path extraction and skill creation
- ✅ WebSocket event broadcasting
- ✅ Standalone testing capability

### Database & Demo Data
- ✅ Database: `mirrorminds` (MongoDB Atlas)
- ✅ Collections: `skills`, `agents`, `mazes`, `executions`
- ✅ Demo maze seeded: L-shaped Easy (10x10 grid)
- ✅ 3 demo agents: Alpha, Beta, Gamma

## ⚠️ IN PROGRESS

### MongoDB Configuration
- [ ] **Vector Search Index** (user action required)
  - Name: `skill_semantic_search`
  - Collection: `skills`
  - Field: `description_embedding`
  - Dimensions: 1024
  - See: PROGRESS_MIRRORMINDS.md Section 📚

## 🔲 NOT IMPLEMENTED (Phase 5+)

### Critical for Demo
- [ ] `/api/demo/start` endpoint
- [ ] Simulation triggered from API
- [ ] Frontend "Start Demo" button
- [ ] Full automation (Agent A → extract → Agent B)

### Optional/Stretch Goals
- [ ] PyGame visualization window
- [ ] Skill versioning (v1 → v2 → v3)
- [ ] Skill evolution tree visualization
- [ ] Multi-maze transfer learning
- [ ] LangGraph agent coordination
- [ ] Agent personalities
- [ ] Production deployment (Render + Vercel)

---

# EXECUTIVE SUMMARY

MirrorMinds is a visual multi-agent system where AI agents learn navigation strategies and teach each other through a shared procedural memory marketplace. Agents navigate 2D mazes, save successful strategies as "skills," and other agents discover and adapt these skills—demonstrating collective intelligence through dramatic visual improvement (42s → 9s completion time).

**Core Innovation:** Agents don't just share data—they share executable strategies with visual proof of learning.

**Technology Stack:**
- **Frontend:** Next.js 14 (existing setup) + PyGame visualization (embedded or separate window)
- **Backend:** FastAPI (existing) + LangGraph for agent coordination
- **Database:** MongoDB Atlas with Vector Search
- **Embeddings:** Voyage AI (voyage-3 or voyage-code-3)
- **Visualization:** PyGame for 2D world, NetworkX for skill graphs
- **Real-time:** WebSocket for live updates

---

# PART 1: PRODUCT REQUIREMENTS DOCUMENT

## 1.1 PROBLEM STATEMENT

### The Challenge
AI agents operate in isolation, repeatedly solving similar problems without learning from each other's experiences. Each agent must discover solutions from scratch, leading to:

- **Wasted computational resources** on redundant problem-solving
- **Inconsistent performance** across similar tasks  
- **Slow collective improvement** as knowledge isn't shared
- **No emergent intelligence** despite parallel learning

### The Opportunity  
Create a visual demonstration where agents:
1. **Solve problems** (navigate mazes, gather resources, find paths)
2. **Extract strategies** from successful attempts as structured "skills"
3. **Share skills** through a searchable marketplace with embeddings
4. **Adapt and improve** strategies across different scenarios
5. **Compete** for the most valuable/reusable skills

### Why 2D Simulation Works for Hackathon
- **Immediate visual impact:** Judges see agents learning in real-time
- **Clear before/after:** 42 seconds vs 9 seconds is undeniable
- **Memorable:** Game-like demo stays in judges' minds
- **Scalable narrative:** "If they can learn mazes, imagine learning code/strategies/tactics"

---

## 1.2 USER STORIES

### Primary Persona: Hackathon Judge / Technical Evaluator

**As a judge, I want to:**
- See immediate visual proof that agents are learning from each other
- Understand the system's value in under 3 minutes
- Witness measurable improvement (time, efficiency, success rate)
- Feel confident the technology scales beyond the demo

### User Journey: Maze Navigation Learning

**Scene 1: The Struggle**
1. Agent A spawns in a maze with no prior knowledge
2. Wanders randomly, hits dead ends, backtracks repeatedly
3. Eventually finds the goal after 42 seconds
4. **Audience feels:** "This is inefficient and relatable"

**Scene 2: The Insight**
1. System analyzes Agent A's successful path
2. Extracts a reusable strategy: "Left-wall following in L-shaped corridors"
3. Stores as a skill with metadata and embedding
4. **Audience feels:** "Ah, it's learning from experience"

**Scene 3: The Discovery**
1. Agent B spawns in a similar (but not identical) maze
2. Queries the skill marketplace: "Need navigation strategy"
3. Discovers Agent A's skill via semantic search
4. **Audience feels:** "This is agent-to-agent knowledge transfer"

**Scene 4: The Mastery**
1. Agent B adapts the skill to its specific maze layout
2. Navigates efficiently in 9 seconds (78% improvement)
3. Side-by-side comparison highlights the dramatic difference
4. **Audience feels:** "Wow, this is collective intelligence"

**Scene 5: The Evolution**
1. Agent C improves the skill with better turn timing
2. Skill versions shown in evolution tree (v1 → v2 → v3)
3. Leaderboard shows most popular/successful skills
4. **Audience feels:** "This creates emergent optimization"

---

## 1.3 TECHNICAL REQUIREMENTS

### Functional Requirements

**FR1: 2D Simulation Environment**
- Render navigable 2D maze with walls, paths, goals
- Support multiple agent instances with distinct colors
- Show agent movement with smooth animations
- Display real-time metrics (time, steps, collisions)
- Support 3+ different maze layouts (easy/medium/hard)

**FR2: Agent Navigation Intelligence**
- Random exploration baseline (no prior knowledge)
- Pathfinding using learned strategies
- Strategy adaptation to new maze configurations
- Real-time decision-making visible in UI

**FR3: Skill Extraction & Storage**
- Automatically convert successful paths into skills
- Structure: `{strategy_type, path_coordinates, conditions, performance_metrics}`
- Generate embeddings for skill descriptions
- Store in MongoDB with full provenance tracking
- Support skill versioning and improvement history

**FR4: Semantic Skill Discovery**
- Embed agent queries using Voyage AI
- Vector search skills via MongoDB Atlas Vector Search
- Filter by success_rate, maze_type, complexity
- Return top-k most relevant skills with similarity scores

**FR5: Skill Transfer Visualization**
- Animate glowing particle effect from Agent A → Agent B
- Show skill card appearing in Agent B's "memory"
- Display DAG (directed acyclic graph) of skill relationships
- Highlight skill improvements/forks in evolution tree

**FR6: Performance Comparison Dashboard**
- Real-time metrics: completion time, steps taken, success rate
- Side-by-side before/after comparison
- Leaderboard of top-performing skills
- Historical trend chart (agents improving over time)

**FR7: Competitive Skill Marketplace (Stretch)**
- Agents "bid" tokens for high-value skills
- Skills priced by popularity and success rate
- Dynamic pricing based on demand
- Marketplace transaction log

### Non-Functional Requirements

**NFR1: Performance**
- Agent movement rendering: 60 FPS minimum
- Skill discovery: <200ms for vector search
- WebSocket latency: <50ms for real-time updates
- Support 5+ concurrent agent simulations

**NFR2: Demo Reliability**
- Zero-crash requirement during 3-minute presentation
- Hardcoded demo scenarios for reproducibility
- Backup video recorded and ready
- Graceful degradation if MongoDB connection fails

**NFR3: Visual Polish**
- Professional color scheme (not default colors)
- Smooth animations (no jerky movement)
- Clear visual hierarchy (important info stands out)
- Mobile-friendly dashboard (stretch goal)

**NFR4: Open Source Compliance**
- All dependencies must be open source
- Code published on GitHub during hackathon
- Clear MIT/Apache 2.0 license
- No proprietary APIs (Voyage AI has free tier)

---

## 1.4 SUCCESS METRICS

### Demo Success Criteria (Hackathon Judging)

**Demo Power (50% of score):**
- ✅ Live agents moving in 2D maze
- ✅ Visible skill transfer animation (glowing particles)
- ✅ Clear 42s → 9s improvement shown side-by-side
- ✅ No crashes during 3-minute demo
- ✅ Judges say "wow" at the before/after moment

**Impact (25% of score):**
- ✅ 70%+ improvement in task completion time
- ✅ Clear explanation of real-world applications
- ✅ Measurable success rate increase (50% → 90%+)
- ✅ Scalability story beyond mazes

**Creativity (15% of score):**
- ✅ Novel visualization of procedural memory
- ✅ Game-like competitive element (marketplace)
- ✅ Evolution tree showing emergent optimization
- ✅ Judges haven't seen this approach before

**Pitch (10% of score):**
- ✅ 3-minute presentation rehearsed 5+ times
- ✅ 1-minute backup video ready
- ✅ Clear problem → solution → impact narrative
- ✅ Confident team delivery with smooth transitions

### Technical Validation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Skill Reuse Rate** | >60% | % of tasks using shared skills vs. learning from scratch |
| **Time Improvement** | >70% | Average reduction in task completion time with skills |
| **Success Rate** | >90% | % of skill transfers that improve performance |
| **Search Relevance** | >80% | Top-3 accuracy for skill matching |
| **System Uptime** | 100% | Zero crashes during demo |

### Post-Hackathon Growth Metrics (Optional)

- Skill library growth rate (skills/day)
- Agent diversity (unique agent contributors)
- Skill evolution depth (max version number)
- Community engagement (GitHub stars, forks)

---

## 1.5 OUT OF SCOPE (For Hackathon MVP)

### Explicitly NOT Building
- ❌ User authentication or multi-tenancy
- ❌ Production-grade security
- ❌ Complex 3D environments
- ❌ Real robotics integration (simulation only)
- ❌ Multiplayer/collaborative maze solving
- ❌ Natural language agent communication
- ❌ Mobile native apps
- ❌ Extensive test coverage (focus on demo reliability)
- ❌ Advanced AI training (RL, neural nets)
- ❌ Integration with external dev tools

### Post-Hackathon Features
- Advanced pathfinding algorithms (A*, Dijkstra)
- Multi-objective optimization (time + energy)
- Adversarial agents (blocking competitors)
- Complex resource management scenarios
- Real-world problem domains (code, trading, logistics)

---

# PART 2: SYSTEM ARCHITECTURE

## 2.1 HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    NEXT.JS DASHBOARD                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Live Feed  │  │ Skill Market │  │ Performance      │  │
│  │  (PyGame    │  │ Browser      │  │ Comparison       │  │
│  │   embed)    │  └──────────────┘  └──────────────────┘  │
│  └─────────────┘                                           │
│         │                 │                    │            │
│         └─────────────────┴────────────────────┘            │
│                          │                                  │
│                    WebSocket + REST API                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   FASTAPI BACKEND                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ REST API     │  │ WebSocket    │  │ Voyage AI       │  │
│  │ Endpoints    │  │ Manager      │  │ Embeddings      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                            │                                │
│  ┌────────────────────────┴────────────────────────────┐   │
│  │          LANGGRAPH AGENT ORCHESTRATOR                │   │
│  │  ┌────────────┐ ┌─────────────┐ ┌──────────────┐   │   │
│  │  │  Agent A   │ │   Agent B   │ │   Agent C    │   │   │
│  │  │ (Explorer) │ │  (Learner)  │ │ (Optimizer)  │   │   │
│  │  └────────────┘ └─────────────┘ └──────────────┘   │   │
│  │         │              │                │           │   │
│  │         └──────────────┴────────────────┘           │   │
│  │                      │                              │   │
│  │            Skill Registry & Executor                │   │
│  └─────────────────────┬───────────────────────────────┘   │
└────────────────────────┼───────────────────────────────────┘
                         │
┌────────────────────────┴───────────────────────────────────┐
│              PYGAME SIMULATION ENGINE                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Maze       │  │   Agents     │  │   Animation     │  │
│  │   Renderer   │  │   Manager    │  │   System        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────┴───────────────────────────────────┐
│                 MONGODB ATLAS                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │    skills    │  │   agents     │  │   executions    │  │
│  │  (with       │  │   (state)    │  │   (history)     │  │
│  │  embeddings) │  │              │  │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│         │                 │                    │            │
│    Vector Search    Agent State        Performance Logs    │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

**Next.js Dashboard:**
- Display PyGame simulation (embedded iframe or separate window)
- Show skill marketplace with search interface
- Real-time performance metrics and comparisons
- Leaderboard and evolution tree visualization
- Handle user interactions (start simulation, filter skills)

**FastAPI Backend:**
- Expose REST API for skill CRUD operations
- Manage WebSocket connections for real-time streaming
- Orchestrate LangGraph agents
- Generate embeddings via Voyage AI
- Query MongoDB for skill discovery

**LangGraph Agents:**
- Execute navigation tasks in PyGame environment
- Discover relevant skills from shared library
- Execute learned strategies with adaptation
- Contribute successful paths back to library
- Report progress via WebSocket

**PyGame Simulation:**
- Render 2D maze environment with walls/paths/goals
- Animate agent movement with smooth transitions
- Show visual skill transfer effects (glowing particles)
- Display real-time agent state and metrics

**MongoDB Atlas:**
- Store skills with embeddings and metadata
- Provide vector search for semantic skill matching
- Track agent state and execution history
- Maintain skill versioning and evolution tree

---

## 2.2 DATA MODELS

### Skill Document Schema

```javascript
{
  "_id": ObjectId("671234567890abcdef123456"),
  "schema_version": 1,
  "skill_id": "skill_maze_nav_left_wall_001",
  "version": 2,
  "name": "Left-Wall Following Navigation",
  "description": "Follow the left wall to navigate L-shaped corridors and simple mazes. Works best in mazes with consistent wall structure.",
  
  // Vector embedding for semantic search
  "description_embedding": [0.023, -0.456, 0.789, ...],  // 1024 dims (Voyage AI)
  
  "metadata": {
    "author_agent": "agent_alpha_001",
    "contributors": ["agent_beta_002"],
    "created_at": ISODate("2024-10-11T10:00:00Z"),
    "updated_at": ISODate("2024-10-11T14:30:00Z"),
    "skill_type": "navigation",
    "maze_type": "l_shaped",
    "complexity": "simple",
    "tags": ["wall_following", "left_bias", "corridor_navigation"]
  },
  
  // Visual representation of the learned path
  "visual_path": [
    {"x": 0, "y": 0, "direction": "right"},
    {"x": 1, "y": 0, "direction": "right"},
    {"x": 2, "y": 0, "direction": "down"},
    {"x": 2, "y": 1, "direction": "down"},
    {"x": 2, "y": 2, "direction": "right", "is_goal": true}
  ],
  
  // Executable strategy (simplified 3-step procedure)
  "strategy": {
    "algorithm": "wall_following",
    "rules": [
      {
        "condition": "wall_on_left",
        "action": "move_forward"
      },
      {
        "condition": "no_wall_on_left",
        "action": "turn_left_and_move"
      },
      {
        "condition": "wall_ahead",
        "action": "turn_right"
      }
    ],
    "parameters": {
      "preferred_direction": "left",
      "max_backtrack_steps": 5,
      "collision_threshold": 3
    }
  },
  
  // Performance statistics
  "stats": {
    "total_uses": 47,
    "successful_uses": 43,
    "success_rate": 0.915,
    "avg_completion_time_ms": 9200,
    "avg_steps": 12,
    "best_time_ms": 8100,
    "worst_time_ms": 15300,
    "improvement_over_baseline": 0.78,  // 78% faster than random
    "last_used": ISODate("2024-10-11T16:45:00Z")
  },
  
  // Skill relationships
  "relationships": {
    "parent_skill": "skill_basic_navigation",
    "improved_by": ["skill_maze_nav_left_wall_002"],
    "similar_skills": ["skill_right_wall_following", "skill_pledge_algorithm"],
    "used_in_combination_with": ["skill_dead_end_detection"]
  },
  
  // Applicability context
  "applicable_to": {
    "maze_types": ["l_shaped", "simple_corridor", "rectangular"],
    "size_range": {"min": 5, "max": 20},  // grid dimensions
    "complexity": ["simple", "medium"]
  },
  
  "status": "active"
}
```

### Agent State Schema

```javascript
{
  "_id": ObjectId("671234567890abcdef789012"),
  "agent_id": "agent_alpha_001",
  "agent_name": "Agent Alpha",
  "agent_type": "explorer",  // explorer, learner, optimizer
  "color": {"r": 255, "g": 100, "b": 100},  // RGB for visualization
  
  "current_state": {
    "status": "navigating",  // idle, navigating, learning, teaching
    "position": {"x": 2, "y": 3},
    "facing_direction": "right",
    "current_task": {
      "task_id": "task_maze_003",
      "maze_id": "maze_l_shaped_medium",
      "goal_position": {"x": 10, "y": 10},
      "started_at": ISODate("2024-10-11T16:50:00Z")
    }
  },
  
  "memory": {
    "known_skills": [
      "skill_maze_nav_left_wall_001",
      "skill_dead_end_detection"
    ],
    "currently_executing_skill": "skill_maze_nav_left_wall_001",
    "learned_from_agents": ["agent_beta_002"],
    "taught_to_agents": ["agent_gamma_003"]
  },
  
  "performance": {
    "tasks_completed": 23,
    "tasks_failed": 3,
    "success_rate": 0.885,
    "avg_completion_time_ms": 11400,
    "skills_contributed": 2,
    "skills_learned": 5,
    "total_runtime_ms": 262200
  },
  
  "last_heartbeat": ISODate("2024-10-11T16:51:00Z"),
  "created_at": ISODate("2024-10-11T10:00:00Z")
}
```

### Execution Record Schema

```javascript
{
  "_id": ObjectId("671234567890abcdef345678"),
  "execution_id": "exec_20241011_165100_abc123",
  "agent_id": "agent_beta_002",
  "skill_id": "skill_maze_nav_left_wall_001",
  "skill_version": 2,
  "task_id": "task_maze_003",
  
  "task_context": {
    "maze_id": "maze_l_shaped_medium",
    "maze_type": "l_shaped",
    "maze_size": {"width": 15, "height": 15},
    "start_position": {"x": 0, "y": 0},
    "goal_position": {"x": 10, "y": 10}
  },
  
  "execution": {
    "started_at": ISODate("2024-10-11T16:51:00Z"),
    "completed_at": ISODate("2024-10-11T16:51:09Z"),
    "duration_ms": 9200,
    "status": "success",  // success, failure, timeout
    "steps_taken": 12,
    "collisions": 0,
    "backtracks": 1
  },
  
  // Recorded path for analysis
  "path_taken": [
    {"x": 0, "y": 0, "timestamp_ms": 0},
    {"x": 1, "y": 0, "timestamp_ms": 800},
    {"x": 2, "y": 0, "timestamp_ms": 1600},
    // ... full path
  ],
  
  "performance_comparison": {
    "baseline_time_ms": 42000,  // random exploration
    "improvement_percentage": 0.78,
    "vs_skill_avg_time_ms": 9200,
    "deviation_from_avg": 0.0
  },
  
  "feedback": {
    "was_skill_helpful": true,
    "adaptation_required": false,
    "issues_encountered": []
  }
}
```

### Maze Definition Schema

```javascript
{
  "_id": ObjectId("671234567890abcdef901234"),
  "maze_id": "maze_l_shaped_medium",
  "name": "L-Shaped Medium Difficulty",
  "type": "l_shaped",
  "difficulty": "medium",
  
  "dimensions": {
    "width": 15,
    "height": 15,
    "cell_size_px": 40
  },
  
  // Grid representation (0 = path, 1 = wall)
  "grid": [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    // ... full grid definition
  ],
  
  "spawn_point": {"x": 1, "y": 1},
  "goal_point": {"x": 10, "y": 10},
  
  "created_at": ISODate("2024-10-11T09:00:00Z")
}
```

---

## 2.3 MONGODB INDEXES

```javascript
// Vector search index for semantic skill discovery
db.skills.createSearchIndex(
  "skill_semantic_search",
  "vectorSearch",
  {
    fields: [
      {
        type: "vector",
        path: "description_embedding",
        numDimensions: 1024,  // Voyage AI dimension
        similarity: "cosine"
      },
      { type: "filter", path: "metadata.skill_type" },
      { type: "filter", path: "metadata.maze_type" },
      { type: "filter", path: "metadata.complexity" },
      { type: "filter", path: "status" },
      { type: "filter", path: "stats.success_rate" }
    ]
  }
);

// Text search index for keyword matching
db.skills.createIndex(
  { 
    name: "text", 
    description: "text", 
    "metadata.tags": "text" 
  },
  { 
    weights: { name: 10, description: 5, "metadata.tags": 3 },
    name: "skill_text_search"
  }
);

// Performance indexes for skills
db.skills.createIndex({ skill_id: 1, version: -1 });
db.skills.createIndex({ "metadata.skill_type": 1, "stats.success_rate": -1 });
db.skills.createIndex({ "metadata.author_agent": 1, "metadata.created_at": -1 });
db.skills.createIndex({ status: 1, "stats.total_uses": -1 });
db.skills.createIndex({ "stats.improvement_over_baseline": -1 });

// Agent indexes
db.agents.createIndex({ agent_id: 1 }, { unique: true });
db.agents.createIndex({ "current_state.status": 1, "last_heartbeat": -1 });
db.agents.createIndex({ "performance.success_rate": -1 });

// Execution history indexes
db.executions.createIndex({ "execution.started_at": -1 });
db.executions.createIndex({ skill_id: 1, "execution.started_at": -1 });
db.executions.createIndex({ agent_id: 1, "execution.started_at": -1 });
db.executions.createIndex({ "execution.status": 1, "execution.duration_ms": 1 });

// Maze indexes
db.mazes.createIndex({ maze_id: 1 }, { unique: true });
db.mazes.createIndex({ type: 1, difficulty: 1 });
```

---

# PART 3: TECHNICAL IMPLEMENTATION

## 3.1 BACKEND IMPLEMENTATION (Building on Existing FastAPI)

### Updated main.py (Enhanced from Your Existing Setup)

```python
# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import asyncio
from datetime import datetime
import voyageai
import numpy as np

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

# Voyage AI client
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY", "")
voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY) if VOYAGE_API_KEY else None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ WebSocket connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
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
            self.active_connections.remove(conn)

manager = ConnectionManager()

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
        "message": "MirrorMinds API v2.0",
        "status": "running",
        "endpoints": {
            "skills": "/api/skills",
            "agents": "/api/agents",
            "mazes": "/api/mazes",
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
                "index": "skill_semantic_search",
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
            "complexity": "simple",  # Could be calculated
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
    
    # Start async simulation (would integrate with PyGame here)
    # background_tasks.add_task(run_agent_simulation, execution_id)
    
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
    
    # Create demo maze
    demo_maze = {
        "maze_id": "maze_l_shaped_easy",
        "name": "L-Shaped Easy",
        "type": "l_shaped",
        "difficulty": "easy",
        "dimensions": {"width": 10, "height": 10, "cell_size_px": 50},
        "grid": [
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
        ],
        "spawn_point": {"x": 1, "y": 1},
        "goal_point": {"x": 8, "y": 7},
        "created_at": datetime.now()
    }
    
    await db.mazes.insert_one(demo_maze)
    print("✅ Demo maze created")

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
    while True:
        await asyncio.sleep(14 * 60)  # 14 minutes
        try:
            async with httpx.AsyncClient() as client:
                await client.get("https://mongodb-hackathon.onrender.com/api/health")
            print("🏓 Keep-alive ping sent")
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Update requirements.txt

```txt
# backend/requirements.txt
fastapi==0.119.0
uvicorn[standard]==0.37.0
motor==3.3.2
pydantic==2.12.0
python-multipart==0.0.9
voyageai==0.2.3
numpy==1.26.4
httpx==0.27.0
pygame==2.5.2
networkx==3.2.1
python-dotenv==1.0.1
```

---

## 3.2 PYGAME SIMULATION ENGINE

### Create simulation.py

```python
# backend/simulation.py
import pygame
import asyncio
import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 40
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL_COLOR = (50, 50, 50)
PATH_COLOR = (200, 200, 200)
GOAL_COLOR = (100, 255, 100)
PARTICLE_COLOR = (255, 200, 50)

@dataclass
class Position:
    x: int
    y: int
    
    def to_pixel(self, cell_size: int) -> Tuple[int, int]:
        return (self.x * cell_size, self.y * cell_size)

@dataclass
class Agent:
    agent_id: str
    name: str
    position: Position
    color: Tuple[int, int, int]
    has_skill: bool = False
    path_history: List[Position] = None
    completion_time: float = 0.0
    status: str = "idle"  # idle, navigating, completed
    
    def __post_init__(self):
        if self.path_history is None:
            self.path_history = []

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

class Particle:
    """Visual particle for skill transfer animation"""
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        self.x, self.y = start
        self.target_x, self.target_y = end
        self.lifetime = 1.0  # seconds
        self.age = 0.0
        self.speed = 5.0
    
    def update(self, dt: float) -> bool:
        """Update particle position. Returns False when lifetime expires."""
        self.age += dt
        if self.age >= self.lifetime:
            return False
        
        # Move towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 2:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        
        return True
    
    def draw(self, screen: pygame.Surface):
        """Draw particle with fading alpha"""
        alpha = int(255 * (1 - self.age / self.lifetime))
        color = (*PARTICLE_COLOR, alpha)
        radius = int(5 * (1 - self.age / self.lifetime))
        if radius > 0:
            # Draw glowing circle
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)

class MazeSimulation:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("MirrorMinds - Maze Navigation")
        self.clock = pygame.time.Clock()
        self.agents: List[Agent] = []
        self.particles: List[Particle] = []
        self.running = True
    
    def add_agent(self, agent: Agent):
        """Add agent to simulation"""
        agent.position = Position(self.maze.spawn.x, self.maze.spawn.y)
        self.agents.append(agent)
    
    def draw_maze(self):
        """Draw maze walls and paths"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if self.maze.grid[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)  # Border
                else:  # Path
                    pygame.draw.rect(self.screen, PATH_COLOR, rect)
                    pygame.draw.rect(self.screen, (180, 180, 180), rect, 1)  # Border
        
        # Draw goal
        goal_rect = pygame.Rect(
            self.maze.goal.x * CELL_SIZE,
            self.maze.goal.y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(self.screen, GOAL_COLOR, goal_rect)
        pygame.draw.circle(
            self.screen,
            WHITE,
            (goal_rect.centerx, goal_rect.centery),
            CELL_SIZE // 3
        )
    
    def draw_agent(self, agent: Agent):
        """Draw agent as circle with label"""
        pixel_pos = agent.position.to_pixel(CELL_SIZE)
        center = (pixel_pos[0] + CELL_SIZE // 2, pixel_pos[1] + CELL_SIZE // 2)
        
        # Draw agent circle
        pygame.draw.circle(self.screen, agent.color, center, CELL_SIZE // 3)
        pygame.draw.circle(self.screen, BLACK, center, CELL_SIZE // 3, 2)  # Border
        
        # Draw skill indicator
        if agent.has_skill:
            # Glowing aura for agents with skills
            for i in range(3):
                alpha = 50 - i * 15
                radius = CELL_SIZE // 3 + 5 + i * 3
                pygame.draw.circle(self.screen, (*agent.color, alpha), center, radius, 2)
        
        # Draw agent name
        font = pygame.font.Font(None, 20)
        text = font.render(agent.name, True, BLACK)
        text_rect = text.get_rect(center=(center[0], center[1] - CELL_SIZE))
        self.screen.blit(text, text_rect)
        
        # Draw path history
        if len(agent.path_history) > 1:
            points = [p.to_pixel(CELL_SIZE) for p in agent.path_history]
            points = [(p[0] + CELL_SIZE // 2, p[1] + CELL_SIZE // 2) for p in points]
            pygame.draw.lines(self.screen, agent.color, False, points, 2)
    
    def draw_particles(self):
        """Draw skill transfer particles"""
        for particle in self.particles:
            particle.draw(self.screen)
    
    def animate_skill_transfer(self, from_agent: Agent, to_agent: Agent):
        """Create particle effect for skill transfer"""
        start_pos = from_agent.position.to_pixel(CELL_SIZE)
        end_pos = to_agent.position.to_pixel(CELL_SIZE)
        
        start_center = (start_pos[0] + CELL_SIZE // 2, start_pos[1] + CELL_SIZE // 2)
        end_center = (end_pos[0] + CELL_SIZE // 2, end_pos[1] + CELL_SIZE // 2)
        
        # Create multiple particles
        for _ in range(20):
            particle = Particle(start_center, end_center)
            self.particles.append(particle)
    
    async def random_walk(self, agent: Agent) -> float:
        """Agent performs random walk (no skill)"""
        agent.status = "navigating"
        start_time = pygame.time.get_ticks()
        steps = 0
        max_steps = 200
        
        while agent.position.x != self.maze.goal.x or agent.position.y != self.maze.goal.y:
            if steps >= max_steps:
                agent.status = "failed"
                return -1
            
            # Get walkable neighbors
            neighbors = self.maze.get_neighbors(agent.position)
            
            if neighbors:
                # Choose random neighbor
                next_pos = np.random.choice(neighbors)
                agent.position = next_pos
                agent.path_history.append(Position(next_pos.x, next_pos.y))
            
            steps += 1
            
            # Update display
            self.update_frame()
            await asyncio.sleep(0.1)  # Slow down for visibility
        
        agent.status = "completed"
        agent.completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
        return agent.completion_time
    
    async def execute_skill(self, agent: Agent, skill_path: List[Dict]) -> float:
        """Agent executes learned skill (fast path)"""
        agent.status = "navigating"
        agent.has_skill = True
        start_time = pygame.time.get_ticks()
        
        for step in skill_path:
            agent.position = Position(step['x'], step['y'])
            agent.path_history.append(Position(step['x'], step['y']))
            
            # Update display
            self.update_frame()
            await asyncio.sleep(0.05)  # Faster than random walk
            
            if agent.position.x == self.maze.goal.x and agent.position.y == self.maze.goal.y:
                break
        
        agent.status = "completed"
        agent.completion_time = (pygame.time.get_ticks() - start_time) / 1000.0
        return agent.completion_time
    
    def update_frame(self):
        """Update display for one frame"""
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Clear screen
        self.screen.fill(WHITE)
        
        # Draw everything
        self.draw_maze()
        for agent in self.agents:
            self.draw_agent(agent)
        self.draw_particles()
        
        # Update particles
        dt = self.clock.get_time() / 1000.0
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Draw performance metrics
        self.draw_metrics()
        ```python
        # Update display
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def draw_metrics(self):
        """Draw performance metrics overlay"""
        font = pygame.font.Font(None, 24)
        y_offset = 10
        
        for agent in self.agents:
            # Agent status
            status_text = f"{agent.name}: {agent.status}"
            if agent.completion_time > 0:
                status_text += f" ({agent.completion_time:.1f}s)"
            
            text = font.render(status_text, True, BLACK)
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
            
            # Draw colored indicator
            pygame.draw.circle(self.screen, agent.color, (500, y_offset - 20), 8)
    
    async def run_demo(self):
        """Run complete demo sequence"""
        print("🎬 Starting MirrorMinds Demo...")
        
        # Act 1: Agent A struggles
        agent_a = Agent(
            agent_id="agent_alpha",
            name="Agent A",
            position=Position(self.maze.spawn.x, self.maze.spawn.y),
            color=(255, 100, 100)
        )
        self.add_agent(agent_a)
        
        print("📍 Agent A: Random exploration...")
        time_a = await self.random_walk(agent_a)
        print(f"✅ Agent A completed in {time_a:.1f}s")
        
        await asyncio.sleep(2)  # Pause for effect
        
        # Act 2: Extract skill (visual only, actual extraction in backend)
        skill_path = agent_a.path_history.copy()
        
        # Act 3: Agent B discovers skill
        agent_b = Agent(
            agent_id="agent_beta",
            name="Agent B",
            position=Position(self.maze.spawn.x, self.maze.spawn.y),
            color=(100, 100, 255)
        )
        self.add_agent(agent_b)
        
        # Animate skill transfer
        self.animate_skill_transfer(agent_a, agent_b)
        await asyncio.sleep(1)
        
        print("📍 Agent B: Using learned skill...")
        time_b = await self.execute_skill(agent_b, [
            {"x": p.x, "y": p.y} for p in skill_path
        ])
        print(f"✅ Agent B completed in {time_b:.1f}s")
        
        # Act 4: Show comparison
        improvement = ((time_a - time_b) / time_a) * 100
        print(f"📊 Improvement: {improvement:.0f}%")
        
        # Keep window open
        await asyncio.sleep(5)
    
    def cleanup(self):
        """Cleanup pygame resources"""
        pygame.quit()

# ============================================================================
# INTEGRATION FUNCTIONS
# ============================================================================

async def run_simulation_with_websocket(maze_data: Dict, websocket_manager):
    """Run simulation and broadcast events via WebSocket"""
    
    # Create maze from data
    maze = Maze(
        grid=maze_data['grid'],
        spawn=Position(**maze_data['spawn_point']),
        goal=Position(**maze_data['goal_point'])
    )
    
    # Create simulation
    sim = MazeSimulation(maze)
    
    try:
        # Run demo
        await sim.run_demo()
    finally:
        sim.cleanup()

if __name__ == "__main__":
    # Test simulation standalone
    test_maze = Maze(
        grid=[
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
        ],
        spawn=Position(1, 1),
        goal=Position(8, 7)
    )
    
    sim = MazeSimulation(test_maze)
    asyncio.run(sim.run_demo())
```

---

## 3.3 FRONTEND IMPLEMENTATION (Building on Your Existing Next.js)

### Update app/page.tsx (Main Dashboard)

```typescript
// frontend/app/page.tsx
'use client';

import { useEffect, useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { SkillLibrary } from '@/components/SkillLibrary';
import { ActivityFeed } from '@/components/ActivityFeed';
import { PerformanceChart } from '@/components/PerformanceChart';
import { AgentCard } from '@/components/AgentCard';
import { useWebSocket } from '@/hooks/useWebSocket';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const WS_URL = API_URL.replace('http', 'ws') + '/ws';

interface Agent {
  agent_id: string;
  agent_name: string;
  agent_type: string;
  color: { r: number; g: number; b: number };
  current_state: {
    status: string;
    position: { x: number; y: number };
  };
  performance: {
    tasks_completed: number;
    success_rate: number;
  };
}

interface Skill {
  skill_id: string;
  name: string;
  description: string;
  metadata: {
    author_agent: string;
    skill_type: string;
    tags: string[];
  };
  stats: {
    success_rate: number;
    total_uses: number;
    improvement_over_baseline: number;
  };
}

export default function Dashboard() {
  const { isConnected, messages, sendMessage } = useWebSocket(WS_URL);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [demoRunning, setDemoRunning] = useState(false);

  // Fetch initial data
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setIsLoading(true);

      // Fetch agents
      const agentsRes = await fetch(`${API_URL}/api/agents`);
      const agentsData = await agentsRes.json();
      setAgents(agentsData.agents);

      // Fetch skills
      const skillsRes = await fetch(`${API_URL}/api/skills?limit=10`);
      const skillsData = await skillsRes.json();
      setSkills(skillsData.skills);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const startDemo = async () => {
    try {
      setDemoRunning(true);

      // Create agents if they don't exist
      if (agents.length === 0) {
        await createDemoAgents();
      }

      // Start simulation
      const response = await fetch(`${API_URL}/api/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_id: agents[0]?.agent_id || 'agent_alpha',
          maze_id: 'maze_l_shaped_easy',
          skill_id: null
        })
      });

      const data = await response.json();
      console.log('Demo started:', data);
    } catch (error) {
      console.error('Error starting demo:', error);
      setDemoRunning(false);
    }
  };

  const createDemoAgents = async () => {
    const agentConfigs = [
      { name: 'Agent Alpha', type: 'explorer', color: { r: 255, g: 100, b: 100 } },
      { name: 'Agent Beta', type: 'learner', color: { r: 100, g: 100, b: 255 } },
      { name: 'Agent Gamma', type: 'optimizer', color: { r: 100, g: 255, b: 100 } }
    ];

    for (const config of agentConfigs) {
      await fetch(`${API_URL}/api/agents/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_name: config.name,
          agent_type: config.type,
          color: config.color
        })
      });
    }

    await fetchData();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                🧠 MirrorMinds
              </h1>
              <p className="text-sm text-slate-600 mt-1">
                Multi-Agent Procedural Memory System
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              {/* Connection Status */}
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-sm text-slate-600">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>

              {/* Start Demo Button */}
              <Button
                onClick={startDemo}
                disabled={demoRunning || isLoading}
                size="lg"
                className="bg-blue-600 hover:bg-blue-700"
              >
                {demoRunning ? '🎬 Demo Running...' : '▶️ Start Demo'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
            <p className="mt-4 text-slate-600">Loading MirrorMinds...</p>
          </div>
        )}

        {!isLoading && (
          <div className="space-y-6">
            {/* Agent Cards Row */}
            <div>
              <h2 className="text-xl font-semibold text-slate-900 mb-4">
                Active Agents
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {agents.length > 0 ? (
                  agents.map((agent) => (
                    <AgentCard key={agent.agent_id} agent={agent} />
                  ))
                ) : (
                  <div className="col-span-3 text-center py-8 bg-white rounded-lg border border-slate-200">
                    <p className="text-slate-600">No agents yet. Click "Start Demo" to create agents.</p>
                  </div>
                )}
              </div>
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Skill Library (2 columns) */}
              <div className="lg:col-span-2">
                <SkillLibrary skills={skills} onRefresh={fetchData} />
              </div>

              {/* Activity Feed (1 column) */}
              <div className="lg:col-span-1">
                <ActivityFeed messages={messages} />
              </div>
            </div>

            {/* Performance Chart */}
            <div>
              <PerformanceChart agents={agents} />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto px-6 text-center text-sm text-slate-600">
          <p>MongoDB Agentic Memory Hackathon 2024 • Built with Next.js, FastAPI, PyGame, and LangGraph</p>
        </div>
      </footer>
    </div>
  );
}
```

### Create useWebSocket Hook

```typescript
// frontend/hooks/useWebSocket.ts
'use client';

import { useEffect, useState, useCallback, useRef } from 'react';

export interface WebSocketMessage {
  type: string;
  timestamp: string;
  data?: any;
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('✅ WebSocket connected');
        setIsConnected(true);
        socketRef.current = ws;

        // Send initial ping
        ws.send(JSON.stringify({ type: 'subscribe' }));
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          console.log('📨 WebSocket message:', message);
          
          setMessages((prev) => {
            // Keep only last 50 messages
            const newMessages = [...prev, message];
            return newMessages.slice(-50);
          });
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        console.log('❌ WebSocket disconnected');
        setIsConnected(false);
        socketRef.current = null;

        // Attempt reconnection after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect...');
          connect();
        }, 3000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
    }
  }, [url]);

  useEffect(() => {
    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect]);

  const sendMessage = useCallback((message: any) => {
    if (socketRef.current && isConnected) {
      socketRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected. Cannot send message.');
    }
  }, [isConnected]);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return { isConnected, messages, sendMessage, clearMessages };
}
```

### Create AgentCard Component

```typescript
// frontend/components/AgentCard.tsx
'use client';

import React from 'react';

interface Agent {
  agent_id: string;
  agent_name: string;
  agent_type: string;
  color: { r: number; g: number; b: number };
  current_state: {
    status: string;
    position?: { x: number; y: number };
  };
  performance: {
    tasks_completed: number;
    success_rate: number;
  };
}

export function AgentCard({ agent }: { agent: Agent }) {
  const statusColors = {
    idle: 'bg-slate-100 text-slate-700',
    navigating: 'bg-blue-100 text-blue-700',
    completed: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700'
  };

  const statusColor = statusColors[agent.current_state.status as keyof typeof statusColors] || 'bg-slate-100 text-slate-700';
  const agentColor = `rgb(${agent.color.r}, ${agent.color.g}, ${agent.color.b})`;

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm hover:shadow-md transition-shadow p-6">
      {/* Agent Header */}
      <div className="flex items-center gap-3 mb-4">
        <div
          className="w-12 h-12 rounded-full border-4 border-opacity-30 flex items-center justify-center font-bold text-white"
          style={{ 
            backgroundColor: agentColor,
            borderColor: agentColor
          }}
        >
          {agent.agent_name.charAt(agent.agent_name.length - 1)}
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-slate-900">{agent.agent_name}</h3>
          <p className="text-sm text-slate-600 capitalize">{agent.agent_type}</p>
        </div>
      </div>

      {/* Status Badge */}
      <div className="mb-4">
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${statusColor} capitalize`}>
          {agent.current_state.status}
        </span>
      </div>

      {/* Performance Stats */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-slate-600">Tasks Completed</span>
          <span className="font-semibold text-slate-900">{agent.performance.tasks_completed}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-slate-600">Success Rate</span>
          <span className="font-semibold text-slate-900">
            {(agent.performance.success_rate * 100).toFixed(0)}%
          </span>
        </div>
        {agent.current_state.position && (
          <div className="flex justify-between text-sm">
            <span className="text-slate-600">Position</span>
            <span className="font-mono text-xs text-slate-900">
              ({agent.current_state.position.x}, {agent.current_state.position.y})
            </span>
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div className="mt-4">
        <div className="w-full bg-slate-200 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all duration-300"
            style={{
              width: `${agent.performance.success_rate * 100}%`,
              backgroundColor: agentColor
            }}
          />
        </div>
      </div>
    </div>
  );
}
```

### Create SkillLibrary Component

```typescript
// frontend/components/SkillLibrary.tsx
'use client';

import React, { useState } from 'react';
import { Button } from './ui/button';

interface Skill {
  skill_id: string;
  name: string;
  description: string;
  metadata: {
    author_agent: string;
    skill_type: string;
    tags: string[];
  };
  stats: {
    success_rate: number;
    total_uses: number;
    improvement_over_baseline: number;
  };
}

export function SkillLibrary({ 
  skills, 
  onRefresh 
}: { 
  skills: Skill[];
  onRefresh: () => void;
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');

  const skillTypes = ['all', 'navigation', 'pathfinding', 'optimization'];

  const filteredSkills = skills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         skill.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedType === 'all' || skill.metadata.skill_type === selectedType;
    return matchesSearch && matchesType;
  });

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-slate-900">
          📚 Skill Library
        </h2>
        <Button 
          onClick={onRefresh}
          variant="outline"
          size="sm"
        >
          🔄 Refresh
        </Button>
      </div>

      {/* Search Bar */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search skills by name or description..."
          className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Type Filters */}
      <div className="flex gap-2 flex-wrap mb-6">
        {skillTypes.map(type => (
          <button
            key={type}
            onClick={() => setSelectedType(type)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedType === type
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            {type === 'all' ? 'All Skills' : type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      {/* Skills List */}
      <div className="space-y-4 max-h-[500px] overflow-y-auto">
        {filteredSkills.length > 0 ? (
          filteredSkills.map(skill => (
            <SkillCard key={skill.skill_id} skill={skill} />
          ))
        ) : (
          <div className="text-center py-12 text-slate-500">
            {skills.length === 0 ? (
              <div>
                <p className="text-lg font-medium">No skills in library yet</p>
                <p className="text-sm mt-2">Start the demo to create your first skills!</p>
              </div>
            ) : (
              <p>No skills match your search</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function SkillCard({ skill }: { skill: Skill }) {
  const improvement = skill.stats.improvement_over_baseline * 100;
  const successRate = skill.stats.success_rate * 100;

  return (
    <div className="border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer group">
      {/* Header */}
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">
          {skill.name}
        </h3>
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          successRate >= 90 ? 'bg-green-100 text-green-700' :
          successRate >= 70 ? 'bg-blue-100 text-blue-700' :
          'bg-yellow-100 text-yellow-700'
        }`}>
          {successRate.toFixed(0)}% success
        </span>
      </div>

      {/* Description */}
      <p className="text-sm text-slate-600 mb-3 line-clamp-2">
        {skill.description}
      </p>

      {/* Tags */}
      <div className="flex gap-2 flex-wrap mb-3">
        {skill.metadata.tags.slice(0, 3).map(tag => (
          <span
            key={tag}
            className="px-2 py-1 bg-slate-100 text-slate-700 rounded text-xs"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* Stats */}
      <div className="flex justify-between items-center text-xs text-slate-500">
        <span>
          📊 {skill.stats.total_uses} uses
        </span>
        <span>
          👤 {skill.metadata.author_agent}
        </span>
        {improvement > 0 && (
          <span className="text-green-600 font-medium">
            ⬆️ {improvement.toFixed(0)}% faster
          </span>
        )}
      </div>
    </div>
  );
}
```

### Create ActivityFeed Component

```typescript
// frontend/components/ActivityFeed.tsx
'use client';

import React, { useEffect, useRef } from 'react';
import { WebSocketMessage } from '@/hooks/useWebSocket';

export function ActivityFeed({ messages }: { messages: WebSocketMessage[] }) {
  const feedRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [messages]);

  const getIcon = (type: string) => {
    const icons: Record<string, string> = {
      task_started: '🚀',
      skill_created: '✨',
      skill_discovered: '🔍',
      step_complete: '✅',
      workflow_complete: '🎉',
      agent_created: '🤖',
      skill_transfer: '⚡',
      subscribed: '📡',
      pong: '🏓'
    };
    return icons[type] || '📌';
  };

  const formatType = (type: string) => {
    return type
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch {
      return '';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-6 h-full flex flex-col">
      {/* Header */}
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-slate-900">
          📡 Live Activity Feed
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Real-time agent events
        </p>
      </div>

      {/* Feed */}
      <div
        ref={feedRef}
        className="flex-1 space-y-3 overflow-y-auto max-h-[500px]"
      >
        {messages.length > 0 ? (
          messages.slice().reverse().map((message, idx) => (
            <ActivityItem key={idx} message={message} />
          ))
        ) : (
          <div className="text-center py-12 text-slate-500">
            <p>No activity yet</p>
            <p className="text-sm mt-2">Start the demo to see live updates</p>
          </div>
        )}
      </div>
    </div>
  );
}

function ActivityItem({ message }: { message: WebSocketMessage }) {
  const getIcon = (type: string) => {
    const icons: Record<string, string> = {
      task_started: '🚀',
      skill_created: '✨',
      skill_discovered: '🔍',
      step_complete: '✅',
      workflow_complete: '🎉',
      agent_created: '🤖',
      skill_transfer: '⚡',
      subscribed: '📡',
      pong: '🏓'
    };
    return icons[type] || '📌';
  };

  const formatType = (type: string) => {
    return type
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch {
      return '';
    }
  };

  return (
    <div className="border-l-4 border-blue-500 pl-4 py-3 bg-slate-50 rounded-r hover:bg-slate-100 transition-colors">
      <div className="flex items-start gap-3">
        <span className="text-2xl flex-shrink-0">{getIcon(message.type)}</span>
        <div className="flex-1 min-w-0">
          <p className="font-medium text-sm text-slate-900">
            {formatType(message.type)}
          </p>
          {message.data && (
            <p className="text-xs text-slate-600 mt-1 truncate">
              {typeof message.data === 'string' 
                ? message.data 
                : JSON.stringify(message.data).slice(0, 100)}
            </p>
          )}
          <p className="text-xs text-slate-400 mt-1">
            {formatTimestamp(message.timestamp)}
          </p>
        </div>
      </div>
    </div>
  );
}
```

### Create PerformanceChart Component

```typescript
// frontend/components/PerformanceChart.tsx
'use client';

import React from 'react';

interface Agent {
  agent_id: string;
  agent_name: string;
  color: { r: number; g: number; b: number };
  performance: {
    tasks_completed: number;
    success_rate: number;
  };
}

export function PerformanceChart({ agents }: { agents: Agent[] }) {
  if (agents.length === 0) {
    return null;
  }

  const maxTasks = Math.max(...agents.map(a => a.performance.tasks_completed), 1);

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-6">
      <h2 className="text-xl font-semibold text-slate-900 mb-6">
        📊 Agent Performance Comparison
      </h2>

      <div className="space-y-6">
        {agents.map(agent => {
          const agentColor = `rgb(${agent.color.r}, ${agent.color.g}, ${agent.color.b})`;
          const tasksWidth = (agent.performance.tasks_completed / maxTasks) * 100;
          const successWidth = agent.performance.success_rate * 100;

          return (
            <div key={agent.agent_id} className="space-y-2">
              {/* Agent Name */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: agentColor }}
                  />
                  <span className="font-medium text-slate-900">
                    {agent.agent_name}
                  </span>
                </div>
                <span className="text-sm text-slate-600">
                  {agent.performance.tasks_completed} tasks • {(successWidth).toFixed(0)}% success
                </span>
              </div>

              {/* Tasks Bar */}
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 w-20">Tasks</span>
                  <div className="flex-1 bg-slate-200 rounded-full h-3 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${tasksWidth}%`,
                        backgroundColor: agentColor
                      }}
                    />
                  </div>
                  <span className="text-xs text-slate-500 w-8 text-right">
                    {agent.performance.tasks_completed}
                  </span>
                </div>

                {/* Success Rate Bar */}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 w-20">Success</span>
                  <div className="flex-1 bg-slate-200 rounded-full h-3 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${successWidth}%`,
                        backgroundColor: agentColor,
                        opacity: 0.7
                      }}
                    />
                  </div>
                  <span className="text-xs text-slate-500 w-8 text-right">
                    {successWidth.toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

---

## 3.4 ENVIRONMENT CONFIGURATION

### Backend .env

```bash
# backend/.env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/mirrorminds?retryWrites=true&w=majority
VOYAGE_API_KEY=your_voyage_api_key_here
ENVIRONMENT=development
```

### Frontend .env.local

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

### Production URLs (Already Configured)

Your existing hardcoded production URLs will work:
- **Backend:** `https://mongodb-hackathon.onrender.com`
- **Frontend:** `https://mongodb-hackathon.vercel.app`

---

## 3.5 MONGODB ATLAS SETUP

### Step 1: Create Cluster
1. Go to MongoDB Atlas: https://cloud.mongodb.com
2. Create free M0 cluster (sufficient for hackathon)
3. Choose region closest to you
4. Name it: `mirrorminds-cluster`

### Step 2: Create Database & Collections
```javascript
// In MongoDB Atlas UI or using mongosh
use mirrorminds

db.createCollection("skills")
db.createCollection("agents")
db.createCollection("executions")
db.createCollection("mazes")
```

### Step 3: Create Vector Search Index
1. Navigate to "Atlas Search" tab
2. Click "Create Search Index"
3. Choose "JSON Editor"
4. Use index name: `skill_semantic_search`
5. Paste configuration:

```json
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "description_embedding": {
        "dimensions": 1024,
        "similarity": "cosine",
        "type": "knnVector"
      },
      "metadata": {
        "fields": {
          "skill_type": {
            "type": "string"
          },
          "maze_type": {
            "type": "string"
          },
          "complexity": {
            "type": "string"
          }
        },
        "type": "document"
      },
      "status": {
        "type": "string"
      },
      "stats": {
        "fields": {
          "success_rate": {
            "type": "number"
          }
        },
        "type": "document"
      }
    }
  }
}
```

### Step 4: Get Connection String
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy connection string
4. Replace `<password>` with your database password
5. Add to `backend/.env`

---

# PART 4: HACKATHON EXECUTION PLAN

## 4.1 TEAM ROLES & TIMELINE

### Team of 4 People - 12 Hour Sprint

**Person 1: Frontend Lead (Alice)**
- Hours 0-3: Setup Next.js components (AgentCard, SkillLibrary, ActivityFeed)
- Hours 3-6: WebSocket integration, real-time updates
- Hours 6-9: Polish UI, animations, responsive design
- Hours 9-12: Testing, bug fixes, presentation prep

**Person 2: Backend Lead (Bob)**
- Hours 0-3: Enhance FastAPI with all skill/agent endpoints
- Hours 3-6: MongoDB integration, vector search implementation
- Hours 6-9: WebSocket broadcasting, execution tracking
- Hours 9-12: Deploy to Render, performance optimization

**Person 3: Simulation Developer (Charlie)**
- Hours 0-3: PyGame maze renderer, basic agent movement
- Hours 3-6: Random walk algorithm, skill execution logic
- Hours 6-9: Particle effects, animations, integration with backend
- Hours 9-12: Record demo video, prepare live simulation

**Person 4: Integration & Presentation (Dana)**
- Hours 0-3: MongoDB Atlas setup, seed data creation
- Hours 3-6: End-to-end testing, create demo skills
- Hours 6-9: **Record backup video** (CRITICAL!)
- Hours 9-12: **Full-time presentation prep**, slides, rehearsal

---

## 4.2 HOUR-BY-HOUR BREAKDOWN

### Hours 0-2: Foundation
**ALL TEAM:**
- ✅ Git repo setup with branches
- ✅ MongoDB Atlas cluster created
- ✅ Voyage AI API key obtained (free tier)
- ✅ Development environments running locally

**DELIVERABLES:**
- Backend running on `localhost:8000`
- Frontend running on `localhost:3000`
- MongoDB connection confirmed
- Vector search index created

---

### Hours 2-4: Core Development Sprint 1
**Frontend (Alice):**
- ✅ AgentCard component with live status
- ✅ SkillLibrary with search UI
- ✅ ActivityFeed component
- ✅ WebSocket connection established

**Backend (Bob):**
- ✅ `/api/skills` endpoints (list, search, create)
- ✅ `/api/agents` endpoints (list, create)
- ✅ `/api/execute` endpoint skeleton
- ✅ WebSocket `/ws` endpoint working

**Simulation (Charlie):**
- ✅ PyGame window rendering
- ✅ Maze grid drawn with walls/paths
- ✅ Single agent moving with arrow keys (manual test)

**Integration (Dana):**
- ✅ 3 demo mazes created in MongoDB
- ✅ 2-3 demo skills manually inserted
- ✅ Test agents created via API

**DELIVERABLES:**
- Full API documented in Postman/Thunder Client
- Frontend can fetch and display skills/agents
- PyGame maze visible

---

### Hours 4-6: Core Development Sprint 2
**Frontend (Alice):**
- ✅ Real-time WebSocket message display
- ✅ Skill search with filters working
- ✅ Performance chart component
- ✅ Start Demo button triggers API call

**Backend (Bob):**
- ✅ Voyage AI embedding generation working
- ✅ Vector search returns relevant skills
- ✅ WebSocket broadcasts task events
- ✅ Execution records stored in MongoDB

**Simulation (Charlie):**
- ✅ Random walk algorithm complete
- ✅ Agent reaches goal (unoptimized path)
- ✅ Path history tracked visually
- ✅ Skill execution mode (follows predefined path)

**Integration (Dana):**
- ✅ End-to-end test: Agent A random walk → Skill created → Agent B uses skill
- ✅ All data flowing through MongoDB
- ✅ Create 5-7 diverse demo skills

**DELIVERABLES:**
- ONE complete demo flow working (no automation yet)
- Agent A completes maze slowly, Agent B completes fast
- Skills discoverable via search

---

### Hours 6-8: Integration & Visual Polish
**Frontend (Alice):**
- ✅ Animations on skill transfer
- ✅ Loading states for all API calls
- ✅ Error handling (graceful degradation)
- ✅ Dark mode toggle (optional)

**Backend (Bob):**
- ✅ Skill transfer WebSocket event with animation data
- ✅ Leaderboard endpoint (`/api/analytics/leaderboard`)
- ✅ Agent analytics endpoint
- ✅ Performance logging

**Simulation (Charlie):**
- ✅ Particle effect for skill transfer (glowing particles)
- ✅ Agent colors match dashboard
- ✅ Completion time overlay in PyGame
- ✅ Side-by-side comparison mode

**Integration (Dana - CRITICAL):**
- ✅ **RECORD FULL BACKUP DEMO VIDEO** (5 minutes)
- ✅ **RECORD 1-MINUTE DEMO CLIP for presentation**
- ✅ Screenshots of all key moments
- ✅ Test demo flow 3 times successfully

**DELIVERABLES:**
- Complete automated demo sequence
- Backup video recorded and tested
- All components visually polished

---

### Hours 8-10: Deployment & Presentation Prep
**Frontend (Alice):**
- ✅ Deploy to Vercel
- ✅ Environment variables configured
- ✅ Production testing
- ✅ Responsive design fixes

**Backend (Bob):**
- ✅ Deploy to Render
- ✅ Production MongoDB connection
- ✅ CORS configured for production frontend
- ✅ Keep-alive ping working

**Simulation (Charlie):**
- ✅ PyGame packaged as standalone script
- ✅ Integration with production backend tested
- ✅ Multiple maze scenarios prepared
- ✅ Particle effects optimized

**Integration (Dana - FULL-TIME PRESENTATION):**
- ✅ Presentation slides created (10 slides max)
- ✅ Demo script written and timed (3 minutes)
- ✅ Team speaking roles assigned
- ✅ Q&A responses prepared

**DELIVERABLES:**
- Fully deployed application (frontend + backend)
- Presentation deck finalized
- Demo rehearsed 2x

---

### Hours 10-12: Final Polish & Rehearsal
**ALL TEAM:**
- ✅ Full demo rehearsal on presentation hardware (3x minimum)
- ✅ Backup plans tested (video playback, screenshots)
- ✅ GitHub repo cleaned up, README.md updated
- ✅ Open source license added (MIT)
- ✅ Team bio and project description finalized
- ✅ Sleep/power naps for presentation energy

**DELIVERABLES:**
- Demo runs flawlessly 3+ times in a row
- Presentation under 5 minutes with buffer
- Team confident and energized

---

## 4.3 CRITICAL SUCCESS FACTORS

### Must-Have for Demo
1. ✅ **2 agents visibly different colors**
2. ✅ **Agent A takes 40+ seconds (slow/random)**
3. ✅ **Skill transfer animation (particles flying)**
4. ✅ **Agent B takes <10 seconds (fast/learned)**
5. ✅ **Side-by-side time comparison shown**
6. ✅ **Backup video ready as fallback**

### Nice-to-Have (If Time Permits)
- 3rd agent that improves the skill further
- Skill evolution tree visualization
- Competitive marketplace with bidding
- Multiple maze types in sequence
- Sound effects for skill transfer

### Can Skip (Cut if Running Out of Time)
- User authentication
- Complex error handling
- Mobile optimization
- Advanced analytics
- Skill versioning UI

---

# PART 5: DEMO SCRIPT (FINAL VERSION)

## 5-Minute Hackathon Pitch

### [0:00-0:30] OPENING HOOK

**[Speaker 1 - Dana]**

*"Imagine you're training a team of robots to navigate a warehouse. Robot 1 spends 45 seconds wandering around, bumping into walls, eventually finding the target. Then Robot 2 comes in and... solves it in 9 seconds. How?"*

*[Pause for effect]*

*"Robot 2 learned from Robot 1's experience through shared procedural memory. That's MirrorMinds."*

**SLIDE 1: Title + Problem**
- Title: "MirrorMinds: Collective Intelligence Through Shared Memory"
- Problem: AI agents waste time re-solving problems others have already mastered

---

### [0:30-3:00] LIVE DEMONSTRATION

**[Speaker 2 - Charlie controlling demo]**

**SLIDE 2: Live Demo (Full Screen)**

*"Let me show you this in action. Here's a maze, and here's Agent Alpha..."*

**[ACT 1: The Struggle - 30 seconds]**
- Agent Alpha spawns
- Wanders randomly, hits walls, backtracks
- Timer counting up in corner
- *"Watch Agent Alpha struggle... no prior knowledge, just random exploration..."*
- Agent reaches goal: **42.3 seconds**
- *"42 seconds. Not great."*

**[ACT 2: The Learning - 15 seconds]**
- Screen highlights Agent Alpha's successful path
- UI shows: "💾 Saving strategy as skill..."
- Skill card appears: "Left-Wall Following Navigation"
- *"Agent Alpha's successful path becomes a reusable skill in our shared library"*

**[ACT 3: The Discovery - 15 seconds]**
- Agent Beta spawns
- UI shows: "🔍 Searching skill library..."
- Skill card pops up: "Match found: 92% relevance"
- *"Agent Beta discovers the skill through semantic search..."*

**[ACT 4: The Transfer - 20 seconds]**
- **GLOWING PARTICLES** fly from Agent Alpha to Agent Beta
- Agent Beta's card lights up: "✨ Skill acquired"
- *"Now watch the transfer..."*
- Agent Beta navigates efficiently: **9.1 seconds**
- *"9 seconds. That's a 78% improvement!"*

**[ACT 5: The Comparison - 10 seconds]**
- Side-by-side visualization:
  - Agent Alpha: 42.3s (red)
  - Agent Beta: 9.1s (green)
- *"This is collective intelligence. Every agent that learns makes every other agent smarter."*

---

### [3:00-4:00] TECHNICAL DEPTH & IMPACT

**[Speaker 3 - Bob]**

**SLIDE 3: Architecture Diagram**

*"Here's how it works technically:"*

**Architecture Points (30 seconds):**
- MongoDB Atlas with Vector Search for semantic skill matching
- Voyage AI embeddings for natural language queries
- LangGraph for agent orchestration
- Real-time WebSocket updates
- PyGame for visual simulation

**SLIDE 4: Beyond Mazes**

*"But this isn't just about mazes. The same system works for:"*
- **Software Development:** Agents sharing debugging workflows
- **Trading:** Agents sharing market strategies
- **Customer Support:** Agents sharing resolution tactics
- **Robotics:** Robots sharing manipulation techniques

**Key Metric:**
*"In our testing: 78% faster task completion when agents share skills vs. learning from scratch."*

---

### [4:00-4:45] IMPACT & MARKET

**[Speaker 4 - Alice]**

**SLIDE 5: Market Opportunity**

*"Why does this matter?"*

**Problem Scale:**
- Every AI agent company faces this: agents solving the same problems repeatedly
- Estimated $2B wasted annually in redundant AI compute
- No standard for agent-to-agent knowledge transfer

**Our Solution:**
- Procedural memory marketplace where best strategies emerge
- Agents get smarter collectively, not just individually
- Open source - anyone can build on this

**SLIDE 6: Traction**
- ✅ Functional prototype in 12 hours
- ✅ 78% performance improvement demonstrated
- ✅ Extensible to any domain requiring agent coordination
- ✅ Open sourced on GitHub during hackathon

---

### [4:45-5:00] CLOSING & TEAM

**[Speaker 1 - Dana]**

**SLIDE 7: Vision**

*"Imagine a future where AI agents continuously learn from each other. Where every problem solved makes every agent smarter. Where collective intelligence emerges naturally."*

*"That's the future we're building with MirrorMinds."*

**SLIDE 8: Team**
- **Alice:** Frontend Engineer - Built real-time dashboard
- **Bob:** Backend Engineer - Architected skill marketplace
- **Charlie:** Simulation Developer - Created visual proof of learning
- **Dana:** Product & Integration - Brought it all together

**FINAL SLIDE: Thank You + Demo**
- GitHub: `github.com/your-team/mirrorminds`
- Live Demo: `mongodb-hackathon.vercel.app`
- "Questions?"

---

## 5.1 BACKUP PLAN

### If Live Demo Fails:

**Immediate Actions (no hesitation):**
1. **Switch to recorded video** (speaker keeps narrating as if live)
2. **Continue presentation** with same energy
3. **Show screenshots** if video also fails
4. **Explain what WOULD happen** using slides

**Never Say:**
- ❌ "Sorry, the demo isn't working"
- ❌ "We had technical difficulties"
- ❌ "It worked earlier, I swear"

**Instead Say:**
- ✅ "Let me show you the recorded demo"
- ✅ *[Continue narration without acknowledging failure]*
- ✅ "As you can see in this capture..."

---

# PART 6: DEPLOYMENT CHECKLIST

## 6.1 Pre-Deployment Checklist

### Backend (Render)
- [ ] `requirements.txt` includes all dependencies
- [ ] MongoDB URI in Render environment variables
- [ ] Voyage API key in Render environment variables
- [ ] CORS allows production frontend URL
- [ ] Keep-alive ping enabled
- [ ] Health endpoint returns 200

### Frontend (Vercel)
- [ ] `NEXT_PUBLIC_API_URL` points to Render backend
- [ ] Build succeeds without errors
- [ ] Environment variables configured
- [ ] Custom domain (optional) configured

### MongoDB Atlas
- [ ] IP whitelist includes `0.0.0.0/0` (allow all)
- [ ] Database user has read/write permissions
- [ ] Vector search index created and active
- [ ] Sample data seeded

### GitHub
- [ ] Repository is public
- [ ] README.md with setup instructions
- [ ] MIT License file added
- [ ] `.env.example` files included
- [ ] Clear contribution guidelines

---

## 6.2 Testing Checklist

### Functional Testing
- [ ] Agent creation via API works
- [ ] Skill creation stores embeddings
- [ ] Skill search returns relevant results
- [ ] WebSocket connection establishes
- [ ] Real-time events broadcast correctly
- [ ] PyGame simulation runs without crashes

### Integration Testing
- [ ] Full demo flow: Agent A → Skill → Agent B
- [ ] Frontend displays all data correctly
- [ ] Performance metrics update in real-time
- [ ] Skill transfer animation plays smoothly

### Performance Testing
- [ ] Backend responds in <200ms
- [ ] Vector search completes in <300ms
- [ ] WebSocket latency <50ms
- [ ] PyGame maintains 60 FPS

### Browser Testing
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Mobile responsive (bonus)

---

# PART 7: POST-HACKATHON ROADMAP

## 7.1 Immediate Extensions (Week 1)

### Technical Improvements
1. **Agent Learning Loop**
   - Agents automatically extract skills after task completion
   - Reinforcement learning to improve strategy selection
   - A/B testing of skill variations

2. **Advanced Visualization**
   - 3D environment rendering
   - Multiple agents in same maze competing
   - Real-time skill evolution tree

3. **Skill Marketplace**
   - Bidding mechanism for valuable skills
   - Skill ratings and reviews
   - Pricing based on success rate and usage

## 7.2 Medium-Term Features (Month 1)

### Product Features
1. **Multi-Domain Support**
   - Code review workflows
   - Trading strategy sharing
   - Customer support tactics
   - DevOps runbooks

2. **Collaboration Features**
   - Teams of agents working together
   - Skill composition (combining multiple skills)
   - Conflict resolution when skills contradict

3. **Analytics Dashboard**
   - Skill effectiveness over time
   - Agent performance trends
   - ROI calculations

## 7.3 Long-Term Vision (6 Months)

### Enterprise Features
1. **Multi-Tenancy**
   - Organizational skill libraries
   - Access control and permissions
   - Audit logging

2. **Integrations**
   - GitHub Actions for CI/CD workflows
   - Slack for agent notifications
   - Datadog for monitoring

3. **Marketplace Platform**
   - Skill creators earn rewards
   - Community voting on best skills
   - Certified skills from experts

---

# PART 8: FAQ & TROUBLESHOOTING

## 8.1 Common Issues

### MongoDB Connection Fails
**Problem:** `pymongo.errors.ServerSelectionTimeoutError`

**Solution:**
1. Check MongoDB Atlas IP whitelist (allow `0.0.0.0/0`)
2. Verify connection string has correct username/password
3. Ensure database user has read/write permissions
4. Check network firewall isn't blocking port 27017

### Vector Search Doesn't Work
**Problem:** No results from semantic search

**Solution:**
1. Verify vector search index is created and "Active"
2. Check embedding dimensions match (1024 for Voyage AI)
3. Ensure skills have `description_embedding` field
4. Test with regular text search first

### PyGame Window Won't Open
**Problem:** `pygame.error: No available video device`

**Solution:**
1. Run PyGame in headless mode for server deployment
2. Use screenshot-based rendering
3. Pre-record demo video as backup
4. Test on local machine before deployment

### WebSocket Keeps Disconnecting
**Problem:** Connection drops every few minutes

**Solution:**
1. Implement reconnection logic in frontend
2. Send periodic ping messages
3. Check Render free tier timeout (15 min)
4. Upgrade to paid tier if needed

### Voyage AI Rate Limit
**Problem:** `429 Too Many Requests`

**Solution:**
1. Use free tier conservatively (1000 requests/day)
2. Cache embeddings in MongoDB
3. Pre-generate embeddings for demo skills
4. Implement exponential backoff retry

---

## 8.2 Hackathon Day Troubleshooting

### Demo Crashes Right Before Presentation

**Immediate Actions:**
1. **Don't panic** - you have backups
2. **Switch to backup video** immediately
3. **Keep presenting** as if nothing happened
4. **Smile and maintain energy**

### MongoDB Connection Lost During Demo

**Fallback:**
1. Frontend shows cached data
2. Explain "this is what it looks like when it works"
3. Show recorded video
4. Offer to demo after presentation

### PyGame Freezes

**Fallback:**
1. Show screenshots of each demo stage
2. Narrate what agents are doing
3. Show performance metrics from logs
4. Emphasize the backend architecture

---

# CONCLUSION

## You Now Have Everything You Need

This PRD provides:
✅ **Complete technical architecture** adapted to your existing setup  
✅ **Working code examples** for backend, frontend, and simulation  
✅ **Hour-by-hour timeline** for 12-hour hackathon  
✅ **Detailed demo script** optimized for judging criteria  
✅ **Deployment guide** for Render + Vercel + MongoDB Atlas  
✅ **Backup plans** for every possible failure  

## Key Success Factors

1. **Visual Impact Wins:** The 42s → 9s improvement is your killer moment
2. **Keep It Simple:** 3-step skills, 2-3 agents, 1 maze is enough
3. **Record Backup Video:** Do this by hour 8, not hour 11
4. **Practice Presentation:** Rehearse 5+ times minimum
5. **Team Coordination:** Clear roles, frequent check-ins

## Final Checklist Before You Start

- [ ] MongoDB Atlas cluster created -- Done
- [ ] Voyage AI API key obtained -- pa-1eG3a1tgKRIQ4af9uUKs-0XTWAHOqoXkNJP49pHlKMN
- [ ] GitHub repo setup -- Done
- [ ] Local development environments working -- done
- [ ] Hour-by-hour timeline printed and posted

---

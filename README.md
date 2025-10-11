# MirrorMinds - Collective Intelligence for AI Agents

**A shared brain for AI agents—a skill marketplace where they publish, discover, and reuse proven solutions.**

## The Problem: Stop Wasting AI's Potential

How many of us have had this exact conversation with an AI? "Okay, start the server... no, remember to activate the virtual environment first… the one in this folder…" We are all constantly re-explaining the same context in every new chat.

This isn't just annoying; it's incredibly wasteful. We're burning through expensive tokens, energy, and our own time, just to get the AI back to a state of understanding it already had. Now, imagine this problem scaled up to a team of AI agents trying to work together. They operate in silos, each one re-solving the same problems from scratch. It's a massive drain on resources and a huge barrier to creating truly intelligent systems.

## The Solution: MirrorMinds

MirrorMinds is a **skill marketplace** where AI agents can publish and discover proven solutions. The maze demo represents any complex, recurring problem—like a difficult debugging sequence or a multi-step deployment.

**The Magic:**
1. **Agent Alpha explores** the maze through intelligent trial and error (~100-200 steps, ~20-30 seconds)
2. **System optimizes** the discovered solution using BFS pathfinding (~25-30 steps)
3. **MongoDB stores** the skill with semantic embeddings powered by Voyage AI
4. **Agent Beta retrieves** the solution using Vector Search—no need to know the skill name, just describe the problem!
5. **Result:** Agent Beta completes in ~2-3 seconds with ~25-30 steps—**10x faster!**

This is the power of **collective learning**. The future of effective AI isn't about endlessly re-exploring and re-computing the same solutions. It's about solving a problem once, and allowing every other agent to instantly retrieve that knowledge and execute.

## Project Structure

```
mongodb-hackathon/
├── frontend/          # Next.js application
└── backend/           # FastAPI application
```

## Architecture

MirrorMinds is a **pure API + React frontend** architecture—no pygame required!

### How It Works

**Backend (FastAPI):**
- Runs maze simulation logic (smart exploration, BFS pathfinding)
- Broadcasts agent position updates via WebSocket in real-time
- Stores/retrieves skills from MongoDB with Vector Search
- Generates semantic embeddings using Voyage AI
- Pure REST API—no visualization libraries needed

**Frontend (React/Next.js):**
- `MazeVisualization.tsx` component renders the maze grid
- Listens to WebSocket updates and animates agent movement
- All visual rendering happens in the browser, not on the server

**Why No pygame?**
- pygame requires SDL2 native libraries that aren't available in cloud deployment environments
- Our visualization is 100% React-based, making deployment simple and cloud-friendly
- The backend only needs to send position data—the frontend handles all rendering

### Technology Usage in Code

**MongoDB (Motor)** - `main.py:36-38`
- `AsyncIOMotorClient` for non-blocking database operations across agents, skills, mazes, and executions collections

**Voyage AI** - `main.py:129-161`
- Generates 1024-dimensional semantic embeddings for skill descriptions using the `voyage-3` model

**Vector Search** - `main.py:237-308`
- MongoDB `$vectorSearch` aggregation pipeline enables semantic skill discovery with similarity scoring

**WebSockets** - `main.py:52-80, 797-840`
- `ConnectionManager` broadcasts real-time agent positions and events to all connected clients

**FastAPI** - `main.py:17-21`
- REST API framework with automatic Swagger/ReDoc documentation generation

**Render** - `main.py:899-916`
- Keep-alive system pings backend every 14 minutes to prevent free-tier spin-down

**Vercel** - `main.py:23-33`
- CORS middleware allows frontend at `mongodb-hackathon.vercel.app`

**Pydantic** - `main.py:95-124`
- Type-safe request/response models validate all API endpoint data

## Tech Stack

### Frontend
- **Next.js 14** with App Router
- **TypeScript**
- **Tailwind CSS v4** (latest)
- **shadcn/ui** - Beautiful, accessible UI components
- **React 18**
- **WebSocket client** for real-time updates

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Voyage AI** - Semantic embeddings for Vector Search
- **WebSockets** - Real-time agent position broadcasting
- **Uvicorn** - ASGI server
- **Python 3.13+**

## Quick Start

### 1. Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

Backend runs on http://localhost:8000

### 2. Start the Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on http://localhost:3000

### 3. Run the Demo

Visit http://localhost:3000 to see the MirrorMinds demo!

**Interactive Demo Flow:**
1. Click "Start Demo" to create the agents and maze
2. Click "Run Agent Alpha" to watch the first agent explore (wait for completion)
3. Click "Run Agent Beta" to see the second agent use the learned solution
4. Watch the real-time visualization and activity feed!

## Features

### Core Capabilities
- ✅ **Smart Exploration** - Agent Alpha intelligently explores mazes (prefers unvisited cells)
- ✅ **Path Optimization** - System extracts optimal solution using BFS after exploration
- ✅ **Vector Search** - Semantic skill discovery powered by MongoDB Vector Search + Voyage AI
- ✅ **Real-time Visualization** - WebSocket-powered live agent position updates
- ✅ **Human-in-the-Loop** - Separate control over Agent Alpha and Beta execution
- ✅ **Activity Feed** - Real-time event log showing agent decisions and outcomes

### Technical Features
- ✅ MongoDB Atlas integration with Vector Search indexes
- ✅ Async Python with Motor (MongoDB) and FastAPI
- ✅ TypeScript for full type safety
- ✅ Cloud-ready deployment (no native dependencies like pygame)
- ✅ Built-in keep-alive system (prevents free-tier services from sleeping)
- ✅ CORS configured for local development
- ✅ Comprehensive API documentation (Swagger + ReDoc)

## Development

### Adding shadcn/ui Components

```bash
cd frontend
npx shadcn@latest add [component-name]
```

### Backend API Documentation

When the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

Ready to deploy? See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for complete deployment instructions.

**Quick Links:**
- Backend: Deploy to [Render](https://render.com)
- Frontend: Deploy to [Vercel](https://vercel.com)

The backend includes a built-in keep-alive system that pings itself every 14 minutes to prevent free-tier services from going to sleep.

## Documentation

- **[README.md](./README.md)** - This file (project overview and quick start)
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Complete deployment guide for Render + Vercel
- **[PROGRESS_MIRRORMINDS.md](./PROGRESS_MIRRORMINDS.md)** - Detailed development progress (7 phases completed!)
- **[PRD_2.md](./PRD_2.md)** - Product requirements document
- **[backend/README.md](./backend/README.md)** - Backend-specific documentation

## Performance Results

**Labyrinth Challenge (15x15 maze):**
- **Agent Alpha (Explorer):** ~100-200 steps, ~20-30 seconds
- **Optimized Solution:** ~25-30 steps (saved 75-175 steps!)
- **Agent Beta (Learner):** ~25-30 steps, ~2-3 seconds
- **Speedup:** 10x faster execution time
- **Efficiency Gain:** 75-85% fewer steps

## What's Next?

MirrorMinds demonstrates the core concept of collective intelligence for AI agents. Future enhancements could include:

- Multiple maze types and difficulty levels
- Multi-agent collaborative problem solving
- Skill versioning and improvement tracking
- Cross-domain skill transfer
- Agent reputation and trust scoring
- API for third-party agent integration

---

## About This Project

**Built for MongoDB Hackathon 2025**

MirrorMinds showcases the power of MongoDB Vector Search for enabling semantic skill discovery in multi-agent systems. By combining MongoDB Atlas's vector search capabilities with Voyage AI embeddings, we demonstrate how AI agents can move from isolated problem-solving to true collective intelligence.

**Key MongoDB Features Used:**
- **Vector Search** - Semantic similarity search for skill discovery
- **Atlas Search Indexes** - Optimized vector embeddings storage
- **Motor (Async Driver)** - Non-blocking database operations for real-time performance
- **Document Model** - Flexible schema for storing agent data, skills, and maze configurations

**Lines of Code:** ~2,600+
**Development Time:** 7 phases completed
**Status:** Demo ready and cloud-deployable

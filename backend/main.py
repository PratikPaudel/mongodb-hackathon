from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import httpx
from datetime import datetime
import os

# Keep-alive configuration
SELF_PING_INTERVAL = 14 * 60  # 14 minutes in seconds
# Use production URL if RENDER_EXTERNAL_URL is set, otherwise use localhost
SELF_URL = os.getenv("RENDER_EXTERNAL_URL") or "http://localhost:8000"
# Hardcoded production URL as fallback
if SELF_URL == "http://localhost:8000" and os.getenv("RENDER"):
    SELF_URL = "https://mongodb-hackathon.onrender.com"

async def keep_alive_task():
    """Background task to ping the health endpoint every 14 minutes to keep the service alive."""
    await asyncio.sleep(60)  # Wait 1 minute before starting

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(f"{SELF_URL}/api/health", timeout=10.0)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if response.status_code == 200:
                    print(f"[{timestamp}] ✓ Self-ping successful: {response.json()}")
                else:
                    print(f"[{timestamp}] ✗ Self-ping failed with status {response.status_code}")
            except Exception as e:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] ✗ Self-ping error: {e}")

            await asyncio.sleep(SELF_PING_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create keep-alive background task
    task = asyncio.create_task(keep_alive_task())
    print(f"Started keep-alive task (pinging every {SELF_PING_INTERVAL // 60} minutes)")
    yield
    # Shutdown: Cancel the task
    task.cancel()
    print("Stopped keep-alive task")

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "https://mongodb-hackathon.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

@app.get("/api/data")
async def get_data():
    return {
        "data": [
            {"id": 1, "name": "Item 1", "description": "First item"},
            {"id": 2, "name": "Item 2", "description": "Second item"},
            {"id": 3, "name": "Item 3", "description": "Third item"},
        ]
    }

@app.post("/api/echo")
async def echo(payload: dict):
    return {"received": payload, "message": "Echo successful"}

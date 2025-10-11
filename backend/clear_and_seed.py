#!/usr/bin/env python3
"""
Quick script to clear old mazes and seed the new Labyrinth Challenge
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client["mirrorminds"]

    # Drop old mazes and skills to force re-seeding
    print("🗑️  Dropping mazes and skills collections...")
    await db.mazes.drop()
    await db.skills.drop()

    # Create the new Labyrinth Challenge maze
    print("📦 Creating Labyrinth Challenge maze...")
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
    print("✅ Labyrinth Challenge maze created!")

    client.close()

if __name__ == "__main__":
    asyncio.run(main())

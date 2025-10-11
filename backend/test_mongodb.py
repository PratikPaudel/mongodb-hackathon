#!/usr/bin/env python3
"""
Quick MongoDB connection test script
"""
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

async def test_connection():
    # Load environment variables
    load_dotenv()

    mongodb_uri = os.getenv("MONGODB_URI")

    if not mongodb_uri:
        print("❌ MONGODB_URI not found in environment variables")
        return False

    print(f"📡 Attempting to connect to MongoDB...")
    print(f"   URI: {mongodb_uri.split('@')[1] if '@' in mongodb_uri else 'unknown'}")

    try:
        # Create client with timeout
        client = AsyncIOMotorClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )

        print("🔄 Attempting to ping MongoDB...")
        # Test connection
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")

        # Get database info
        db = client["mirrorminds"]
        collections = await db.list_collection_names()
        print(f"📚 Database: mirrorminds")
        print(f"📦 Collections: {collections if collections else 'No collections yet'}")

        # Close connection
        client.close()
        return True

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)

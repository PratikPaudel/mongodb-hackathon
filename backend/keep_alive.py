"""
Keep-alive script to ping the health check endpoint every 14 minutes.
This prevents free tier services on Render from going to sleep.

Usage:
    python keep_alive.py <your-backend-url>

Example:
    python keep_alive.py https://your-app.onrender.com
"""

import time
import requests
import sys
from datetime import datetime

def ping_health_check(base_url: str):
    """Ping the health check endpoint."""
    url = f"{base_url}/api/health"
    try:
        response = requests.get(url, timeout=10)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            print(f"[{timestamp}] ✓ Health check successful: {response.json()}")
            return True
        else:
            print(f"[{timestamp}] ✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✗ Error pinging health check: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python keep_alive.py <backend-url>")
        print("Example: python keep_alive.py https://your-app.onrender.com")
        sys.exit(1)

    backend_url = sys.argv[1].rstrip('/')
    interval_minutes = 14
    interval_seconds = interval_minutes * 60

    print(f"Starting keep-alive service...")
    print(f"Backend URL: {backend_url}")
    print(f"Ping interval: {interval_minutes} minutes")
    print(f"Press Ctrl+C to stop\n")

    while True:
        ping_health_check(backend_url)
        print(f"Waiting {interval_minutes} minutes until next ping...\n")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()

# FastAPI Backend

A FastAPI backend with CORS configured to work with the Next.js frontend.

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

**Development:**
```bash
uvicorn main:app --reload
```

**Production:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## Available Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check endpoint
- `GET /api/data` - Returns sample data
- `POST /api/echo` - Echo endpoint that returns the payload sent to it

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Keep-Alive System

The backend includes a built-in keep-alive mechanism that automatically pings itself every 14 minutes to prevent sleeping on free tier services like Render.

**How it works:**
- A background task starts on application startup
- Every 14 minutes, it sends a GET request to `/api/health`
- Logs ping results to console
- Uses the `RENDER_EXTERNAL_URL` environment variable (auto-set by Render)

**Local testing:**
The keep-alive will use `http://localhost:8000` by default when running locally.

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed deployment instructions to Render.

**Quick Deploy to Render:**
1. Push code to GitHub
2. Connect repository to Render
3. Set root directory to `backend`
4. Deploy with build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

The keep-alive system will automatically start keeping your service active.

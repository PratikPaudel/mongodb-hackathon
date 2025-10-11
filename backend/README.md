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

```bash
uvicorn main:app --reload
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

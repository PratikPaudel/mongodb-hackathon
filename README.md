# Next.js + FastAPI Full Stack Application

A full-stack application with Next.js 14 (App Router), Tailwind CSS v4, shadcn/ui on the frontend, and FastAPI on the backend.

## Project Structure

```
mongodb-hackathon/
├── frontend/          # Next.js application
└── backend/           # FastAPI application
```

## Tech Stack

### Frontend
- **Next.js 14** with App Router
- **TypeScript**
- **Tailwind CSS v4** (latest)
- **shadcn/ui** - Beautiful, accessible UI components
- **React 18**

### Backend
- **FastAPI** - Modern Python web framework
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

### 3. Test the Connection

Visit http://localhost:3000 and click the buttons to test the API connection!

## Features

- ✅ CORS configured for local development
- ✅ Sample API endpoints for health check and data fetching
- ✅ Interactive demo page with shadcn/ui components
- ✅ TypeScript for type safety
- ✅ Tailwind CSS v4 for modern styling
- ✅ Auto-reloading for both frontend and backend

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

## Next Steps

- Add MongoDB integration
- Implement authentication
- Create more API endpoints
- Build out your application features!

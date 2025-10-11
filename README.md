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
- ✅ Built-in keep-alive system (backend pings itself every 14 minutes)
- ✅ Ready for deployment to Render and Vercel

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

- **[README.md](./README.md)** - This file (quick start guide)
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment instructions
- **[PROGRESS.md](./PROGRESS.md)** - Development progress and roadmap
- **[backend/README.md](./backend/README.md)** - Backend-specific documentation

## Next Steps

- Add MongoDB integration
- Implement authentication
- Create more API endpoints
- Build out your application features!

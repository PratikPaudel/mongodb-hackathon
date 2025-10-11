# Deployment Guide

This guide covers deploying the MongoDB Hackathon application to production.

## Backend Deployment (Render)

### Quick Deploy

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name:** `mongodb-hackathon-backend` (or your preferred name)
     - **Region:** Choose closest to your users
     - **Branch:** `main`
     - **Root Directory:** `backend`
     - **Runtime:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

3. **Note your Backend URL**
   - After deployment, Render will give you a URL like: `https://your-app.onrender.com`
   - Copy this URL for the frontend configuration

### Using render.yaml (Alternative)

Alternatively, you can use the included `render.yaml` file:

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Select `backend/render.yaml`
5. Click "Apply"

### Environment Variables (if needed later)

When you add MongoDB or other services, add environment variables in Render:
- Go to your service → "Environment"
- Add variables like `MONGODB_URI`, `SECRET_KEY`, etc.

---

## Frontend Deployment (Vercel - Recommended)

### Quick Deploy

1. **Update Backend URL**
   - Create `.env.production` in the `frontend` directory:
   ```bash
   NEXT_PUBLIC_BACKEND_URL=https://your-backend.onrender.com
   ```

2. **Deploy to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset:** Next.js
     - **Root Directory:** `frontend`
     - **Build Command:** (leave default) `npm run build`
     - **Output Directory:** (leave default) `.next`
   - Add environment variable:
     - **Key:** `NEXT_PUBLIC_BACKEND_URL`
     - **Value:** `https://your-backend.onrender.com`
   - Click "Deploy"

### Alternative: Frontend on Render

If you prefer to deploy the frontend on Render as well:

1. Create a new Web Service in Render
2. Configure:
   - **Name:** `mongodb-hackathon-frontend`
   - **Root Directory:** `frontend`
   - **Runtime:** `Node`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start`
3. Add environment variable:
   - **Key:** `NEXT_PUBLIC_BACKEND_URL`
   - **Value:** Your backend URL

---

## Keep-Alive System

### Built-in Self-Ping (Backend)

The backend automatically pings itself every 14 minutes to prevent sleeping on free tier services. This is configured in `main.py` and uses the `RENDER_EXTERNAL_URL` environment variable (auto-populated by Render).

**How it works:**
- On startup, a background task is created
- Every 14 minutes, it sends a GET request to `/api/health`
- This keeps the service active and prevents it from going to sleep

### Alternative: External Keep-Alive

If you need additional reliability, you can also use external services:

1. **UptimeRobot** (Free)
   - Sign up at [uptimerobot.com](https://uptimerobot.com)
   - Add a new monitor
   - Set URL to `https://your-backend.onrender.com/api/health`
   - Set interval to 5 minutes (minimum on free tier)

2. **Cron-job.org** (Free)
   - Sign up at [cron-job.org](https://cron-job.org)
   - Create a new cron job
   - Set URL to your health endpoint
   - Set schedule to every 14 minutes

3. **Standalone Script** (Manual)
   - Run the included `backend/keep_alive.py` script:
   ```bash
   cd backend
   source venv/bin/activate
   pip install requests
   python keep_alive.py https://your-backend.onrender.com
   ```

---

## Post-Deployment Checklist

After deploying both frontend and backend:

- [ ] Backend is accessible at the Render URL
- [ ] Visit `https://your-backend.onrender.com/docs` to verify API docs work
- [ ] Test `/api/health` endpoint returns `{"status": "healthy"}`
- [ ] Frontend is accessible at the Vercel/Render URL
- [ ] Frontend can successfully call backend API
- [ ] Check browser console for any CORS errors
- [ ] Verify keep-alive system is working (check backend logs)

---

## Updating CORS for Production

Once your frontend is deployed, update the CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-frontend.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Or for development, you can use:
```python
allow_origins=["*"]  # Allow all origins (not recommended for production)
```

---

## Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify all dependencies are in `requirements.txt`
- Ensure Python version is 3.9+

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_BACKEND_URL` is set correctly
- Check CORS settings in backend
- Test backend URL directly in browser

### Backend keeps going to sleep
- Verify the keep-alive task is running (check logs)
- Ensure `RENDER_EXTERNAL_URL` is set correctly
- Consider using an external monitoring service

### 502 Bad Gateway on Render
- Check if the app is listening on `0.0.0.0` and port `$PORT`
- Verify the start command is correct
- Check logs for startup errors

---

## Costs

### Free Tier Limits

**Render (Backend):**
- Free tier available
- 750 hours/month
- Services sleep after 15 minutes of inactivity (keep-alive prevents this)
- 0.1 CPU, 512 MB RAM

**Vercel (Frontend):**
- Free tier available
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS

---

## Next Steps

1. **Add Custom Domain** (Optional)
   - Configure custom domain in Vercel/Render dashboard
   - Update DNS settings

2. **Set up CI/CD**
   - Both Vercel and Render auto-deploy on git push
   - Configure branch deployments if needed

3. **Add MongoDB**
   - Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster
   - Add connection string as environment variable
   - Update CORS to allow MongoDB Atlas IPs if needed

4. **Add Monitoring**
   - Set up error tracking (Sentry)
   - Configure analytics
   - Set up uptime monitoring

---

## Support

For deployment issues:
- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

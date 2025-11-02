# 🚀 Sweet Shop Management System - Deployment Guide

Complete step-by-step guide to deploy your Sweet Shop Management System to production.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Database Setup](#database-setup)
7. [Environment Variables](#environment-variables)
8. [Post-Deployment](#post-deployment)

---

## 🎯 Overview

This guide will help you deploy:
- **Backend**: FastAPI application (Railway/Render/Railway.app)
- **Frontend**: React application (Vercel/Netlify)
- **Database**: PostgreSQL (managed database)

---

## ✅ Prerequisites

1. GitHub account with your code pushed
2. Account on deployment platforms:
   - **Backend**: [Railway](https://railway.app) or [Render](https://render.com)
   - **Frontend**: [Vercel](https://vercel.com) or [Netlify](https://netlify.com)
   - **Database**: Included with backend platform or separate (Supabase/Neon)

---

## 🎯 Deployment Options

### Recommended Stack (Free Tier Available):

| Component | Platform | Free Tier |
|-----------|----------|-----------|
| Backend | Railway.app | ✅ Yes |
| Frontend | Vercel | ✅ Yes |
| Database | Railway PostgreSQL | ✅ Yes |

### Alternative Options:
- **Backend**: Render, Fly.io, Heroku (paid)
- **Frontend**: Netlify, GitHub Pages
- **Database**: Supabase, Neon, ElephantSQL

---

## 🗄️ Step 1: Database Setup

### Option A: Railway PostgreSQL (Recommended)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"**
4. Click **"Add Database"** → Select **"PostgreSQL"**
5. Wait for database to provision
6. Click on database → Go to **"Variables"** tab
7. **Important:** आपको यहां 2 URLs दिखेंगे:
   - `DATABASE_URL` (Private/Internal) - जैसे: `postgresql://...@postgres.railway.internal:5432/railway`
   - `DATABASE_URL_PUBLIC` या `Public URL` - जैसे: `postgresql://...@xxxxx.proxy.rlwy.net:56520/railway`

**कौन सा URL use करें?**

### अगर Backend भी Railway पर deploy हो रहा है:
✅ **`DATABASE_URL` (Private/Internal)** use करें
- Railway के services एक-दूसरे के साथ private network में communicate करते हैं
- यह तेज़ और ज्यादा secure होता है
- Format: `postgresql://postgres:password@postgres.railway.internal:5432/railway`

postgresql://postgres:IaOCaRrwoAHBxCVIjywUWDMZSxcSbjwg@postgres.railway.internal:5432/railway

### अगर Backend दूसरे platform पर है (Render, Heroku, etc.):
✅ **`DATABASE_URL_PUBLIC` (Public URL)** use करें
- External connections के लिए ज़रूरी है
- Format: `postgresql://postgres:password@xxxxx.proxy.rlwy.net:PORT/railway`

**Example DATABASE_URL format:**
```
# Private (Railway to Railway):
postgresql://postgres:password@postgres.railway.internal:5432/railway

# Public (External platforms):
postgresql://postgres:password@xxxxx.proxy.rlwy.net:56520/railway
```

### Option B: Supabase (Free PostgreSQL)

1. Go to [Supabase](https://supabase.com)
2. Create new project
3. Go to **Settings** → **Database**
4. Copy **Connection String** → **URI**

---

## 🔧 Step 2: Backend Deployment

### Option A: Railway (Recommended - Easiest)

#### 2.1 Connect Repository
1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will auto-detect it's a Python project

#### 2.2 Configure Backend (⚠️ बहुत Important!)

**⚠️ यह step मिस न करें - 90% errors इसी से होती हैं!**

1. **Settings** tab → **General** section पर जाएं
2. **Root Directory** field में `backend` type करें (exact spelling)
3. **Save** button click करें
4. Page refresh करें और verify करें Root Directory = `backend` है
5. Railway अब automatically:
   - Python version detect करेगा (`requirements.txt` से)
   - Build करेगा
   - Deploy करेगा

**Note:** अगर Root Directory set नहीं करेंगे, तो Railway root folder से scan करेगा और "could not determine how to build" error आएगा!

#### 2.3 Set Environment Variables
Go to **Variables** tab and add:

**Important:** अगर Database और Backend दोनों Railway पर हैं:
- Railway **automatically** `DATABASE_URL` add कर देता है (जब आप database को same project में link करते हैं)
- आपको manually copy-paste करने की ज़रूरत नहीं!

**अगर manually add करना हो तो:**
```
DATABASE_URL=postgresql://postgres:password@postgres.railway.internal:5432/railway
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

**Note:** `DATABASE_URL` में Private URL (`.railway.internal`) use करें, Public URL नहीं।

**Important Notes:**
- Generate a strong `SECRET_KEY`: Use `openssl rand -hex 32` or [randomkeygen.com](https://randomkeygen.com)
- Use the `DATABASE_URL` from Step 1
- `DEBUG=False` in production

**⚠️ Python Version Fix (अगर pydantic-core build error आए):**
Railway कभी-कभी Python 3.13 use करता है जो `pydantic-core` के साथ compatible नहीं है। 
- **Variables** tab में add करें: `PYTHON_VERSION=3.12.7`
- या `backend/runtime.txt` file में `python-3.12.7` होना चाहिए

#### 2.4 Configure Build & Start Commands
In **Settings** → **Deploy** tab:

1. **Root Directory**: `backend` (बहुत ज़रूरी!)
2. **Build Command**: (खाली छोड़ दें - Railway/Nixpacks automatically detect करेगा)
   - Nixpacks automatically `requirements.txt` detect करेगा और install करेगा
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**⚠️ Important:** 
- Root Directory **अवश्य** `backend` set करें
- अगर Root Directory गलत है, तो "Error creating build plan" error आएगा

#### 2.5 Deploy
1. Click **"Deploy"** button
2. Wait for build to complete (2-5 minutes)
3. Once deployed, Railway gives you a URL like: `https://your-app.railway.app`

**✅ Backend URL Example:** `https://sweet-shop-api.railway.app`

---

### Option B: Render

#### 2.1 Create Web Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `sweet-shop-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 2.2 Add Environment Variables
Under **Environment Variables**:
```
DATABASE_URL=your-postgres-url
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=False
```

#### 2.3 Deploy
- Click **"Create Web Service"**
- Render will automatically deploy
- URL: `https://sweet-shop-backend.onrender.com`

---

## 🌐 Step 3: Frontend Deployment

### Option A: Vercel (Recommended - Best for React)

#### 3.1 Connect Repository
1. Go to [Vercel](https://vercel.com)
2. Sign up with GitHub
3. Click **"Add New Project"**
4. Import your repository
5. Vercel will auto-detect React

#### 3.2 Configure Project
- **Framework Preset**: Create React App
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `build` (auto-detected)

#### 3.3 Environment Variables
Add:
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

**Important:** Replace `your-backend-url` with your actual backend URL from Step 2.

#### 3.4 Deploy
1. Click **"Deploy"**
2. Wait 1-2 minutes
3. Get your frontend URL: `https://your-app.vercel.app`

**✅ Frontend URL Example:** `https://sweet-shop-app.vercel.app`

---

### Option B: Netlify

#### 3.1 Connect Repository
1. Go to [Netlify](https://netlify.com)
2. Sign up with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. Select your repository

#### 3.2 Configure Build Settings
- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `frontend/build`

#### 3.3 Environment Variables
Go to **Site settings** → **Environment variables**:
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

#### 3.4 Deploy
- Click **"Deploy site"**
- URL: `https://your-app-name.netlify.app`

---

## 🔗 Step 4: Update CORS & API URL

### Update Backend CORS
Your backend needs to allow your frontend URL. Update `backend/app/main.py`:

```python
# Update CORS to include your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Keep for local dev
        "https://your-frontend.vercel.app",  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update Frontend API URL
Create/update `frontend/.env.production`:
```
REACT_APP_API_URL=https://your-backend.railway.app
```

Or update `AuthContext.tsx` to use:
```typescript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
axios.post(`${API_URL}/api/auth/login`, formData);
```

---

## 🔐 Step 5: Environment Variables Summary

### Backend Environment Variables (Railway/Render):
```env
DATABASE_URL=postgresql://postgres:password@host:5432/dbname
SECRET_KEY=your-very-long-random-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=False
```

### Frontend Environment Variables (Vercel/Netlify):
```env
REACT_APP_API_URL=https://your-backend-url.railway.app
```

---

## ✅ Step 6: Post-Deployment Checklist

### Backend:
- [ ] Backend is accessible at `https://your-backend.railway.app/health`
- [ ] Database connection works
- [ ] API docs accessible at `https://your-backend.railway.app/docs`
- [ ] CORS allows frontend URL

### Frontend:
- [ ] Frontend loads at `https://your-frontend.vercel.app`
- [ ] Can register new user
- [ ] Can login
- [ ] API calls work (check browser console)
- [ ] No CORS errors

### Database:
- [ ] Tables created automatically (on first startup)
- [ ] Can create admin user manually if needed

---

## 🐛 Troubleshooting

**⚠️ Railway Build Error Fix:**
अगर "Error creating build plan" error आ रहा है, तो `RAILWAY_TROUBLESHOOTING.md` देखें - detailed solutions हैं!

### Backend Issues:

**"Database connection failed"**
- Check `DATABASE_URL` is correct
- Ensure database is running
- Check firewall/network settings

**"CORS error"**
- Add frontend URL to `allow_origins` in `main.py`
- Redeploy backend

**"Module not found"**
- Ensure `requirements.txt` has all dependencies
- Check build logs in Railway/Render

### Frontend Issues:

**"Failed to fetch" or "Network error"**
- Check `REACT_APP_API_URL` is set correctly
- Verify backend URL is accessible
- Check CORS configuration in backend

**"404 on API calls"**
- Ensure API URL doesn't have trailing slash
- Check backend routes are correct

---

## 🎉 Quick Reference: Your Deployment URLs

After deployment, you'll have:

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | `https://your-app.vercel.app` | User-facing app |
| Backend API | `https://your-api.railway.app` | API endpoints |
| API Docs | `https://your-api.railway.app/docs` | Swagger UI |
| Health Check | `https://your-api.railway.app/health` | Status check |

---

## 📝 Creating First Admin User

After deployment, create an admin user:

1. Register a normal user through the frontend
2. Connect to your production database
3. Update user role:
   ```sql
   UPDATE users SET role = 'admin' WHERE username = 'your_username';
   ```
4. Logout and login again

---

## 🔄 Updating Your Deployment

### Backend:
- Push changes to GitHub
- Railway/Render auto-deploys on push
- Or manually trigger redeploy

### Frontend:
- Push changes to GitHub
- Vercel/Netlify auto-deploys on push

---

## 💰 Cost Estimates (Free Tier)

- **Railway**: Free tier with $5 credit/month
- **Vercel**: Free for personal projects
- **Render**: Free tier with limitations
- **Netlify**: Free tier available

For production with high traffic, consider paid plans.

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://react.dev/learn/start-a-new-react-project#production-build)

---

**🎊 Congratulations! Your Sweet Shop Management System is now live!**

Need help? Check the troubleshooting section or review deployment logs.


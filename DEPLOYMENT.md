# Deployment Guide

## 🚀 Quick Deploy Options

### Best Platforms for This Project:
1. **Backend (FastAPI)**: Railway, Render, or Fly.io
2. **Frontend (HTML)**: GitHub Pages, Netlify, or Vercel
3. **Full Stack**: Railway (easiest all-in-one)

---

## 📦 Step 1: Push to GitHub

### Initialize Git Repository

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Hyperlocal Intelligence Platform"

# Create repository on GitHub (go to github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/hyperlocal-insurance.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Important: Protect Sensitive Data

Your `.gitignore` already excludes:
- `.env` (contains API keys)
- `__pycache__/`
- `node_modules/`
- `*.pyc`

**Never commit your `.env` file!** Only commit `.env.example`

---

## 🌐 Option 1: Deploy to Railway (RECOMMENDED - Easiest)

Railway is perfect for this project - handles both backend and frontend.

### Deploy Backend to Railway

1. **Sign up**: https://railway.app (use GitHub login)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**:
   - Go to Variables tab
   - Add:
     ```
     WEATHER_API_KEY=your_openweathermap_key
     PORT=8080
     ```

4. **Railway will auto-detect** your Python app and deploy it!

5. **Get your API URL**: 
   - Railway provides: `https://your-app.railway.app`
   - Update this in your `dashboard.html` (line 1 of script section)

### Deploy Frontend to Railway

1. **Create another service** in same project
2. **Add Static Site**:
   - Upload `dashboard.html`
   - Railway will serve it automatically

**Total cost**: FREE for hobby projects!

---

## 🌐 Option 2: Render (Free Tier Available)

### Deploy Backend to Render

1. **Sign up**: https://render.com

2. **New Web Service**:
   - Connect GitHub repository
   - Name: `hyperlocal-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   ```
   WEATHER_API_KEY=your_key
   ```

4. **Deploy**: Render will build and deploy automatically

### Deploy Frontend to Netlify

1. **Sign up**: https://netlify.com

2. **Drag & Drop**:
   - Just drag `dashboard.html` to Netlify
   - Or connect GitHub repo

3. **Update API URL** in `dashboard.html`:
   ```javascript
   const API_BASE = 'https://your-app.onrender.com/api';
   ```

**Cost**: FREE (with some limitations)

---

## 🐳 Option 3: Docker + Any Cloud Provider

### Build Docker Image

```powershell
# Build the image
docker build -t hyperlocal-insurance .

# Test locally
docker run -p 8080:8080 --env-file .env hyperlocal-insurance
```

### Deploy to:
- **Google Cloud Run**: Auto-scaling, pay-per-use
- **AWS ECS/Fargate**: Enterprise-grade
- **DigitalOcean App Platform**: Simple and affordable
- **Azure Container Instances**: Microsoft ecosystem

---

## 🔧 Pre-Deployment Checklist

### 1. Update CORS Settings

In `backend/main.py`, update allowed origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "http://localhost:3000"  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Update API URL in Frontend

In `dashboard.html`, change:
```javascript
const API_BASE = 'https://your-backend-url.com/api';
```

### 3. Set Production Environment Variables

```env
WEATHER_API_KEY=your_actual_key
DATABASE_URL=your_production_db_url
REDIS_URL=your_production_redis_url
```

### 4. Test Locally with Production Settings

```powershell
# Test backend
python -m backend.main

# Open dashboard.html in browser
# Test all features
```

---

## 📊 Recommended Setup (Best Performance)

### For Production:

**Backend**: Railway or Render
- ✅ Auto-scaling
- ✅ Free SSL
- ✅ Easy environment variables
- ✅ GitHub auto-deploy

**Frontend**: Netlify or Vercel
- ✅ Global CDN
- ✅ Instant deploys
- ✅ Free SSL
- ✅ Custom domains

**Database** (when you add it): 
- Railway PostgreSQL (included)
- Supabase (free tier)
- PlanetScale (MySQL)

**Cost**: $0-5/month for small scale

---

## 🚨 Common Deployment Issues

### Issue: CORS Errors
**Fix**: Update `allow_origins` in `backend/main.py`

### Issue: API Key Not Working
**Fix**: Check environment variables are set correctly in deployment platform

### Issue: Port Binding Error
**Fix**: Use `PORT` environment variable:
```python
port = int(os.getenv("PORT", 8080))
uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
```

### Issue: Module Not Found
**Fix**: Ensure `requirements.txt` is in root directory

---

## 🎯 Quick Start Commands

### Push to GitHub:
```powershell
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Deploy to Railway:
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Add environment variables
4. Done! ✅

### Deploy Frontend to Netlify:
1. Go to https://netlify.com
2. Drag `dashboard.html` to deploy
3. Update API URL in file
4. Done! ✅

---

## 📈 Monitoring & Maintenance

### Set Up Monitoring:
- **Uptime**: UptimeRobot (free)
- **Errors**: Sentry (free tier)
- **Analytics**: Google Analytics

### Regular Maintenance:
- Update dependencies monthly
- Monitor API usage (OpenWeatherMap limits)
- Check logs for errors
- Backup database regularly

---

## 💰 Cost Estimates

### Free Tier (Hobby/Testing):
- Railway: Free for 500 hours/month
- Render: Free tier available
- Netlify: Free for personal projects
- **Total**: $0/month

### Production (Small Scale):
- Railway Pro: $5/month
- Render Starter: $7/month
- Database: $5/month
- **Total**: ~$15-20/month

### Production (Medium Scale):
- Railway: $20/month
- Database: $15/month
- CDN: $10/month
- **Total**: ~$45/month

---

## 🎓 Next Steps After Deployment

1. ✅ Set up custom domain
2. ✅ Enable HTTPS (automatic on most platforms)
3. ✅ Set up monitoring
4. ✅ Configure backup strategy
5. ✅ Add authentication (if needed)
6. ✅ Set up CI/CD pipeline
7. ✅ Load testing
8. ✅ Documentation for users

---

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Netlify Docs: https://docs.netlify.com
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/

Good luck with your deployment! 🚀

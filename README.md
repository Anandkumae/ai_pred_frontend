# Frontend Deployment

## 📦 Files in this directory

All files needed for frontend deployment are here:

- `dashboard.py` - Streamlit dashboard application
- `requirements.txt` - Python dependencies

## 🚀 Deploy to Streamlit Cloud

### Step 1: Push to GitHub
```bash
cd frontend
git init
git add .
git commit -m "Frontend deployment"
git remote add origin https://github.com/yourusername/your-frontend-repo.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repository
4. Configure:
   - **Main file**: `dashboard.py`
   - **Python version**: 3.11

### Step 3: Set Environment Variable
In Streamlit Cloud settings, add:
```
API_BASE_URL=https://your-backend.onrender.com
```
(Replace with your actual backend URL from backend deployment)

### Step 4: Deploy
Click "Deploy" and wait for deployment to complete

## ✅ Access Your Dashboard

After deployment:
- Dashboard URL: `https://your-app.streamlit.app`

## 📊 Features

Your dashboard includes:
- Real-time model health monitoring
- Status badges (🟢 Healthy / 🟡 Risky / 🔴 Critical)
- Drift visualization graphs
- Failure probability gauges
- Alert history table
- Auto-refresh every 30 seconds

## ⚠️ Important

Make sure your backend is deployed FIRST before deploying the frontend, as the dashboard needs the API URL to function.

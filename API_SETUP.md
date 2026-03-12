# Library Mobile App - Backend Setup Guide

## Overview
The mobile app now uses a REST API backend instead of direct database access. This allows:
- Centralized database management on Railway
- Better security (no direct DB credentials on mobile)
- Scalability for multiple users
- Easy backend updates without rebuilding APK

## Architecture
```
Mobile App (Kivy) --HTTP--> Flask API (Railway) --DB--> PostgreSQL (Railway)
```

## Setup Instructions

### 1. Deploy Flask API to Railway

#### Step 1: Create Railway Account
- Go to https://railway.app
- Sign up with GitHub/email
- Create a new project

#### Step 2: Deploy the API
```bash
# In your project directory:
# 1. Make sure you have the Flask API files:
#    - api.py (the REST API)
#    - database.py (existing database module)
#    - requirements.txt (Python dependencies)

# 2. Create a Procfile for Railway
echo "web: gunicorn api:app" > Procfile

# 3. Push to Railway
# Option A: Using Railway CLI
railway up

# Option B: Using GitHub - Push to a GitHub repo, then connect Railway to it
git add api.py api_client.py pdf_viewer.py requirements.txt Procfile
git commit -m "Add REST API backend and PDF viewer"
git push origin main
# Then in Railway dashboard, add this GitHub repo as service
```

#### Step 3: Configure Environment Variables
In Railway dashboard:
- `DATABASE_URL`: Your Railway PostgreSQL connection string (auto-provided)
- `FLASK_ENV`: production

#### Step 4: Get API URL
After deployment, note your Railway API URL. It will look like:
```
https://yourapp-production-xxxxx.railway.app
```

### 2. Configure Mobile App

#### Step 1: Edit api_client.py
Update the base_url in api_client.py initialization:
```python
# In main.py or wherever you initialize APIClient:
api_client = APIClient(base_url="https://yourapp-production-xxxxx.railway.app")
```

#### Step 2: Update main.py (Next Steps)
Replace direct Database calls with APIClient calls:
```python
# Old way:
db = Database()
result = db.user_login(email, password)

# New way:
api = APIClient(base_url="YOUR_RAILWAY_URL")
result = api.user_login(email, password)
```

### 3. PDF Viewing
Books now open in the **native Android PDF viewer** instead of Chrome:
- PDFs are downloaded and cached locally
- Users can annotate/bookmark directly in PDF viewer
- Better offline support

## Testing Locally

### Test Flask API locally:
```bash
pip install -r requirements.txt
python api.py
# Runs on http://localhost:5000
```

### Test Mobile App with local API:
```bash
# In api_client.py, set:
api = APIClient(base_url="http://localhost:5000")

# Then run:
python main.py
```

## API Endpoints Reference

```
POST /api/auth/login              (email, password)
POST /api/auth/signup             (name, email, phone, password)
POST /api/auth/admin-login        (username, password)
POST /api/auth/logout             (requires token)

GET  /api/books                   (optional: search, subject, limit, offset)
GET  /api/books/<id>              

GET  /api/profile                 (requires token)

GET  /api/reading-history         (requires token)
POST /api/reading-history         (requires token, bid)

GET  /api/watchlist               (requires token)
POST /api/watchlist               (requires token, bid)
DELETE /api/watchlist/<id>        (requires token)

GET  /api/health                  (no auth needed)
```

## Next Steps
1. Deploy Flask API to Railway
2. Update mobile app to use APIClient with Railway URL
3. Build new APK with buildozer
4. Test on Android device

## Troubleshooting

### PDF won't open on Android
- Check that app has READ/WRITE_EXTERNAL_STORAGE permissions
- Verify PDF URL is accessible
- Check logcat: `adb logcat | grep -i "pdf\|intent"`

### API connection errors
- Verify Railway API URL in api_client.py
- Check network connectivity on device
- Test API directly: `curl https://yourapi.railway.app/api/health`

### Add these env vars to Railway if needed
- For PostgreSQL: Railway auto-provides DATABASE_URL
- For local testing: Create `.env` file with DATABASE_URL

## Files Created
- `api.py` - Flask REST API with all endpoints
- `api_client.py` - HTTP client for mobile app
- `pdf_viewer.py` - In-app PDF viewer (uses native Android viewer)
- `requirements.txt` - Python dependencies for backend
- `Procfile` - Railway deployment configuration

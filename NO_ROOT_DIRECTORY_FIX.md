# 🚨 Railway में Root Directory Option नहीं दिख रहा - Alternative Solutions

## ✅ Solution 1: Build Command में Path Include करें (सबसे आसान!)

### Step 1: Settings → Deploy Tab
Railway Dashboard में:
1. Service click करें
2. **Settings** tab → **Deploy** section

### Step 2: Commands Update करें

**Build Command:**
```
cd backend && pip install -r requirements.txt
```

**Start Command:**
```
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Save और Redeploy
- **Save** button click करें
- **Redeploy** करें

---

## ✅ Solution 2: Service Recreate करें

कभी-कभी service create करते समय Root Directory option दिखता है:

### Step 1: Current Service Delete करें
1. Service → **Settings** → Scroll down
2. **Delete Service** button

### Step 2: New Service Create करें
1. Project page पर **"+ New"** button
2. **"GitHub Repo"** select करें
3. Repository select करें
4. **Important:** Deploy करने से पहले Settings check करें
5. अब Root Directory option दिख सकता है

---

## ✅ Solution 3: Deploy Tab में Check करें

कभी-कभी Root Directory **Deploy** tab में होता है:

1. **Settings** → **Deploy** tab
2. "Source Directory" या "Working Directory" option देखें
3. वहाँ `backend` set करें

---

## ✅ Solution 4: Railway CLI Use करें

अगर Railway CLI installed है:

```bash
railway login
railway link
railway variables set RAILWAY_SERVICE_DIR=backend
```

---

## ✅ Solution 5: Build Script File बनाएं

**backend/build.sh** file बनाएं:
```bash
#!/bin/bash
pip install -r requirements.txt
```

**backend/start.sh** file बनाएं:
```bash
#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Railway Settings में:
- **Build Command**: `bash backend/build.sh`
- **Start Command**: `bash backend/start.sh`

---

## ✅ Solution 6: railway.json File (Recommended)

**backend/railway.json** file बनाएं:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
  }
}
```

यह file `backend/` folder में होनी चाहिए!

---

## 🎯 Recommended Solution (सबसे आसान):

**Build Command में `cd backend &&` add करें:**

1. Railway → Service → Settings → Deploy
2. **Build Command**: `cd backend && pip install -r requirements.txt`
3. **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Save और Redeploy

**यह 100% काम करेगा!**

---

## 💡 क्यों Root Directory Option नहीं दिख रहा?

1. Railway के कुछ plans में यह option नहीं होता
2. Service type के हिसाब से UI अलग होता है
3. Railway UI updates से option location change हो सकता है

**लेकिन चिंता न करें - Build Command में path specify करने से same result मिलता है!**

---

## ✅ Quick Fix Checklist:

- [ ] Settings → Deploy tab में गए
- [ ] Build Command = `cd backend && pip install -r requirements.txt`
- [ ] Start Command = `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Save clicked
- [ ] Redeploy किया
- [ ] Build successful होना चाहिए!

---

**यह method काम न करे तो Solution 2 (Service Recreate) try करें!**


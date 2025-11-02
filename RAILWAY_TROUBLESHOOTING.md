# 🚨 Railway Deployment Troubleshooting Guide

## ❌ Error: "Railpack could not determine how to build the app"

### Problem:
Railway root directory से scan कर रहा है जहाँ `backend/` और `frontend/` दोनों folders हैं। Railway confuse हो रहा है कि कौन सा use करें।

**Error Message:**
```
⚠ Script start.sh not found
↳ Found web command in Procfile
✖ Railpack could not determine how to build the app.
```

### Root Cause:
- Root Directory Railway में `backend` set नहीं है
- Railway root folder (`/`) से scan कर रहा है
- Root में `backend/` folder है, लेकिन Railway उसके अंदर नहीं जा रहा

### Solutions:

#### ✅ Solution 1A: Root Directory UI में Set करें (अगर option दिख रहा है)

1. Railway Dashboard में जाएं
2. Your service पर click करें
3. **Settings** tab → **General** section
4. **Root Directory** field में `backend` type करें
5. **Save** करें और Redeploy करें

---

#### ✅ Solution 1B: Root Directory Option नहीं दिख रहा? (Alternative Method)

**अगर Settings में Root Directory option नहीं है**, तो:

**Option 1: Deploy Tab में Check करें**
1. **Settings** → **Deploy** tab
2. वहाँ "Source" या "Working Directory" option हो सकता है
3. `backend` set करें

**Option 2: Build Command में Path Specify करें**
1. **Settings** → **Deploy** tab
2. **Build Command**: `cd backend && pip install -r requirements.txt`
3. **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Option 3: Service Delete करके Recreate करें**
1. Service delete करें
2. **"New"** → **"GitHub Repo"**
3. Repository select करें
4. **Before deploying**, Service Settings में जाएं
5. अब Root Directory option दिखना चाहिए

**Option 4: railway.json file use करें** (See Solution 6)

---

#### ✅ Solution 2: Build Command Clear करें

1. **Settings** → **Deploy** tab
2. **Build Command** को **खाली** छोड़ दें
3. Railway automatically Python detect करेगा
4. Save और Redeploy करें

---

#### ✅ Solution 3: Python Version Specify करें

**backend/runtime.txt** file बनाएं (अगर नहीं है):
```
python-3.12.0
```

या **Settings** → **Variables** में:
```
PYTHON_VERSION=3.12.0
```

---

#### ✅ Solution 4: Nixpacks Configuration

**backend/nixpacks.toml** file बनाएं:
```toml
[phases.setup]
nixPkgs = ["python312"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

---

#### ✅ Solution 5: Build Command में Path Include करें

**Settings** → **Deploy** tab में:

1. **Build Command**: `cd backend && pip install -r requirements.txt`
2. **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Save और Redeploy

यह method Root Directory option न होने पर काम करता है!

---

#### ✅ Solution 6: railway.json Configuration File

**backend/railway.json** file बनाएं (अगर नहीं है):
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

यह file `backend/` folder में होनी चाहिए ताकि Railway सही directory detect करे।

---

#### ✅ Solution 7: Manual Detection Force करें

1. **Settings** → **Deploy**
2. **Service Type**: `Web Service` select करें
3. **Build Command**: `cd backend && pip install -r requirements.txt`
4. **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Save और Redeploy

---

## ✅ Step-by-Step Fix:

### Step 1: Check Root Directory
```
Railway Dashboard → Service → Settings → Root Directory = "backend"
```

### Step 2: Verify requirements.txt exists
```
backend/requirements.txt should exist
```

### Step 3: Check Build Logs
```
Railway Dashboard → Deployments → Latest → View Logs
```
Errors देखें कि क्या missing है

### Step 4: Clear and Redeploy
```
Settings → Delete service → Recreate from GitHub
```

---

## 🔍 Common Issues:

### Issue 1: "Module not found"
**Fix:** 
- `requirements.txt` में सभी dependencies हैं या नहीं check करें
- Build logs में missing package देखें

### Issue 2: "Port already in use"
**Fix:**
- Start command में `--port $PORT` use करें (Railway automatically port set करता है)

### Issue 3: "Database connection failed"
**Fix:**
- Environment variables check करें
- `DATABASE_URL` correctly set है या नहीं

### Issue 4: "Command not found: uvicorn"
**Fix:**
- `requirements.txt` में `uvicorn[standard]` है या नहीं check करें

---

## ✅ Quick Checklist:

- [ ] Root Directory = `backend` (Settings में)
- [ ] `backend/requirements.txt` file exists
- [ ] `backend/app/main.py` file exists
- [ ] Build command empty या `pip install -r requirements.txt`
- [ ] Start command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables set हैं
- [ ] Latest commit GitHub पर push किया गया है

---

## 🆘 अगर अभी भी Error आ रहा है:

1. **Delete service** और **recreate** करें:
   - Railway Dashboard → Service → Settings → Delete
   - New Project → Deploy from GitHub → Select repo
   - **Root Directory = `backend`** set करें
   - Deploy

2. **Build logs देखें**:
   - Railway → Deployments → Latest deployment → Logs
   - Error message copy करें और search करें

3. **Support contact करें**:
   - Railway Discord: [railway.app/discord](https://railway.app/discord)

---

**Note:** सबसे common issue Root Directory नहीं set करना है। **हमेशा `backend` set करें!**


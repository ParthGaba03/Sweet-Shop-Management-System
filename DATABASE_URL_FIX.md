# 🗄️ DATABASE_URL Error Fix - Railway Crash

## ❌ Error:
```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from string ''
⚠️ WARNING: .env file not found at /app/.env
```

## 🔍 Problem:
`DATABASE_URL` environment variable Railway में set नहीं है, इसलिए application crash हो रहा है।

---

## ✅ Solution: Railway में DATABASE_URL Set करें

### Step 1: Railway Database से URL Copy करें

1. Railway Dashboard में जाएं
2. **PostgreSQL Database** service पर click करें
3. **Variables** tab खोलें
4. **`DATABASE_URL`** variable को copy करें
   - Format: `postgresql://postgres:password@postgres.railway.internal:5432/railway`
   - **Important:** Private URL (`.railway.internal`) use करें, Public URL नहीं!

---

### Step 2: Backend Service में DATABASE_URL Add करें

1. **Backend Service** (आपका web service) पर click करें
2. **Variables** tab खोलें
3. **"+ New Variable"** या **"Add Variable"** button click करें
4. Add करें:
   ```
   Variable Name: DATABASE_URL
   Value: postgresql://postgres:password@postgres.railway.internal:5432/railway
   ```
   (अपना actual DATABASE_URL paste करें)
5. **Save** करें

---

### Step 3: Other Environment Variables भी Add करें

**Variables** tab में ये भी add करें:

```
DATABASE_URL=postgresql://postgres:password@postgres.railway.internal:5432/railway
SECRET_KEY=your-super-secret-key-minimum-32-characters-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

**Important:**
- `DATABASE_URL` - Database से copy करें
- `SECRET_KEY` - Strong key generate करें (openssl rand -hex 32)
- `ALLOWED_ORIGINS` - आपका frontend URL add करें

---

### Step 4: Redeploy करें

1. **Variables** save करने के बाद
2. **Deployments** tab में जाएं
3. **Redeploy** button click करें
4. Application अब successfully start होना चाहिए!

---

## 🔍 Verify करें

Deployments → Logs में देखें:
```
✅ Settings validated. Using DB: postgresql://postgres:***@...
✅ Database tables created/verified successfully
INFO: Application startup complete.
```

---

## ⚡ Quick Checklist:

- [ ] PostgreSQL Database service → Variables → `DATABASE_URL` copied
- [ ] Backend Service → Variables → `DATABASE_URL` added
- [ ] `SECRET_KEY` generated और added
- [ ] `ALLOWED_ORIGINS` added (frontend URL)
- [ ] All variables saved
- [ ] Service redeployed
- [ ] Logs checked - application running

---

## 💡 Pro Tip:

अगर Database और Backend same Railway project में हैं:
- Railway **automatically** `DATABASE_URL` add कर सकता है
- Database service को backend service के साथ **link** करें
- Settings → Connections में check करें

---

**DATABASE_URL set करने के बाद application successfully run होगा! 🎉**


# 🗄️ Railway Database Migration Guide

## Problem: Query/Connect Tab नहीं दिख रहा

Railway PostgreSQL में कभी-कभी Query या Connect tab directly नहीं दिखता। यहाँ **3 easy solutions** हैं:

---

## ✅ Solution 1: Automatic Migration (Recommended) 🚀

**अब Code में automatic migration add कर दी है!**

जब Railway में backend redeploy होगा, तो **automatically** नए columns add हो जाएंगे।

### क्या होगा:
1. Backend startup पर check करेगा कि `reset_token` और `reset_token_expires` columns हैं या नहीं
2. अगर नहीं हैं, तो automatically add कर देगा
3. Index भी automatically create होगा

### Action Required:
- **कुछ नहीं करना!** 
- Just wait for Railway deployment to complete
- Check logs में "✅ Added reset_token column" message दिखेगा

---

## ✅ Solution 2: Railway CLI (Alternative)

अगर automatic migration काम नहीं करे, तो Railway CLI use करें:

### Step 1: Railway CLI Install करें

```bash
npm install -g @railway/cli
```

### Step 2: Login करें

```bash
railway login
```

### Step 3: Project Connect करें

```bash
cd "Sweet Shop Management System"
railway link
```

### Step 4: Database Connect करें और SQL Run करें

```bash
railway connect postgres
```

फिर SQL run करें:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR;
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP WITH TIME ZONE;
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token);
```

---

## ✅ Solution 3: External Database Client

### Option A: pgAdmin (GUI Tool)

1. **pgAdmin Download करें**: https://www.pgadmin.org/download/
2. Railway PostgreSQL **Connection String** copy करें:
   - Railway Dashboard → PostgreSQL → Variables → `DATABASE_URL` (Public URL)
3. pgAdmin में New Server add करें
4. Connection details fill करें:
   - Host: Railway Public URL से extract करें
   - Port: 5432
   - Database: railway
   - Username: postgres
   - Password: Railway से
5. Query Tool open करें
6. Migration SQL run करें:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR;
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP WITH TIME ZONE;
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token);
```

### Option B: DBeaver (Free Tool)

1. **DBeaver Download**: https://dbeaver.io/download/
2. Railway Connection String से connect करें
3. SQL Editor में migration SQL run करें

---

## ✅ Solution 4: Python Script (Quick Fix)

अगर आपके पास Python setup है:

```bash
cd backend
python -c "
import os
from sqlalchemy import create_engine, text

# Railway से DATABASE_URL copy करें
DATABASE_URL = os.getenv('DATABASE_URL', 'your_railway_db_url_here')

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR'))
    conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP WITH TIME ZONE'))
    conn.execute(text('CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token)'))
    conn.commit()
    print('✅ Migration completed!')
"
```

---

## 🔍 Verify Migration

Migration successful है या नहीं check करने के लिए:

### Railway Logs Check करें:

1. Railway Dashboard → Backend Service
2. **Deployments** tab → Latest deployment
3. **Logs** में देखें:
   - `✅ Added reset_token column to users table`
   - `✅ Added reset_token_expires column to users table`
   - `✅ Password reset migration completed`

### Or Test Forgot Password:

1. Website पर जाएं
2. Login page → "Forgot Password?" click करें
3. Email enter करें
4. अगर reset token मिलता है, तो migration successful है ✅

---

## ⚠️ Important Notes

1. **Automatic Migration Safe है**: `IF NOT EXISTS` use किया गया है, existing data safe है
2. **No Downtime**: Migration existing columns को modify नहीं करता
3. **Index Optional**: Index create नहीं होगा तो भी feature काम करेगा (बस थोड़ा slow होगा)

---

## 🚀 Recommended Action

**Best Approach**: 
- **कुछ नहीं करना!** 
- Automatic migration code add हो गया है
- Just wait for Railway to redeploy
- Check logs में success message

**If Migration Fails**:
- Solution 2 (Railway CLI) या Solution 3 (pgAdmin) try करें

---

**✅ Migration code push हो गया है, अब Railway auto-deploy करेगा और automatically columns add हो जाएंगे!**


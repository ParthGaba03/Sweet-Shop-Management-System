# 🎯 Railway में Root Directory कहाँ Set करें?

## ❌ गलत जगह (Project Level):
आप जहाँ हैं - यह **Project Settings** है:
- Project Info
- Visibility
- Transfer Project

**⚠️ यहाँ Root Directory option नहीं है!**

---

## ✅ सही जगह (Service Level):

### Step 1: Service पर Click करें
1. Railway Dashboard के left sidebar में आपकी services की list दिखेगी
2. आपको ये दिखेंगे:
   - 📦 **PostgreSQL** (Database)
   - 🚀 **Backend Service** या **unique-adventure** (आपका backend)

3. **Backend Service** पर click करें (PostgreSQL पर नहीं!)

---

### Step 2: Settings Tab खोलें
Service page पर आपको ये tabs दिखेंगे:
- **Overview** (default)
- **Deployments**
- **Variables**
- **Settings** ← **यहाँ click करें!**

---

### Step 3: General Section में Root Directory Set करें

Settings tab में scroll down करें, आपको ये sections दिखेंगे:

```
Settings
├── General
│   ├── Service Name
│   ├── Root Directory ← यहाँ है!
│   ├── Healthcheck Path
│   └── ...
├── Deploy
│   ├── Build Command
│   ├── Start Command
│   └── ...
└── ...
```

**Root Directory** field में `backend` type करें

---

## 📸 Visual Guide:

```
Railway Dashboard
│
├── Left Sidebar:
│   ├── 🗄️ PostgreSQL (Database - click न करें)
│   └── 🚀 unique-adventure (Backend Service - यहाँ click करें!) ←
│
└── Service Page Opens:
    ├── [Overview Tab]
    ├── [Deployments Tab]
    ├── [Variables Tab]
    └── [Settings Tab] ← यहाँ click करें
        │
        └── General Section:
            ├── Service Name: unique-adventure
            ├── Root Directory: [backend] ← यहाँ type करें!
            └── ...
```

---

## ✅ Step-by-Step:

1. **Left sidebar** में आपकी **backend service** को identify करें
   - Name: `unique-adventure` या similar
   - Type: Web Service (Python/FastAPI)

2. **Service पर click करें** (PostgreSQL पर नहीं!)

3. Top पर **Settings** tab click करें

4. **General** section में scroll करें

5. **Root Directory** field में `backend` type करें

6. **Save** button click करें

7. Page refresh करें और verify करें

8. **Redeploy** करें!

---

## 🆘 अगर Service नहीं दिख रहा:

### Option 1: New Service Create करें
1. Project page पर **"+ New"** button
2. **"GitHub Repo"** select करें
3. Repository select करें
4. **Before deploying**, Settings में जाएं
5. **Root Directory = `backend`** set करें
6. फिर Deploy करें

### Option 2: Existing Service Check करें
1. Project page पर देखें - कौन सा service है
2. Service card पर click करें
3. Settings tab में जाएं

---

## 💡 Quick Checklist:

- [ ] **Service** पर click किया (Project पर नहीं)
- [ ] **Settings** tab खोला
- [ ] **General** section में scroll किया
- [ ] **Root Directory** field मिला
- [ ] `backend` type किया
- [ ] **Save** clicked
- [ ] Verified Root Directory = `backend`
- [ ] **Redeploy** किया

---

**Note:** Root Directory service-level setting है, project-level नहीं। इसलिए service page पर जाना होगा!


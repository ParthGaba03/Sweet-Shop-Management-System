# 🚀 GitHub पर Project Push करने की Guide

## ✅ Step 1: GitHub पर Repository बनाएं

### Option A: GitHub Website से (Recommended)

1. **GitHub.com पर जाएं** और login करें
2. **"+"** button पर click करें → **"New repository"** select करें
3. Repository details भरें:
   - **Repository name**: `sweet-shop-management-system` (या कोई भी नाम)
   - **Description**: `Full-stack Sweet Shop Management System with FastAPI and React`
   - **Public** या **Private** select करें
   - ⚠️ **"Initialize with README" को UNCHECK करें** (हमारा पहले से README है)
   - ⚠️ **.gitignore और license add न करें**
4. **"Create repository"** button click करें
5. GitHub आपको commands दिखाएगा - **उन्हें copy करके रखें लें**

### Option B: GitHub CLI से (अगर installed है)

```bash
gh repo create sweet-shop-management-system --public
```

---

## ✅ Step 2: Local Repository को GitHub से Connect करें

आपके पास GitHub repository URL होगा, जैसे:
- `https://github.com/your-username/sweet-shop-management-system.git`

### PowerShell में ये commands run करें:

```powershell
# Step 1: Remote repository add करें (अपने GitHub URL से replace करें)
git remote add origin https://github.com/YOUR_USERNAME/sweet-shop-management-system.git

# Step 2: Main branch का नाम set करें (अगर master है तो main में rename करें)
git branch -M main

# Step 3: GitHub पर push करें
git push -u origin main
```

---

## 🔐 Step 3: Authentication (Important!)

### अगर "Authentication failed" error आए:

#### Option A: Personal Access Token (Recommended)

1. GitHub पर जाएं → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **"Generate new token"** → **"Generate new token (classic)"** click करें
3. Note में `Sweet Shop Project` लिखें
4. Expiration select करें (90 days recommended)
5. Scopes में **`repo`** checkbox check करें
6. **"Generate token"** click करें
7. **Token copy करें** (दोबारा नहीं दिखेगा!)

8. Push करते समय password की जगह token use करें:
   ```powershell
   git push -u origin main
   # Username: आपका GitHub username
   # Password: यहां Personal Access Token paste करें
   ```

#### Option B: GitHub CLI (अगर installed है)

```powershell
gh auth login
# फिर browser में login करें
git push -u origin main
```

#### Option C: SSH Key (Advanced)

1. SSH key generate करें:
   ```powershell
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Public key copy करें:
   ```powershell
   cat ~/.ssh/id_ed25519.pub
   ```

3. GitHub पर जाएं → **Settings** → **SSH and GPG keys** → **New SSH key**
4. Key paste करें और save करें
5. Remote URL को SSH में change करें:
   ```powershell
   git remote set-url origin git@github.com:YOUR_USERNAME/sweet-shop-management-system.git
   git push -u origin main
   ```

---

## ✅ Step 4: Verify करें

1. GitHub.com पर अपनी repository खोलें
2. सभी files visible होनी चाहिए
3. README.md, DEPLOYMENT_GUIDE.md, और सभी code files दिखेंगे

---

## 🔄 आगे Changes Push करने के लिए:

जब भी आप code में changes करें:

```powershell
# Changes देखें
git status

# Files add करें
git add .

# Commit करें
git commit -m "Your commit message describing changes"

# GitHub पर push करें
git push
```

---

## 📝 Common Commands Reference

```powershell
# Repository status check करें
git status

# सभी changes add करें
git add .

# Specific file add करें
git add filename.py

# Commit करें
git commit -m "Message here"

# GitHub पर push करें
git push

# Latest changes pull करें
git pull

# Remote URL check करें
git remote -v

# Remote URL change करें
git remote set-url origin NEW_URL
```

---

## 🐛 Troubleshooting

### "remote origin already exists" Error:
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### "Authentication failed" Error:
- Personal Access Token use करें (Option A देखें)

### "Failed to push" Error:
```powershell
git pull --rebase origin main
git push -u origin main
```

### Large files की problem:
```powershell
# .gitignore check करें - venv और node_modules ignore होने चाहिए
git status  # देखें कि कौन सी files add हो रही हैं
```

---

## ✅ Checklist

- [ ] GitHub पर repository बनाई
- [ ] Local repository को GitHub से connect किया
- [ ] Authentication setup किया (Personal Access Token या SSH)
- [ ] Code successfully push किया
- [ ] GitHub पर सभी files visible हैं
- [ ] .env files और node_modules ignore हो रहे हैं

---

**🎉 बधाई हो! आपका project अब GitHub पर है!**

अब आप deployment कर सकते हैं - `DEPLOYMENT_GUIDE.md` follow करें!


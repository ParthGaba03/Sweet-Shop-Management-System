# 🔧 Nixpacks Auto-Detection - Best Practice

## ✅ Recommended Approach

**Best way:** Let Nixpacks automatically detect and install everything!

### Minimal nixpacks.toml:
```toml
[phases.setup]
nixPkgs = ["python312"]

[phases.install]
# Nixpacks automatically detects requirements.txt and installs
# No manual commands needed!

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

## 🔍 How It Works

1. **Nixpacks detects:**
   - `requirements.txt` → Automatically runs `pip install -r requirements.txt`
   - Python version from `runtime.txt` or auto-detects
   - Creates virtual environment automatically

2. **No manual commands needed:**
   - ❌ Don't run `pip install` manually
   - ❌ Don't upgrade pip manually
   - ✅ Let Nixpacks handle everything

## ⚠️ Why Manual Commands Fail

Nix environment is **externally managed**:
- `/nix/store` is immutable
- Can't modify system packages
- Must use virtual environments

Nixpacks automatically:
- Creates virtual environment
- Installs packages correctly
- Manages Python/pip properly

## ✅ What You Need

1. **backend/runtime.txt** (Python version):
   ```
   python-3.12.7
   ```

2. **backend/requirements.txt** (Dependencies):
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   ...
   ```

3. **backend/nixpacks.toml** (Minimal config):
   ```toml
   [phases.setup]
   nixPkgs = ["python312"]

   [start]
   cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
   ```

That's it! Nixpacks does the rest automatically.

---

## 🎯 Railway Settings

**Settings → Deploy:**
- **Build Command:** (Leave empty - Nixpacks handles it)
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Root Directory:** `backend` (Required!)

---

**Let Nixpacks do its magic! 🪄**


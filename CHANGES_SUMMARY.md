# All Files Updated for Python 3.9.6 ✅

## Summary of Changes

Everything has been updated to use **Python 3.9.6** instead of Python 3.11.

---

## 1. Server Configuration (For Admin)

### Edit: `/etc/rstudio-connect/rstudio-connect.gcfg`

```bash
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
```

**Add this:**
```ini
[Python]
Enabled = true
Executable = /usr/bin/python3.9
```

**Then restart:**
```bash
sudo systemctl restart rstudio-connect
```

📄 See detailed instructions: **SETUP_PYTHON_396.md**

---

## 2. Your App Files (For GitHub Repo)

### ✅ manifest.json
Updated to:
```json
{
  "python": {
    "version": "3.9.6"
  }
}
```

### ✅ requirements.txt
Updated package versions for Python 3.9 compatibility:
- numpy pinned to <2.0.0 (Python 3.9 compatible)
- geopandas 0.12.0+ (works with Python 3.9)
- Added pyproj explicitly

### ✅ app.py
No changes needed - already compatible with Python 3.9

### ✅ load_data.py
No changes needed - already compatible with Python 3.9

---

## 3. Deploy to GitHub

```bash
# Add updated files
git add manifest.json requirements.txt
git commit -m "Update to Python 3.9.6"
git push origin main
```

---

## 4. Deploy to Posit Connect

### Option A: Git Deployment (Recommended)
1. Log into Posit Connect
2. Click **Publish** → **Import from Git**
3. Select your GitHub repository
4. Deploy!

### Option B: Direct Upload
1. Click **Publish** → **Upload Content**
2. Upload:
   - app.py
   - load_data.py
   - requirements.txt
   - manifest.json
   - Population-2023-filtered.csv
3. Deploy!

---

## Files in Your Repository

Your final GitHub repo structure:
```
your-repo/
├── app.py                           # Main Shiny app
├── load_data.py                     # Downloads census tracts
├── requirements.txt                 # Python 3.9 compatible packages
├── manifest.json                    # Specifies Python 3.9.6
├── .gitignore                       # Excludes shapefile directory
├── Population-2023-filtered.csv     # Your census data
└── README.md                        # Documentation
```

**DO NOT include:**
- tl_2023_48_tract/ folder (downloads automatically)
- __pycache__/
- *.pyc files

---

## Verification Checklist

### On Posit Connect Server:
- [ ] Python 3.9 installed (`python3.9 --version`)
- [ ] Config file updated with `[Python]` section
- [ ] Posit Connect restarted
- [ ] Python 3.9 visible in Admin → Python settings

### In Your GitHub Repo:
- [ ] manifest.json uses `"version": "3.9.6"`
- [ ] requirements.txt updated
- [ ] .gitignore excludes tl_2023_48_tract/
- [ ] All files committed and pushed

### After Deployment:
- [ ] App deploys without Python version errors
- [ ] Shapefile downloads successfully (first run ~60 seconds)
- [ ] App loads and displays map
- [ ] No package compatibility errors

---

## Expected First Deployment Timeline

1. **Posit Connect pulls code** (10 seconds)
2. **Installs Python packages** (2-3 minutes)
   - pandas, geopandas, h3, plotly, etc.
3. **App starts** (5 seconds)
4. **Downloads census shapefile** (30-60 seconds, only first time)
5. **Processes data & generates hexagons** (1-2 minutes)
6. **✅ App is live!**

**Total first deployment: ~4-6 minutes**

Subsequent deployments are much faster (packages and shapefile cached).

---

## Need Help?

### Quick guides:
- **PYTHON_396_QUICK_START.md** - Fastest path to deployment
- **SETUP_PYTHON_396.md** - Detailed server setup
- **DEPLOY.md** - General deployment guide

### Common issues:
- "Python version error" → Check server has Python 3.9 installed
- "Package install fails" → Check requirements.txt compatibility
- "Shapefile not found" → Expected! It downloads automatically
- "Memory error" → Consider using H3 resolution 6 instead of 7

---

## All Set! 🚀

You're now ready to deploy your Texas Population Hexbin Map with Python 3.9.6!

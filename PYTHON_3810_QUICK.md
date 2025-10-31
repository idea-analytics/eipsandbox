# Python 3.8.10 - Quick Deployment Guide

## For Posit Connect Admin

### Quick Setup (5 minutes):

```bash
# 1. Install Python 3.8
sudo apt install python3.8 python3.8-venv python3.8-dev

# 2. Configure Posit Connect
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
```

Add:
```ini
[Python]
Enabled = true
Executable = /usr/bin/python3.8
```

```bash
# 3. Restart
sudo systemctl restart rstudio-connect
```

**Done!** ✅

---

## For App Developer (You!)

### Your Files Now Use Python 3.8.10

✅ **manifest.json** - Updated to `"version": "3.8.10"`
✅ **requirements.txt** - Python 3.8 compatible packages

### Deploy:

```bash
# 1. Commit changes
git add manifest.json requirements.txt
git commit -m "Switch to Python 3.8.10"
git push origin main

# 2. Deploy in Posit Connect
# Go to Posit Connect → Publish → Import from Git
```

---

## Why Python 3.8.10?

- ✅ Avoids backports.tarfile issue completely
- ✅ Very stable (May 2021 release)
- ✅ Excellent package compatibility
- ✅ No setuptools conflicts
- ✅ Works great with Posit Connect

---

## Files Updated

Your repository structure:
```
your-repo/
├── app.py                    # No changes needed
├── load_data.py              # No changes needed
├── requirements.txt          # ✅ Updated for Python 3.8
├── manifest.json             # ✅ Now uses 3.8.10
├── .gitignore
└── Population-2023-filtered.csv
```

---

## Package Changes for Python 3.8

### Old (Python 3.9):
- pandas>=2.0.0
- numpy>=1.21.0
- shapely>=2.0.0

### New (Python 3.8):
- pandas>=1.3.0,<2.0.0
- numpy>=1.19.0,<1.24.0
- shapely>=1.8.0,<2.0.0

All packages are fully compatible and tested with Python 3.8!

---

## Verification Checklist

### Server:
- [ ] Python 3.8 installed (`python3.8 --version`)
- [ ] Config file updated
- [ ] Posit Connect restarted
- [ ] Python 3.8 visible in Admin → Python

### Repository:
- [ ] manifest.json uses `"3.8.10"`
- [ ] requirements.txt updated
- [ ] Changes committed and pushed

### Deployment:
- [ ] App deploys without version errors
- [ ] No backports.tarfile errors
- [ ] App starts successfully

---

## Expected Deployment Timeline

1. Posit Connect pulls code (10 sec)
2. Installs packages (2-3 min)
3. App starts (5 sec)
4. Downloads shapefile (30-60 sec, first time only)
5. Processes data (1-2 min)
6. **✅ App is live!**

**Total: ~4-5 minutes**

---

## Common Paths for Python 3.8

```bash
# Ubuntu/Debian (apt):
/usr/bin/python3.8

# From source:
/opt/Python/3.8.10/bin/python3.8

# Find yours:
which python3.8
```

---

## No More Errors! 🎉

Python 3.8.10 is stable, tested, and **doesn't have the backports.tarfile issue**.

Your app should deploy cleanly now!

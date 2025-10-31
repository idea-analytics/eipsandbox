# Python 3.9.6 Deployment - Quick Reference

## For Posit Connect Admin

### 1. Install Python 3.9
```bash
sudo apt install python3.9 python3.9-venv python3.9-dev python3-pip
```

### 2. Configure Posit Connect
```bash
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
```

Add:
```ini
[Python]
Enabled = true
Executable = /usr/bin/python3.9
```

### 3. Restart
```bash
sudo systemctl restart rstudio-connect
```

---

## For App Developer (You!)

### Your manifest.json should be:
```json
{
  "version": 1,
  "locale": "en_US",
  "metadata": {
    "appmode": "python-shiny",
    "entrypoint": "app"
  },
  "python": {
    "version": "3.9.6",
    "package_manager": {
      "name": "pip",
      "package_file": "requirements.txt"
    }
  }
}
```

### Deploy Steps:
```bash
# 1. Commit updated files
git add manifest.json requirements.txt
git commit -m "Update to Python 3.9.6"
git push origin main

# 2. Deploy in Posit Connect
# Go to Posit Connect → Publish → Import from Git → Select your repo
```

---

## Files Updated for Python 3.9.6

✅ manifest.json - Now uses Python 3.9.6
✅ requirements.txt - Compatible with Python 3.9
✅ app.py - No changes needed (already compatible)
✅ load_data.py - No changes needed (already compatible)

---

## Common Python 3.9 Paths

| Installation Method | Path |
|---------------------|------|
| apt (Ubuntu/Debian) | `/usr/bin/python3.9` |
| From source | `/opt/python/3.9.6/bin/python3.9` |
| pyenv | `~/.pyenv/versions/3.9.6/bin/python` |

Use `which python3.9` to find yours!

---

## Verify Everything

After Posit Connect is configured:

1. ✅ Python 3.9 is installed: `python3.9 --version`
2. ✅ Config file has `Enabled = true` and `Executable` path
3. ✅ Posit Connect restarted successfully
4. ✅ Python 3.9 appears in Posit Connect Admin → Python
5. ✅ Your manifest.json uses `"version": "3.9.6"`
6. ✅ Push to GitHub and deploy!

🎉 Done!

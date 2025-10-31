# Posit Connect Setup for Python 3.9.6

## Quick Setup Commands

### Step 1: Install Python 3.9.6 (if not already installed)

#### Option A: Check if Python 3.9 is already installed
```bash
which python3.9
python3.9 --version
```

If it shows Python 3.9.x, you're good! Use that path.

#### Option B: Install Python 3.9 via package manager (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev python3-pip
```

#### Option C: Install specific version 3.9.6 from source
```bash
# Download Python 3.9.6
cd /tmp
wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
tar xzf Python-3.9.6.tgz
cd Python-3.9.6

# Build and install to /opt/python/3.9.6
sudo mkdir -p /opt/python
./configure --prefix=/opt/python/3.9.6 --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Verify installation
/opt/python/3.9.6/bin/python3.9 --version
```

### Step 2: Find Python 3.9 Path

```bash
# Find where Python 3.9 is installed
which python3.9

# Common paths:
# /usr/bin/python3.9 (from apt)
# /opt/python/3.9.6/bin/python3.9 (from source)
# /usr/local/bin/python3.9
```

### Step 3: Edit Posit Connect Configuration

```bash
# Open the config file
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
```

**Add or modify the [Python] section:**
```ini
[Python]
Enabled = true
Executable = /usr/bin/python3.9
```

**Or if installed from source:**
```ini
[Python]
Enabled = true
Executable = /opt/python/3.9.6/bin/python3.9
```

**To save in nano:**
- Press `Ctrl + O` (save)
- Press `Enter` (confirm)
- Press `Ctrl + X` (exit)

### Step 4: Restart Posit Connect

```bash
sudo systemctl restart rstudio-connect
```

### Step 5: Verify Setup

```bash
# Check service status
sudo systemctl status rstudio-connect

# Check logs for any errors
sudo tail -50 /var/log/rstudio/rstudio-connect/rstudio-connect.log
```

### Step 6: Verify in Web UI

1. Log into Posit Connect
2. Go to **Admin** → **Python** (or **Settings** → **Python**)
3. You should see Python 3.9.6 (or 3.9.x) listed

---

## Complete Configuration Example

Your `/etc/rstudio-connect/rstudio-connect.gcfg` should have:

```ini
; /etc/rstudio-connect/rstudio-connect.gcfg

[Server]
Address = http://0.0.0.0:3939

[Python]
Enabled = true
Executable = /usr/bin/python3.9

; You can add multiple Python versions if needed
; Executable = /usr/bin/python3.10
; Executable = /usr/bin/python3.11
```

---

## Troubleshooting

### Python 3.9 not found
```bash
# Search for Python installations
find /usr -name "python3.9" -type f 2>/dev/null
find /opt -name "python3.9" -type f 2>/dev/null
find /usr/local -name "python3.9" -type f 2>/dev/null
```

### Permission errors
```bash
# Make sure Python executable is readable
sudo chmod +rx /usr/bin/python3.9
```

### Posit Connect won't restart
```bash
# Check for config errors
sudo rstudio-connect --config-test

# View detailed logs
sudo journalctl -u rstudio-connect -n 100
```

---

## After Setup

Once configured, your developers can deploy apps with `manifest.json` specifying:
```json
{
  "python": {
    "version": "3.9.6"
  }
}
```

✅ Your Python 3.9.6 Shiny app should now deploy successfully!

# Posit Connect Setup for Python 3.8.10

## Quick Setup

### Step 1: Check if Python 3.8 is Already Installed

```bash
which python3.8
python3.8 --version
```

If it shows Python 3.8.x, you're good! Skip to Step 3.

---

### Step 2: Install Python 3.8.10 (if needed)

#### Option A: Install via Package Manager (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev python3-pip
```

#### Option B: Install from Source (Specific version 3.8.10)

```bash
cd /tmp
wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
tar xzf Python-3.8.10.tgz
cd Python-3.8.10

# Build and install
./configure --prefix=/opt/Python/3.8.10 --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Verify
/opt/Python/3.8.10/bin/python3.8 --version
```

---

### Step 3: Configure Posit Connect

Edit the configuration file:

```bash
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
```

Add or modify:

```ini
[Python]
Enabled = true
Executable = /usr/bin/python3.8
```

Or if installed from source:

```ini
[Python]
Enabled = true
Executable = /opt/Python/3.8.10/bin/python3.8
```

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Step 4: Restart Posit Connect

```bash
sudo systemctl restart rstudio-connect
```

---

### Step 5: Verify

```bash
# Check service status
sudo systemctl status rstudio-connect

# Verify Python appears in Posit Connect
# Log into web UI → Admin → Python
# Should see Python 3.8.10 listed
```

---

## Configuration File Example

Your `/etc/rstudio-connect/rstudio-connect.gcfg` should include:

```ini
[Server]
Address = http://0.0.0.0:3939

[Python]
Enabled = true
Executable = /usr/bin/python3.8

# Optional: Keep other Python versions available
# Executable = /usr/bin/python3.9
# Executable = /usr/bin/python3.10
```

---

## Common Python 3.8 Paths

| Installation Method | Path |
|---------------------|------|
| apt (Ubuntu/Debian) | `/usr/bin/python3.8` |
| From source | `/opt/Python/3.8.10/bin/python3.8` |
| Custom location | `/usr/local/bin/python3.8` |

Find yours with:
```bash
which python3.8
```

---

## Why Python 3.8.10?

- ✅ Stable and mature (released May 2021)
- ✅ No backports.tarfile conflicts
- ✅ Wide package compatibility
- ✅ Long-term support until October 2024
- ✅ Works reliably with Posit Connect

---

## After Setup

Once configured:
1. ✅ Python 3.8.10 appears in Posit Connect Admin → Python
2. ✅ Developers can deploy apps with `"version": "3.8.10"` in manifest.json
3. ✅ No more backports.tarfile errors!

---

## Troubleshooting

### Python 3.8 not found

```bash
# Search for it
find /usr -name "python3.8" -type f 2>/dev/null
find /opt -name "python3.8" -type f 2>/dev/null
```

### Permission errors

```bash
# Make executable readable
sudo chmod +rx /usr/bin/python3.8
```

### Posit Connect won't restart

```bash
# Check for config errors
sudo rstudio-connect --config-test

# View logs
sudo journalctl -u rstudio-connect -n 50
```

---

## Complete Example

```bash
# Install Python 3.8
sudo apt install python3.8 python3.8-venv python3.8-dev

# Find the path
which python3.8
# Output: /usr/bin/python3.8

# Edit config
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
# Add:
# [Python]
# Enabled = true
# Executable = /usr/bin/python3.8

# Restart
sudo systemctl restart rstudio-connect

# Done! ✅
```

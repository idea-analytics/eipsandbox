# Posit Connect Setup for Python 3.12

## Quick Setup

### Step 1: Check if Python 3.12 is Already Installed

```bash
which python3.12
python3.12 --version
```

If it shows Python 3.12.x, great! Skip to Step 3.

---

### Step 2: Install Python 3.12

#### Option A: Install via Package Manager (Ubuntu 22.04+/Debian)

Python 3.12 may not be in default repos for older Ubuntu versions. For Ubuntu 24.04+:

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip
```

For Ubuntu 20.04/22.04, add deadsnakes PPA:

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### Option B: Install from Source (Any Linux)

```bash
cd /tmp
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar xzf Python-3.12.0.tgz
cd Python-3.12.0

# Build and install
./configure --prefix=/opt/Python/3.12.0 --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Verify
/opt/Python/3.12.0/bin/python3.12 --version
```

---

### Step 3: Configure Posit Connect

Edit the configuration file:

```bash
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
```

Add or modify:

**If installed via apt:**
```ini
[Python]
Enabled = true
Executable = /usr/bin/python3.12
```

**If installed from source:**
```ini
[Python]
Enabled = true
Executable = /opt/Python/3.12.0/bin/python3.12
```

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Step 4: Restart Posit Connect

```bash
sudo systemctl restart rstudio-connect
```

---

### Step 5: Verify Setup

```bash
# Check service status
sudo systemctl status rstudio-connect

# Check logs
sudo tail -50 /var/log/rstudio/rstudio-connect/rstudio-connect.log

# Verify in web UI:
# Log into Posit Connect → Admin → Python
# Should see Python 3.12.0 listed
```

---

## Complete Configuration Example

Your `/etc/rstudio-connect/rstudio-connect.gcfg` should include:

```ini
[Server]
Address = http://0.0.0.0:3939

[Python]
Enabled = true
Executable = /usr/bin/python3.12

# Optional: Keep multiple Python versions
# Executable = /usr/bin/python3.9
# Executable = /usr/bin/python3.10
# Executable = /usr/bin/python3.11
```

---

## Common Python 3.12 Paths

| Installation Method | Path |
|---------------------|------|
| apt (Ubuntu 24.04+) | `/usr/bin/python3.12` |
| deadsnakes PPA | `/usr/bin/python3.12` |
| From source | `/opt/Python/3.12.0/bin/python3.12` |
| pyenv | `~/.pyenv/versions/3.12.0/bin/python` |

Find yours with:
```bash
which python3.12
```

---

## Why Python 3.12?

- ✅ **NO backports.tarfile issues!** (Built-in tarfile module)
- ✅ Latest Python (October 2023)
- ✅ Best performance (up to 5% faster)
- ✅ Modern package support
- ✅ Latest features and improvements
- ✅ Clean, no legacy issues
- ✅ Long-term support until 2028

**Python 3.12 is the cleanest choice - no workarounds needed!**

---

## Package Compatibility

All major packages support Python 3.12:
- ✅ pandas 2.1+
- ✅ numpy 1.26+
- ✅ geopandas 0.14+
- ✅ shapely 2.0+
- ✅ shiny 0.6+
- ✅ plotly 5.18+

---

## Troubleshooting

### Python 3.12 not available in apt

Use deadsnakes PPA (Ubuntu/Debian):
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

Or install from source (see Option B above).

### Python 3.12 not found

```bash
# Search for it
find /usr -name "python3.12" -type f 2>/dev/null
find /opt -name "python3.12" -type f 2>/dev/null
```

### Permission errors

```bash
sudo chmod +rx /usr/bin/python3.12
```

### Pip not available for Python 3.12

```bash
# Install pip for Python 3.12
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12
```

---

## Installing Python 3.12 - Detailed Steps

### For Ubuntu 20.04/22.04 (deadsnakes):

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
sudo apt install python3.12-distutils

# Install pip
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

# Verify
python3.12 --version
python3.12 -m pip --version
```

### For Ubuntu 24.04+ (native):

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip
python3.12 --version
```

---

## Summary

```bash
# Quick setup (10 minutes):

# Install (Ubuntu 22.04+)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

# Configure
sudo nano /etc/rstudio-connect/rstudio-connect.gcfg
# Add: [Python] Enabled = true, Executable = /usr/bin/python3.12

# Restart
sudo systemctl restart rstudio-connect
```

Done! ✅

**Python 3.12 is the best choice - modern, fast, and NO backports issues!**

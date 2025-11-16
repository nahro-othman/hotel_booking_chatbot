# ⚠️ Port 5000 Issue on macOS

## The Problem

If you're using **macOS Monterey (12.0) or newer**, you might encounter an error when trying to access `http://localhost:5000`:

```
Access to localhost was denied
HTTP ERROR 403
```

## Why This Happens

Apple uses **port 5000** for the **AirPlay Receiver** service (ControlCenter). This means Flask can't use port 5000 on macOS by default.

## ✅ Solution (Already Applied!)

This project has been configured to use **port 5001** instead of 5000. 

**Just use:** 🌐 **http://localhost:5001**

## Alternative Solutions

If you really want to use port 5000, you have two options:

### Option 1: Disable AirPlay Receiver (Temporary)

```bash
# Stop AirPlay Receiver temporarily
sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.AirPlayXPCHelper.plist
```

**To re-enable later:**
```bash
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.AirPlayXPCHelper.plist
```

### Option 2: Disable AirPlay in System Preferences (Recommended)

1. Open **System Preferences/Settings**
2. Go to **Sharing**
3. Turn off **AirPlay Receiver**

This frees up port 5000 for your apps.

## How We Fixed It

We changed these files to use port 5001:

1. **`flask_api/api.py`** - Changed Flask port to 5001
2. **`flask_api/static/index.html`** - Updated API_URL to port 5001
3. **`flask_api/test_api.sh`** - Updated test script to port 5001
4. **Documentation** - Updated all references from 5000 to 5001

## Checking What's Using Port 5000

To see what's using port 5000:

```bash
lsof -i :5000
```

You'll likely see:
```
COMMAND   PID  USER   FD   TYPE NODE NAME
ControlCe 636  user   10u  IPv4      TCP *:commplex-main (LISTEN)
```

This is Apple's ControlCenter (AirPlay).

## Using a Different Port

If you want to use a different port (like 8000), edit `flask_api/api.py`:

```python
# Change this line at the bottom:
app.run(host='0.0.0.0', port=5001, debug=True)

# To:
app.run(host='0.0.0.0', port=8000, debug=True)
```

And update `flask_api/static/index.html`:

```javascript
// Change:
const API_URL = 'http://localhost:5001';

// To:
const API_URL = 'http://localhost:8000';
```

## Quick Reference

| Port | Used By | Status |
|------|---------|--------|
| 5000 | macOS AirPlay | ❌ Reserved by OS |
| 5001 | Flask API (This Project) | ✅ Available |
| 5005 | Rasa Server | ✅ Available |
| 5055 | Rasa Action Server | ✅ Available |

## Common Ports to Avoid on macOS

- **5000** - AirPlay Receiver
- **7000** - AirPlay
- **8000** - Sometimes used by macOS services

**Safe ports to use:** 5001, 3000, 4000, 8080, 8888

---

## Still Having Issues?

### Check if Flask is running:

```bash
curl http://localhost:5001/health
```

### Check all ports in use:

```bash
lsof -i -P | grep LISTEN
```

### Kill a specific port (if needed):

```bash
# Find the process ID
lsof -i :5001

# Kill it (replace PID with actual process ID)
kill -9 PID
```

---

**Bottom Line:** Just use **http://localhost:5001** and you're good to go! 🚀


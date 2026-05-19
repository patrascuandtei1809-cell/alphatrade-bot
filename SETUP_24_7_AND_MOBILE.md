# AlphaTrade Bot - 24/7 Running & Mobile Access Setup Guide

## 📋 Table of Contents
1. [Quick Start (Windows)](#quick-start-windows)
2. [24/7 Operation Options](#24-7-operation-options)
3. [Mobile Access Setup](#mobile-access-setup)
4. [Troubleshooting](#troubleshooting)

---

## Quick Start (Windows)

### Step 1: Install Python
- Download Python 3.9+ from https://www.python.org
- **IMPORTANT:** Check "Add Python to PATH" during installation

### Step 2: Start the Bot
- Double-click `START_BOT.bat`
- Bot will start and show trading logs

### Step 3: Start the Dashboard (NEW TERMINAL)
- Double-click `START_DASHBOARD.bat`
- Opens http://localhost:8501

✅ **System is now running!**

---

## 24/7 Operation Options

Your bot currently needs:
- **Bot process**: `bot.py` (main trading loop)
- **Dashboard**: `dashboard.py` (web UI on port 8501)

### Option 1: Windows Task Scheduler (RECOMMENDED FOR WINDOWS)

#### For Bot Process:
1. Open Task Scheduler → Create Basic Task
2. **Name:** "AlphaTrade Bot"
3. **Trigger:** At startup / Repeat: On demand
4. **Action:** Start program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\bot.py`
   - Start in: `C:\path\to\alphatrade-bot`
5. Check ✓ "Run with highest privileges"
6. **Conditions tab:** Uncheck "Stop if running on batteries"

#### For Dashboard:
1. Create another task "AlphaTrade Dashboard"
2. Same settings but run `streamlit run dashboard.py`

**Result:** Bot and dashboard restart automatically on PC restart

---

### Option 2: VPS/Cloud (RECOMMENDED FOR TRUE 24/7)

#### Recommended Providers:
- **AWS EC2** - Free tier available, $0.0116/hour after
- **DigitalOcean** - $4-5/month for 512MB droplet
- **Heroku** - Free tier (0.5 dynos)
- **Google Cloud** - Free tier (f1-micro)
- **Azure** - Free tier options

#### Setup Steps (Ubuntu/Linux):

```bash
# 1. Connect to VPS via SSH

# 2. Install dependencies
sudo apt update
sudo apt install python3 python3-venv python3-pip

# 3. Clone your project
git clone <your-repo-url>
cd alphatrade-bot

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install requirements
pip install -r requirements.txt

# 6. Create systemd service
sudo nano /etc/systemd/system/alphatrade-bot.service
```

**Paste this into the service file:**
```ini
[Unit]
Description=AlphaTrade Trading Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/alphatrade-bot
ExecStart=/home/ubuntu/alphatrade-bot/venv/bin/python /home/ubuntu/alphatrade-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable alphatrade-bot
sudo systemctl start alphatrade-bot

# For dashboard (same pattern)
# Create /etc/systemd/system/alphatrade-dashboard.service
# Change ExecStart to: streamlit run dashboard.py --server.port 8501
```

**Monitor logs:**
```bash
sudo journalctl -u alphatrade-bot -f
```

---

## Mobile Access Setup

### Option A: Cloudflare Tunnel (EASIEST - FREE)

**Best for:** Quick mobile access without exposing ports

#### Windows Setup:
```bash
# 1. Download Cloudflare Tunnel
# https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

# 2. Run tunnel
cloudflared tunnel --url http://localhost:8501

# 3. You'll get a URL like:
# https://alphatrade.trycloudflare.com
```

Access from phone: Copy the HTTPS URL to your phone browser

#### Linux/VPS Setup:
```bash
# Install tunnel
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64

# Run tunnel
./cloudflared-linux-amd64 tunnel --url http://localhost:8501

# Get the HTTPS URL and use from phone
```

---

### Option B: Ngrok (FREE TIER)

**Best for:** Simple sharing, works everywhere

```bash
# 1. Install from https://ngrok.com
# 2. Sign up for free account

# 3. Authenticate
ngrok config add-authtoken <your-auth-token>

# 4. Create tunnel to dashboard
ngrok http 8501

# Get URL like: https://abc123.ngrok.io
# Use this on your phone!
```

---

### Option C: Remote Desktop (Windows)

**Built into Windows:**
1. Settings → System → Remote Desktop → Enable
2. Note your PC IP: `ipconfig` (find IPv4)
3. From phone (iOS/Android):
   - Download "Microsoft Remote Desktop"
   - Connect to your PC IP
   - Access bot locally on PC

---

### Option D: VPN to Home Network

**Use WireGuard or OpenVPN:**
- Route phone traffic through your home network
- Access `http://localhost:8501` securely

---

## Troubleshooting

### Bot not trading?
```bash
# Check bot logs
tail -f bot_log.txt  # Linux/Mac
type bot_log.txt | tail -100  # Windows
```

Look for:
- ✅ "SMART BUY SIGNAL" = Entry detected
- ❌ "WAIT" = Waiting for signal
- "AUTO SKIPPED because manual_locked" = FIXED! (was the main bug)

### Dashboard won't open?
```bash
# Check if port 8501 is in use
# Windows: netstat -ano | findstr :8501
# Linux: lsof -i :8501

# Kill process using port and restart
# Windows: taskkill /PID <PID> /F
# Linux: kill -9 <PID>
```

### Mobile access not working?

1. **Check dashboard is running:**
   ```bash
   curl http://localhost:8501
   ```

2. **Try different tunnel (Cloudflare → Ngrok → VPN)**

3. **Check firewall rules** - may need to allow port 8501

4. **For VPS:** Ensure security group allows inbound on port 8501

---

## Production Checklist

- [ ] Bot logs are rotating (prevent huge files)
- [ ] Dashboard has error handling (✅ DONE)
- [ ] Auto-restart on crash (✅ systemd or Task Scheduler)
- [ ] Mobile access configured
- [ ] Backup of bot_state.json before trading real money
- [ ] Monitor trade history daily
- [ ] Check logs for errors

---

## Quick Commands Reference

**Windows:**
```batch
# Start bot
START_BOT.bat

# Start dashboard
START_DASHBOARD.bat
```

**Linux/VPS:**
```bash
# Start bot in background
nohup python bot.py &

# Start dashboard
streamlit run dashboard.py --server.port 8501 &

# View logs
tail -f bot_log.txt

# Stop bot (find PID first: ps aux | grep bot.py)
kill <PID>
```

---

## Next Steps

1. **Test on demo mode first** ✅ (You're already here!)
2. Run for 24-48 hours, observe patterns
3. Check trading performance
4. Analyze PnL, entry quality, strategy fit
5. Only then: Switch to real trading (if desired)

---

## Support

For issues:
1. Check `bot_log.txt` for error messages
2. Verify settings.json configuration
3. Review bot_state.json for position status
4. Check actions.csv for trade history

**Bot is self-healing:** Most errors are caught and logged, bot continues running.

---

**Last Updated:** May 19, 2026

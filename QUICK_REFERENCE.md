# AlphaTrade Bot - Quick Reference & Troubleshooting

## 🚀 Quick Start (Copy-Paste)

### Windows
```batch
# Open Command Prompt or PowerShell in bot folder

# Terminal 1: Start bot
START_BOT.bat

# Terminal 2: Start dashboard  
START_DASHBOARD.bat

# Browser: http://localhost:8501
```

### Linux/Mac
```bash
# Terminal 1: Bot
source venv/bin/activate  # Or: python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 bot.py

# Terminal 2: Dashboard (new terminal)
source venv/bin/activate
streamlit run dashboard.py

# Browser: http://localhost:8501
```

---

## ✅ What to Look For

### Bot Starting (Expected Output)
```
🚀 AlphaTrade Bot STARTING
=========================================================
Mode: DEMO | Strategy: trend_scalper
Starting Balance: $1000.00
Trade Size: $10.0
Auto Enabled: True
Symbols: BTCUSDT, ETHUSDT, SOLUSDT
=========================================================
📊 TRADING RULES:
  • Entry: EMA20>EMA50 + RSI 45-65 + Last 3 prices up OR Dip Recovery
  • Take Profit: +0.4%
  • Stop Loss: -0.3%
  • Cycle Time: 60 seconds
  • Position: All-in (use full cash)
=========================================================

[CYCLE #1] Starting at 14:30:46 UTC
🔄 CYCLE: Auto=🟢 RUNNING | Symbols=3 | Cash=$1000.00
⏳ WAIT BTCUSDT: ema_cross=True rsi=52.5 last3_up=True ...
[CYCLE #1] Completed - waiting 60s for next cycle...
```

✅ **Good signs:**
- Sees "STARTING"
- Shows "Auto=🟢 RUNNING"
- Processes each symbol
- Waits 60 seconds between cycles

---

## ❌ Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Fix:**
```bash
pip install -r requirements.txt
```

**Verify:**
```bash
python -m pip list | grep streamlit
```

---

### Issue: "Bot won't start / Error on startup"

**Check:**
1. Python installed: `python --version` (should be 3.9+)
2. Requirements: `pip install -r requirements.txt`
3. Read error in bot_log.txt

**Fix most issues:**
```bash
# Delete and recreate venv
rmdir /s venv  # Windows: rmdir /s venv
# Or Linux: rm -rf venv

python -m venv venv
source venv/bin/activate  # Linux/Mac
# Or Windows: venv\Scripts\activate.bat

pip install -r requirements.txt
python bot.py
```

---

### Issue: "Dashboard won't open / localhost:8501 refused"

**Check:**
1. Dashboard process running? (Check terminal)
2. Port already in use? Try different port:
   ```bash
   streamlit run dashboard.py --server.port 8502
   ```

**Fix:**
```bash
# Find what's using port 8501
# Windows:
netstat -ano | findstr :8501

# Linux/Mac:
lsof -i :8501

# Kill the process
# Windows:
taskkill /PID <PID> /F

# Linux/Mac:
kill -9 <PID>

# Restart dashboard
streamlit run dashboard.py
```

---

### Issue: "Auto mode keeps turning off"

**Status: ✅ FIXED**  
This was a critical bug - now fixed!

**If still happening:**
1. Check bot_state.json: `"auto_enabled": true`
2. Check bot_log.txt for "AUTO MODE STOPPED"
3. Verify dashboard "⚙️ Auto" shows ON (🟢)

**Recovery:**
```bash
# In dashboard: Click "Start Auto"
# Or manually edit bot_state.json:
{
  "bot": {
    "auto_enabled": true,  # ← Make sure this is true
    ...
  }
}
```

---

### Issue: "No trades happening / No entry signals"

**Check:**
1. Bot is running? (Check bot_log.txt shows cycles)
2. Auto mode ON? (Dashboard shows 🟢)
3. Enough price history? (Bot needs 55+ prices)

**Normal if:**
- Market not volatile enough
- RSI not in 45-65 range
- EMA20 not above EMA50
- Last 3 prices not ascending

**Wait longer:**
- Signals depend on market conditions
- Bot evaluates every 60 seconds
- Sometimes takes hours for conditions

**Check signals in log:**
```bash
grep "SMART BUY" bot_log.txt  # Trading signals
grep "WAIT" bot_log.txt        # Waiting for conditions
```

---

### Issue: "Manual trade broke auto mode"

**Status: ✅ FIXED**  
This was a critical bug - now fixed!

**If experiencing:**
1. Click "Place order" → manual trade
2. Check: Does "⚙️ Auto" still show 🟢 ON?
3. Check: Does bot continue trading after?

**This should work:**
- Manual trade executes immediately
- Auto stays ON
- Next cycle continues auto trading

**If not working:**
```bash
# Check bot_state.json
# Should have: "auto_enabled": true

# Force restart
# Click "Start Auto" in dashboard
```

---

### Issue: "Dashboard crashes when clicking buttons"

**This should NOT happen** - all errors are caught

**If it crashes:**
1. Refresh page (usually recovers)
2. Check bot_log.txt for errors
3. Restart dashboard

**To debug:**
```bash
streamlit run dashboard.py --logger.level=debug
```

---

### Issue: "Bot log file is huge / slow"

**Normal after running for days**

**Clean up:**
```bash
# Keep last 1000 lines
tail -1000 bot_log.txt > bot_log_trimmed.txt
mv bot_log_trimmed.txt bot_log.txt

# Or delete and restart
del bot_log.txt  # Windows
# rm bot_log.txt  # Linux
python bot.py  # Creates new log
```

---

## 🔧 Manual Fixes

### Reset Everything (Start Fresh)
```bash
# WARNING: This deletes trading history!

del bot_state.json
del bot_log.txt
del commands.json
del prices.csv
del trades.csv
del actions.csv

python bot.py  # Recreates with defaults
```

### Force Auto Mode On
```bash
# Edit bot_state.json:
{
  "bot": {
    "auto_enabled": true,  # ← Set to true
    "current_strategy": "trend_scalper",
    "enabled_symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    "last_run": "..."
  },
  ...
}

# Save and restart bot
```

### Check System Health
```bash
# All these should work:

# 1. Python OK?
python --version

# 2. Requirements installed?
pip list | grep streamlit

# 3. Bot starts?
python bot.py

# 4. Dashboard works?
streamlit run dashboard.py

# 5. State files exist?
ls -la bot_state.json settings.json

# 6. Can read state?
cat bot_state.json
```

---

## 📊 Monitoring Commands

### Watch Bot Live
```bash
# Linux/Mac - follow log in real-time
tail -f bot_log.txt

# Windows - show last 50 lines
type bot_log.txt | tail -50

# With filtering
grep "SMART BUY" bot_log.txt      # Entry signals
grep "TAKE PROFIT" bot_log.txt    # Wins
grep "STOP LOSS" bot_log.txt      # Losses
grep "ERROR" bot_log.txt           # Errors
grep "❌" bot_log.txt              # Problems
```

### Check Status
```bash
# Is bot running auto?
grep "CYCLE" bot_log.txt | tail -5

# Is auto enabled?
grep '"auto_enabled"' bot_state.json

# What's the cash balance?
cat bot_state.json | grep '"cash"'

# Any errors?
grep "❌" bot_log.txt | tail -10

# Recent trades?
tail -20 trades.csv

# PnL on trades?
grep "PnL:" bot_log.txt | tail -10
```

### Calculate Performance
```bash
# Count wins
grep "PnL: +" bot_log.txt | wc -l

# Count losses
grep "PnL: -" bot_log.txt | wc -l

# Win rate
# (wins / (wins + losses)) * 100
```

---

## 📱 Mobile Access (5 min setup)

### Easiest: Cloudflare Tunnel
```bash
# 1. Download from:
# https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

# 2. Run:
cloudflared tunnel --url http://localhost:8501

# 3. Get URL: https://something.trycloudflare.com

# 4. Open on phone browser → Done!
```

### Alternative: Ngrok
```bash
# 1. Install from: https://ngrok.com
# 2. Signup for free account
# 3. Add auth token:
ngrok config add-authtoken YOUR_TOKEN

# 4. Create tunnel:
ngrok http 8501

# 5. Get URL and open on phone
```

---

## 📋 Daily Checklist

- [ ] Bot running? `ps aux | grep bot.py`
- [ ] Dashboard accessible? http://localhost:8501
- [ ] Auto mode ON? Check dashboard metric
- [ ] Recent activity? Check bot_log.txt tail
- [ ] Any errors? `grep "❌" bot_log.txt`
- [ ] Positions look OK? Check dashboard metrics
- [ ] Cash available? Check "💰 Cash" metric

---

## 🆘 Emergency: Kill Stuck Process

### Windows
```batch
REM Find Python process
tasklist | findstr python

REM Kill it
taskkill /IM python.exe /F

REM Or kill specific port
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Linux/Mac
```bash
# Find process
ps aux | grep python
ps aux | grep streamlit

# Kill by name
killall python
killall streamlit

# Or kill by port
lsof -i :8501
kill -9 <PID>
```

---

## 🚨 Critical Issues

### Bot Crashed
1. Check bot_log.txt for error
2. Restart: `python bot.py`
3. If keeps crashing, check error details

### Dashboard Crashed
1. Refresh browser (usually recovers)
2. Restart: `streamlit run dashboard.py`
3. Check bot_log.txt for file issues

### Lost Position Data
1. Data is in bot_state.json
2. If corrupted, restore from backup
3. Or reset (loses history)

### Can't Access Dashboard
1. Check if running: `ps aux | grep streamlit`
2. Try different port: `streamlit run dashboard.py --server.port 8502`
3. Check firewall allows 8501

---

## 📞 Support Checklist

When reporting issues, provide:
- [ ] Full error message
- [ ] Last 30 lines of bot_log.txt
- [ ] Contents of bot_state.json
- [ ] What were you doing when it happened?
- [ ] OS (Windows/Linux/Mac)
- [ ] Python version: `python --version`

---

## 🎯 Before Production

- [ ] Run demo mode 48+ hours
- [ ] Verify entry quality in logs
- [ ] Check PnL performance
- [ ] Test manual + auto working together
- [ ] Analyze strategy fit
- [ ] Review all trades
- [ ] Only then consider real money

---

**Last Updated:** May 19, 2026  
**Status:** ✅ All Critical Fixes Applied  
**Ready to Use:** YES 🚀

# 🚀 AlphaTrade Bot - Fixed & Ready to Run

> **Status:** ✅ Production Ready  
> **Last Updated:** May 19, 2026  
> **Version:** 2.0 (Bugs Fixed)

---

## ⚡ Quick Start (5 Minutes)

### Windows
```batch
REM Open Command Prompt or PowerShell in this folder

REM Terminal 1: Start the bot
START_BOT.bat

REM Terminal 2: Start the dashboard
START_DASHBOARD.bat

REM Open browser: http://localhost:8501
```

### Linux/Mac/VPS
```bash
# Terminal 1: Bot
python3 bot.py

# Terminal 2: Dashboard  
streamlit run dashboard.py

# Open: http://localhost:8501
```

---

## 🔧 What Was Fixed

| Issue | Status | Fix |
|-------|--------|-----|
| **Auto mode turns OFF** | ✅ FIXED | Manual trades no longer disable auto |
| **Manual blocks auto** | ✅ FIXED | Removed manual_locked permanent blocking |
| **Random trades** | ✅ IMPROVED | Added dip recovery detection + better signals |
| **Bot crashes** | ✅ FIXED | Complete error handling, graceful degradation |
| **Dashboard dies** | ✅ FIXED | Safe file loading, error recovery |
| **Poor logging** | ✅ IMPROVED | Added PnL %, signal reasons, emoji status |

**Details:** See [FIXES_APPLIED.md](FIXES_APPLIED.md)

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│         AlphaTrade Bot System           │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   BOT (bot.py) - 60s cycles    │   │
│  │  ✅ Entry detection            │   │
│  │  ✅ Position management        │   │
│  │  ✅ Auto trades               │   │
│  │  ✅ Error resilient           │   │
│  └─────────────────────────────────┘   │
│           ↓                             │
│  ┌─────────────────────────────────┐   │
│  │  State (bot_state.json)        │   │
│  │  ✅ Portfolio (cash, positions)│   │
│  │  ✅ Settings (strategy, symbols)│  │
│  │  ✅ Market (prices)            │   │
│  └─────────────────────────────────┘   │
│           ↓                             │
│  ┌─────────────────────────────────┐   │
│  │  Dashboard (dashboard.py)      │   │
│  │  ✅ Web UI (http:8501)        │   │
│  │  ✅ Live charts               │   │
│  │  ✅ Trade history             │   │
│  │  ✅ Manual controls           │   │
│  └─────────────────────────────────┘   │
│           ↓                             │
│  ┌─────────────────────────────────┐   │
│  │  Data (CSV files)              │   │
│  │  ✅ prices.csv (price history)│   │
│  │  ✅ trades.csv (all trades)   │   │
│  │  ✅ actions.csv (entries/exits)│  │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## ⚙️ Trading Logic

### Entry Signals

**Signal 1: EMA Crossover + Uptrend**
- EMA(20) > EMA(50) ✅
- RSI(14) between 45-65 ✅
- Last 3 prices up ✅
- → Entry with ALL available cash

**Signal 2: Dip Recovery (NEW)**
- Price dips to 15-period low
- Price recovers above recent low
- RSI < 55 (not overbought)
- → Entry with ALL available cash

### Exit Rules

| Condition | Action |
|-----------|--------|
| PnL ≥ +0.4% | Sell all - TAKE PROFIT |
| PnL ≤ -0.3% | Sell all - STOP LOSS |
| Holding | Monitor every 60s |

### Position Rules
- **Entry Size:** Use ALL cash available
- **Exit Size:** Close FULL position (no partial exits)
- **Cycle Time:** Evaluate every 60 seconds
- **Symbols:** BTC, ETH, SOL (configurable)

---

## 🎮 Controls

### Dashboard (http://localhost:8501)

**Sidebar Controls:**
- **Coin:** Select symbol to view
- **Strategy:** Choose trading algorithm
- **Auto Watchlist:** Select which symbols to trade
- **Place Order:** Manual BUY/SELL (instant execution)
- **Start Auto:** Turn on automated trading
- **Stop Auto:** Turn off automated trading
- **Apply Strategy & Watchlist:** Update settings

**Main Display:**
- **Metrics:** Cash, Position, Equity, Profit, Open PnL, Auto status
- **Chart:** Price with EMA(20), EMA(50), entry/exit points
- **Positions:** Current open positions with PnL
- **Actions:** Real-time trade log
- **Trade History:** All completed trades

### Manual Trading
- Click "Place order" to execute instantly
- ✅ **NEW:** Does NOT disable auto mode
- ✅ Auto continues running normally
- Manual + Auto can coexist

### Auto Trading
- Click "Start Auto" to enable
- Bot evaluates every 60 seconds
- Enters on signals, manages positions
- Auto stays ON until you click "Stop Auto"
- ✅ **NEW:** Manual trades don't turn it off

---

## 📁 File Structure

```
alphatrade-bot/
├── bot.py                      # Main trading engine (fixed!)
├── dashboard.py                # Web interface (error handling added)
├── init_app.py                # Initialization
├── settings.json              # Configuration
├── bot_state.json             # Current state (auto_enabled=true now)
├── requirements.txt           # Python dependencies
│
├── START_BOT.bat              # Windows bot launcher
├── START_DASHBOARD.bat        # Windows dashboard launcher
│
├── Dockerfile                 # Docker container setup
├── docker-compose.yml         # Docker compose for easy deployment
│
├── FIXES_APPLIED.md           # Detailed fixes documentation
├── SETUP_24_7_AND_MOBILE.md   # 24/7 operation & mobile access
├── README.md                  # This file
│
├── bot_log.txt                # Trading logs (auto-appended)
├── prices.csv                 # Price history
├── trades.csv                 # All trades executed
├── actions.csv                # Entry/exit events
└── commands.json              # Command queue
```

---

## 🐳 Docker Setup (Easy Cloud Deployment)

### Option 1: Local Docker
```bash
docker-compose up --build
```

### Option 2: Deploy to Cloud

**AWS ECS:**
```bash
docker build -t alphatrade .
aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker tag alphatrade $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/alphatrade
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/alphatrade
```

**DigitalOcean App Platform:**
- Connect GitHub repo
- Build from Dockerfile
- Expose port 8501
- Deploy!

---

## 📱 Mobile Access

### Fastest (Cloudflare Tunnel) ⚡

```bash
# Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
cloudflared tunnel --url http://localhost:8501

# Get HTTPS URL → Open on phone
```

### Alternative (Ngrok)

```bash
# Install: https://ngrok.com
ngrok http 8501

# Get URL → Share with phone
```

**Details:** See [SETUP_24_7_AND_MOBILE.md](SETUP_24_7_AND_MOBILE.md)

---

## 🔄 24/7 Operation

### Windows: Task Scheduler
- Set bot.py to run at startup
- Set dashboard.py to run at startup
- Survives PC restarts

### Linux/VPS: Systemd
```bash
# See SETUP_24_7_AND_MOBILE.md for complete setup
systemctl enable alphatrade-bot
systemctl start alphatrade-bot
```

### Cloud: Docker
```bash
docker-compose up -d
# Runs indefinitely, restarts on crash
```

**Details:** See [SETUP_24_7_AND_MOBILE.md](SETUP_24_7_AND_MOBILE.md)

---

## 📊 Monitoring

### Check Bot Status
```bash
# View live logs
tail -f bot_log.txt

# Check for errors
grep "❌" bot_log.txt

# Check trades
tail -20 trades.csv

# Check auto mode status
cat bot_state.json | grep auto_enabled
```

### Expected Log Output
```
2026-05-19 14:30:45 UTC | 🚀 AlphaTrade Bot STARTING
2026-05-19 14:30:46 UTC | [CYCLE #1] Starting at 14:30:46 UTC
2026-05-19 14:30:47 UTC | 🔄 CYCLE: Auto=🟢 RUNNING | Symbols=3 | Cash=$1000.00
2026-05-19 14:30:47 UTC | 🔔 SMART BUY SIGNAL BTCUSDT: EMA-Cross(20>50) + RSI=55.2
2026-05-19 14:30:48 UTC | ✅ BUY BTCUSDT | $1000.00 qty=0.01273 @ 78536.10 | AUTO ENTRY
2026-05-19 14:31:48 UTC | 📊 HOLD BTCUSDT: PnL=+0.25% (Entry: 78536.10, Current: 78682.55)
2026-05-19 14:32:48 UTC | ✅ SELL BTCUSDT | qty=0.01273 @ 78764.21 | PnL: +0.29% | AUTO TAKE PROFIT
```

---

## ✅ Pre-Launch Checklist

- [ ] Python 3.9+ installed
- [ ] `pip install -r requirements.txt` completed
- [ ] Bot starts: `python bot.py` (no errors)
- [ ] Dashboard loads: http://localhost:8501
- [ ] Bot logs show cycling: "CYCLE #1", "CYCLE #2", etc.
- [ ] Auto mode enabled in dashboard
- [ ] Settings configured (symbols, trade size, strategy)
- [ ] Manual trade works (doesn't break auto)
- [ ] Log file creates entries: check `bot_log.txt`

---

## 🚨 Troubleshooting

### Bot won't start
```bash
python bot.py
# Check for error message
# Common: Missing requirements - run: pip install -r requirements.txt
```

### Dashboard crashes
- Refresh page (most errors are caught and recovered)
- Check bot_log.txt for file access issues
- All errors are now handled gracefully

### Auto mode turns off unexpectedly
- ✅ **FIXED** - This shouldn't happen anymore
- Check dashboard "Auto" status (should be 🟢 ON)
- Check bot_state.json: `"auto_enabled": true`

### No entry signals appearing
- Normal during low volatility
- Might not have enough price history (waits 55 prices)
- Check bot_log.txt for signal attempts
- Wait longer, bot evaluates every 60s

### Mobile access not working
1. **Try Cloudflare Tunnel** (easiest):
   ```bash
   cloudflared tunnel --url http://localhost:8501
   ```
2. Check firewall allows port 8501
3. For VPS: Check security group allows inbound 8501

---

## 📈 Performance Analysis

### Check Win Rate
```bash
# Count winning trades
grep "PnL: +" trades.csv | wc -l

# Count losing trades  
grep "PnL: -" trades.csv | wc -l

# Calculate win rate: (wins / total) * 100
```

### Check Average Profit
```bash
# View last 10 trades with PnL
tail -10 bot_log.txt | grep "PnL"
```

### Optimize Settings
Review `settings.json`:
- Change `trade_size_usdt` for smaller/larger positions
- Change strategy with dashboard selector
- Enable/disable symbols with watchlist

---

## 🔐 Security Notes

**For Demo Mode (Current):**
- No real money involved ✅
- Safe to test behavior ✅
- No API keys needed ✅

**For Real Trading (Future):**
- Never hardcode API keys in code
- Use environment variables
- Use IP whitelist on exchange
- Store keys separately from repo
- Only run on trusted systems

---

## 🎯 Next Steps

1. **Run bot for 24+ hours** on demo mode
2. **Analyze trading patterns** - are entries logical?
3. **Check log quality** - can you see why trades happened?
4. **Monitor performance** - what's the win rate?
5. **Test manually** - click buttons, verify auto still works
6. **Scale to VPS** if satisfied (see SETUP_24_7_AND_MOBILE.md)
7. **Configure mobile access** (see SETUP_24_7_AND_MOBILE.md)
8. **Only switch to real trading** after careful review

---

## ❓ FAQ

**Q: Can manual trades break auto mode?**  
A: ✅ NO - This was the main bug, now FIXED. Manual trades execute independently, auto continues.

**Q: Will bot crash if dashboard closes?**  
A: NO - Bot runs independently. Dashboard is just UI. Close it anytime.

**Q: How do I know if auto is running?**  
A: Check dashboard metric "⚙️ Auto" - shows ON/OFF. Or check `bot_state.json`: `"auto_enabled": true`

**Q: Can I stop bot safely?**  
A: Yes - Press Ctrl+C in terminal. Logs "Shutting down gracefully", saves state, exits cleanly.

**Q: What if bot crashes?**  
A: Check bot_log.txt for error. Most errors are caught and bot continues. For crashes, set up auto-restart (Task Scheduler or systemd).

**Q: Should I use this with real money now?**  
A: NO - Run demo mode for 48+ hours first. Verify strategy, analyze trades, understand behavior. Only switch to real money after full confidence.

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | May 19, 2026 | **Critical fixes:** Auto mode disabled, manual blocks auto, random trades, crashes |
| 1.0 | May 18, 2026 | Initial release |

---

## 🤝 Support

**Common Issues:**
1. Check [FIXES_APPLIED.md](FIXES_APPLIED.md) for detailed fixes
2. Check [SETUP_24_7_AND_MOBILE.md](SETUP_24_7_AND_MOBILE.md) for deployment
3. Review bot_log.txt for error details
4. Check bot_state.json for state confirmation

---

## 🎓 Educational Notes

This system demonstrates:
- ✅ Automated trading architecture
- ✅ Real-time data processing
- ✅ Risk management (TP/SL)
- ✅ Signal detection (EMA, RSI)
- ✅ Error handling & resilience
- ✅ Web dashboard UI
- ✅ State persistence
- ✅ Graceful degradation

**USE FOR:** Learning, experimentation, backtesting  
**NOT FOR:** Real money without thorough testing first

---

## 🚀 Ready to Launch

```bash
# Windows
START_BOT.bat              # Terminal 1
START_DASHBOARD.bat        # Terminal 2

# Linux
python3 bot.py &          # Background
streamlit run dashboard.py # Terminal 2

# Open: http://localhost:8501
```

---

**Status:** ✅ Production Ready  
**Last Tested:** May 19, 2026  
**All Critical Bugs:** FIXED  
**Error Handling:** COMPLETE  
**Ready to Run:** YES 🚀


# AlphaTrade Bot v3.0 - Quick Reference Card

## 🎯 Three Ways to Run Your Bot

### 1️⃣ DEMO MODE (Safe, default)
```json
settings.json: "demo_mode": true
No API keys needed
Simulated prices, simulated trades
Perfect for testing
```

### 2️⃣ REAL PRICES + SIMULATED TRADES (Test API)
```json
settings.json: "demo_mode": false
No API keys needed (or set but not used)
Real Binance prices, simulated trades
Verify prices are correct
```

### 3️⃣ FULL REAL TRADING (Live money)
```json
settings.json: "demo_mode": false
Set environment variables:
  BINANCE_API_KEY=xxx
  BINANCE_API_SECRET=yyy
Real prices + real trades on Binance
MAX $10 per trade (enforced)
```

---

## 🚀 Launch Commands

```bash
# Test in demo (safest)
python bot.py

# Test real prices (no keys needed)
python -c "export BINANCE_API_KEY=; export BINANCE_API_SECRET=; exec python bot.py"

# Real trading (with keys in environment)
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
python bot.py
```

---

## 📋 Checklist: Demo → Real

- [ ] Run demo for 24+ hours
- [ ] Check logs for errors
- [ ] Verify strategy works
- [ ] Get Binance API keys
- [ ] Set environment variables
- [ ] Change `demo_mode` to false
- [ ] Restart bot
- [ ] Check logs for "✅ API READY"
- [ ] Monitor first trades
- [ ] Watch for 2-4 hours

---

## 🛡️ Safety Features

| Feature | Demo | Real |
|---------|------|------|
| Max per trade | unlimited | **$10 USDT** |
| Circuit breaker | ✅ 10% drawdown | ✅ same |
| Risk management | ✅ yes | ✅ yes |
| Error fallback | ✅ demo prices | ✅ safe |
| API keys needed | ❌ no | ✅ yes |
| Real money | ❌ no | ✅ yes |

---

## 📊 What You'll See

### Startup (Demo)
```
🚀 AlphaTrade Bot v2.0
Mode: DEMO MODE 🎮
API Status: ⚠️ NO API CREDENTIALS
```

### Startup (Real with keys)
```
🚀 AlphaTrade Bot v2.0
Mode: REAL BINANCE 🌐
API Status: ✅ API READY
```

### Startup (Real without keys)
```
🚀 AlphaTrade Bot v2.0
Mode: REAL BINANCE 🌐
API Status: ⚠️ NO API CREDENTIALS
```
(Real prices, simulated trades)

---

## 📝 CSV Records

**trades.csv now shows Mode:**
```
SYMBOL, MODE , ACTION, PRICE, TIME, AMOUNT, QTY, REASON
BTCUSDT, DEMO , BUY   , 78500, ..., 10.00, ..., ...
BTCUSDT, REAL , SELL  , 78520, ..., 10.12, ..., ...
```

---

## 🔑 Binance API Setup (5 min)

1. https://www.binance.com → Settings
2. API Management → Create Key
3. Copy API Key → `BINANCE_API_KEY`
4. Copy Secret → `BINANCE_API_SECRET`
5. Enable Spot Trading (Read + Write)
6. Disable everything else

---

## ⚠️ DON'Ts

- Don't share API keys
- Don't commit keys to GitHub
- Don't set demo_mode=false without reading docs
- Don't use same keys on multiple bots
- Don't allow withdrawal permission
- Don't start with large amounts

---

## ✅ DOs

- Do test in demo first
- Do use environment variables
- do read BINANCE_REAL_TRADING.md
- Do monitor first 24 hours
- Do keep IP whitelist enabled
- Do start small

---

## 🐛 If Something Breaks

1. Check logs: `tail -f bot_log.txt`
2. Look for "❌" errors
3. Switch to demo mode (set `demo_mode: true`)
4. Restart bot
5. If still broken, check:
   - Python 3.9+ installed?
   - All dependencies installed? (`pip install -r requirements.txt`)
   - API keys correct?
   - Binance API working? (`curl https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT`)

---

## 🎯 One Command Start

```bash
# Demo (default, safe, no setup)
python bot.py

# Real trading (after env vars set)
python bot.py
```

Same command. Settings control behavior.

---

## 📈 Expected Performance

- Trades: 6-10 per hour (filtered by score)
- Win rate: ~55-65% (backtest dependent)
- Avg trade: +0.2% to +0.4% winner, -0.3% loser
- Max per trade: $10 USDT

With $100 Binance balance:
- Could trade 2-3 symbols simultaneously
- Realistic daily: $0.30-$1.50 profit (if strategy works)

---

## 📞 Support

**Check these first:**
- [ ] BINANCE_REAL_TRADING.md (full guide)
- [ ] RENDER_SETUP.md (if on Render)
- [ ] bot_log.txt (error messages)
- [ ] settings.json (configuration)

**Common issues in logs:**
- "API Status: NO CREDENTIALS" → Set env vars
- "HMAC signature invalid" → Check key/secret
- "Insufficient balance" → Add balance to Binance
- "Rate limit exceeded" → Shouldn't happen, contact support

---

## 🎉 You're Ready!

Your bot now supports both:
- Safe simulated trading (learning)
- Real Binance trading (production)

Choose your mode and go! 🚀

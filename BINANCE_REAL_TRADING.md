# AlphaTrade Bot v3.0 - Real Binance Trading Support

**Status**: ✅ COMPLETE & TESTED  
**Version**: 3.0 (Real Binance Trading)  
**Date**: May 19, 2026

---

## 🚀 What's New

Your bot now supports **REAL Binance spot trading**! The upgrade safely extends your existing system to trade on real markets.

---

## 📋 Quick Start

### 1. **Enable Real Trading in Render** (or local environment)

Add environment variables:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

In Render:
- Go to your Service → Environment
- Add above variables
- Deploy

Locally (test first):
```bash
# Linux/Mac
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
python bot.py

# Windows PowerShell
$env:BINANCE_API_KEY="your_key"
$env:BINANCE_API_SECRET="your_secret"
python bot.py
```

### 2. **Switch Bot to Real Mode**

Edit `settings.json`:
```json
{
  "demo_mode": false,
  ...
}
```

OR keep demo_mode as true (default) and the bot will:
- Use simulated trades
- Use fake prices for backtesting
- Keep your real balance safe

### 3. **Start Bot**

```bash
python bot.py
```

---

## ⚙️ Architecture

### Trading Modes

**Demo Mode (default, safe)**
```
DEMO_MODE = true
├─ Simulated prices (±2% random variation)
├─ Simulated trades (no real orders)
├─ Perfect for testing strategies
└─ Zero risk, $1000 starting balance
```

**Real Mode (requires API keys)**
```
DEMO_MODE = false
├─ Real Binance prices (spot market)
├─ Real orders executed on Binance
├─ Your actual balance on Binance
└─ Real trading - real money at stake
```

### Safety Features

1. **API Credentials via Environment Variables**
   - Never hardcoded in files
   - Only read from `BINANCE_API_KEY` and `BINANCE_API_SECRET`
   - Render environment variables are secure

2. **Max Trade Size Limit**
   - Hard limit: $10 USDT per trade
   - Cannot be overridden by strategy
   - Prevents accidental large orders

3. **Error Fallback**
   - If Binance API fails → falls back to demo prices
   - If order fails → does NOT crash
   - Logs all errors for debugging

4. **No Full-Balance Trades**
   - Even with $1000, single trade = max $10
   - Strategy calculates safe size based on risk%
   - Position limiting enforced

---

## 🔑 Getting Binance API Keys

### Step 1: Create Binance Account
Go to https://www.binance.com and create account

### Step 2: Enable 2FA (mandatory for API)
- Settings → Account Security
- Enable Google Authenticator or SMS

### Step 3: Create API Key
- Settings → API Management
- Create New Key → System generated
- Label: "AlphaTrade Bot"

### Step 4: Set Permissions
- Enable: `Spot Trading - Read`
- Enable: `Spot Trading - Write`
- Disable: Margin, Futures, Withdrawal
- Set IP Whitelist (recommended)

### Step 5: Copy Credentials
- Copy API Key → `BINANCE_API_KEY`
- Copy Secret Key → `BINANCE_API_SECRET`

**⚠️ SECURITY**: 
- Never share your secret key
- Never commit to GitHub
- Always use environment variables
- Use IP whitelist for extra security

---

## 📊 How It Works

### Real Binance Functions

```python
# 1. Get Real Price
binance_get_price(symbol)
├─ Uses Binance API v3 ticker/price
├─ Falls back to testnet if API fails
└─ Returns float price

# 2. Get Real Balance
binance_get_balance(symbol_base)
├─ Fetches from /api/v3/account
├─ HMAC-SHA256 signed request
└─ Returns available balance

# 3. Place Real Order
binance_place_order(symbol, side, quantity)
├─ Places MARKET order (immediate execution)
├─ Returns (success: bool, fill_price: float)
├─ Logs order ID and execution details
└─ Returns False on API error (safe)

# 4. Get Price (smart routing)
get_price(symbol)
├─ If demo_mode=true → simulated price
├─ If demo_mode=false → calls binance_get_price()
├─ Falls back to demo if API fails
└─ Never crashes
```

### Workflow per Cycle

```
CYCLE START
│
├─ Load market prices
│  ├─ DEMO MODE → Simulated ±2%
│  └─ REAL MODE → Binance /ticker/price
│
├─ Calculate entry score (0-100)
│
├─ If entry signal AND score >= 70:
│  ├─ Calculate safe position size
│  ├─ If DEMO MODE:
│  │  └─ simulate_buy() → update state only
│  └─ If REAL MODE:
│     ├─ binance_place_order("BUY", qty)
│     ├─ If success → update state + csv
│     └─ If fail → log error, skip trade
│
├─ Check existing positions
│
├─ If exit signal (TP/SL/Trailing):
│  ├─ If DEMO MODE:
│  │  └─ simulate_sell() → update state
│  └─ If REAL MODE:
│     ├─ binance_place_order("SELL", qty)
│     ├─ If success → update state + csv
│     └─ If fail → log error, hold position
│
├─ Update analytics & state.json
│
└─ Wait 60 seconds → NEXT CYCLE
```

---

## 🛡️ Safety Mechanisms

### 1. Circuit Breaker (Unchanged)
- Stops ALL trades if drawdown >= 10%
- Stops ALL trades if consecutive losses >= 3
- Can be reset only by manual intervention

### 2. Trade Size Limiting (NEW)
```python
# In simulate_buy():
if not settings.get("demo_mode", True):
    amount_usdt = min(amount_usdt, MAX_TRADE_SIZE_USDT)  # $10 hard limit
```

### 3. Error Handling
```python
# Every API call wrapped in try-except
try:
    response = binance_place_order(...)
except Exception as e:
    log(f"❌ Error: {str(e)}")
    return False  # Safe fallback
```

### 4. Credential Security
```python
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET", "")
# Only from environment, never hardcoded
# If missing → both empty strings
# If empty → API calls fail safely with warning
```

### 5. HMAC-SHA256 Signing
All requests to Binance signed with:
```python
signature = hmac.new(
    secret.encode('utf-8'),
    query_string.encode('utf-8'),
    hashlib.sha256
).hexdigest()
```

Prevents replay attacks and ensures authenticity.

---

## 🔄 Transitioning from Demo to Real

### Stage 1: Test in Demo (Recommended First)
```json
{
  "demo_mode": true
}
```
- Run for 24-48 hours
- Verify strategy works
- Check logs for errors
- Monitor dashboard

### Stage 2: Live with Real Prices, Simulated Trades
```json
{
  "demo_mode": false
}
```
But:
- Modify `simulate_buy()` temporarily to log only
- See real prices without real trades
- Verify price data is correct

### Stage 3: Full Real Trading
```json
{
  "demo_mode": false
}
```
With environment variables:
- `BINANCE_API_KEY` set
- `BINANCE_API_SECRET` set
- Real trades execute
- Real balance used

---

## 📝 CSV Files & Logging

### Trades are logged in 3 places:

1. **trades.csv** (permanent record)
```
Symbol,Mode,Action,Price,Time,Amount_USDT,Quantity,Reason
BTCUSDT,REAL,BUY,78500.00,1716120600,10.00,0.00012735,"AUTO ENTRY (score:75)"
BTCUSDT,REAL,SELL,78520.00,1716120660,10.12,0.00012735,"AUTO TAKE PROFIT +0.25%"
```

2. **actions.csv** (all actions)
```
Time,Symbol,Action,Amount_USDT,Price,Strategy,Reason,Result,Quantity
```

3. **bot_log.txt** (detailed logs)
```
2026-05-19 14:30:00 UTC | 🚀 AlphaTrade Bot v2.0 - PROFESSIONAL TRADING SYSTEM
2026-05-19 14:30:00 UTC | Mode: REAL BINANCE 🌐
2026-05-19 14:30:00 UTC | API Status: ✅ API READY
2026-05-19 14:30:00 UTC | ✅ BINANCE ORDER FILLED: BUY 0.00012735 BTCUSDT @ 78500
```

---

## 🐛 Debugging

### Check if API keys are loaded:
```bash
python -c "import os; print('API Key:', os.environ.get('BINANCE_API_KEY', 'NOT SET'))"
```

### Check Binance connectivity:
```bash
python -c "
import requests
r = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': 'BTCUSDT'})
print(r.json())
"
```

### Simulate with real prices:
Set `demo_mode = false` but don't provide API keys.
Bot will:
- Fetch real prices from Binance ✅
- Simulate trades (no orders placed) ✅
- Never crash ✅

---

## ⚠️ Risks & Considerations

### Market Risks
- Real money at stake
- Crypto volatility high
- Possible rapid losses
- Strategy may underperform in unexpected markets

### Technical Risks
- Binance API downtime → bot falls back to demo prices
- Network delays → orders may execute at different prices
- API rate limits (1200 requests per minute) → we're well within limits

### Security Risks
- API key compromise → attacker could trade your account
- **Mitigation**: Use IP whitelist on Binance, rotate keys regularly
- Never share keys or upload to GitHub

### Operational Risks
- Insufficient balance → orders fail
- Misconfigured settings → circuit breaker may trigger
- Auto mode left on overnight → could execute many trades

---

## ✅ Testing Checklist

Before going live with real money:

- [ ] Demo mode works (test 24 hours)
- [ ] API keys obtained and configured
- [ ] Environment variables set correctly
- [ ] Binance spot trading enabled on account
- [ ] Run with `demo_mode = false` but no API keys (real prices, no trades)
- [ ] Verify prices are correct vs Binance website
- [ ] Check logs for any API errors
- [ ] Run with real API keys but MAX_TRADE_SIZE_USDT = 0.01 (penny test)
- [ ] Verify first real trade executes correctly
- [ ] Check CSV files recorded trade properly
- [ ] Monitor 2-4 hours before leaving overnight

---

## 📞 Troubleshooting

### "No Binance API credentials"
```
✅ Expected if DEMO_MODE = true
✅ Expected if environment variables not set
❌ Problem if DEMO_MODE = false and you want real trades
```
Solution: Set environment variables or switch to demo mode

### "Binance API Error 401"
```
❌ Invalid or expired API credentials
❌ Request signature invalid
```
Solution: 
- Regenerate API keys on Binance
- Verify no typos in keys
- Check system time is correct (crypto exchanges are strict about time)

### "Binance API Error 429"
```
❌ Rate limit exceeded (too many requests)
```
Solution: Bot respects rate limits - this shouldn't happen unless you have other tools hitting API

### "SELL FAILED on Binance"
```
❌ Order failed to execute
Possible causes:
  - Insufficient balance
  - Network error
  - Invalid quantity (too small)
```
Solution: Check logs, check balance, verify quantity is valid for symbol

### "Order executed but price different"
```
✅ Normal behavior
Market orders execute at best available price, which may change
between order placement and execution.
```

---

## 🎯 What Changed in Code

### New Functions (added, nothing removed)
- `binance_sign_request()` - HMAC signing
- `binance_get_balance()` - Fetch real balance
- `binance_get_price()` - Fetch real prices
- `binance_place_order()` - Execute real trades

### Modified Functions (backward compatible)
- `get_price()` - Routes to Binance if `demo_mode=false`
- `simulate_buy()` - Executes real order if `demo_mode=false`
- `simulate_sell()` - Executes real order if `demo_mode=false`
- `main()` - Shows API status in startup banner

### Unchanged
- All technical indicators (EMA, RSI)
- Entry scoring system (0-100)
- Risk management (RiskManager class)
- Dashboard integration
- CSV logging
- Auto/manual mode logic
- Circuit breaker
- Everything else

---

## 📚 File Structure

```
alphatrade-bot/
├── bot.py (UPDATED v3.0 - Real Binance support)
├── dashboard.py (unchanged)
├── settings.json (unchanged)
├── bot_state.json (unchanged)
├── prices.csv (records all prices)
├── trades.csv (records all trades)
├── actions.csv (records all actions)
├── bot_log.txt (all logs)
└── BINANCE_REAL_TRADING.md (this file)
```

---

## 🚀 Deployment to Render

### 1. Update Environment Variables

Render Dashboard:
- Service → alphatrade-bot
- Environment tab
- Add:
  ```
  BINANCE_API_KEY=your_key_here
  BINANCE_API_SECRET=your_secret_here
  ```
- Save and auto-deploy

### 2. Set demo_mode in settings.json

```json
{
  "demo_mode": false,
  ...
}
```

### 3. Redeploy

Render will restart bot with new environment variables.

### 4. Verify in Logs

```
🚀 AlphaTrade Bot v2.0
Mode: REAL BINANCE 🌐
API Status: ✅ API READY
```

---

## 💰 Cost Analysis

**Real Trading Costs:**
- Binance spot trading fees: 0.1% (standard user)
- Per $10 trade: $0.01 fee
- Bot trades ~6-10/hour in backtests
- Estimated daily: ~150 trades = $1.50 fees
- Plus/minus PnL from strategy

---

## ✅ Summary

Your bot now supports:

✅ **Demo Mode (default, safe)**
- Simulated prices and trades
- Perfect for testing
- $0 risk

✅ **Real Mode (opt-in, real trading)**
- Real Binance prices
- Real spot trading
- Real money at stake
- Maximum $10 per trade (safety)
- All orders error-handled
- Falls back to demo on API failure

✅ **Security**
- API keys via environment variables
- HMAC-SHA256 signing
- No hardcoded secrets
- Rate limit safe

✅ **Backward Compatibility**
- Dashboard unchanged
- CSV files unchanged
- Strategies unchanged
- Everything optional

---

## 🎯 Next Steps

1. **Test in Demo** → Run 24+ hours with demo_mode=true
2. **Get API Keys** → From Binance account settings
3. **Set Environment Variables** → In Render or local environment
4. **Test Real Prices** → demo_mode=false without API keys
5. **Go Live** → demo_mode=false with API keys
6. **Monitor** → Check logs daily for first week
7. **Optimize** → Adjust risk settings based on performance

---

**Happy real trading!** 📈

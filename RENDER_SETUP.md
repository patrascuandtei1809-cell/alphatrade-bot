# Render Setup Guide - Real Binance Trading

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Binance API Keys

1. Go to https://www.binance.com
2. Sign in → Settings → Account Security
3. Enable 2FA (Google Authenticator)
4. Go to Settings → API Management
5. Create New Key (System generated)
6. Set Permissions:
   - ✅ Spot Trading Read
   - ✅ Spot Trading Write
   - ❌ Margin Trading
   - ❌ Futures Trading
   - ❌ Withdrawal
7. **Copy both:**
   - API Key
   - Secret Key

### Step 2: Add to Render

1. Log in to https://render.com
2. Find your "alphatrade-bot" service
3. Click Service name → **Environment** tab
4. Click **Add Environment Variable**
5. Add two variables:
   ```
   Name: BINANCE_API_KEY
   Value: <paste your API key>
   
   Name: BINANCE_API_SECRET
   Value: <paste your secret key>
   ```
6. Click **Save**
7. Render auto-deploys (wait 2-3 minutes)

### Step 3: Activate Real Trading

1. Download `settings.json` from Render
2. Change `"demo_mode": true` to `"demo_mode": false`
3. Upload back to Render
4. Render restarts bot

### Step 4: Verify in Logs

Click **Logs** tab on Render:
```
✅ Mode: REAL BINANCE 🌐
✅ API Status: ✅ API READY
```

If you see errors, check:
- Environment variables are set
- No typos in API keys
- Binance account has spot trading enabled

---

## 🛡️ Safety First

### MAX TRADE SIZE
- Hard limit: **$10 USDT per trade**
- Cannot be changed (enforced in code)
- Prevents accidents

### CIRCUIT BREAKER
- Auto stops if **-10% drawdown**
- Auto stops after **3 losing trades**
- Prevents catastrophic loss

### ERROR HANDLING
- If API fails → falls back to demo prices
- If order fails → logs error, tries next cycle
- Never crashes

---

## 🔄 Demo to Real Transition

### Option A: Test First (Recommended)
```json
"demo_mode": true
```
Run 24-48 hours with simulated trades. Verify:
- Strategy works
- No crashes
- Logs look good

Then switch to real.

### Option B: Real Prices, Simulated Trades
```json
"demo_mode": false
```
Without API keys in environment variables:
- Fetches real Binance prices
- Simulates trades (no real orders)
- Verify price data is correct
- Still safe

### Option C: Full Real Trading
```json
"demo_mode": false
```
With API keys in environment:
- Real prices ✅
- Real trades ✅
- Real money ✅

---

## 📊 Expected Trades

- **Demo Mode**: 6-10 trades/hour (filtered by entry score)
- **Real Mode**: Same, but on real Binance

With $10 max per trade and risk management:
- Very conservative
- Great for learning
- Lower profit but lower risk

---

## 💬 Testing Command

To verify Binance connection without trading:

```bash
curl "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
```

Should return real BTC price.

---

## ⚠️ Do NOT

- ❌ Share API keys
- ❌ Commit to GitHub
- ❌ Use the same API keys on multiple bots
- ❌ Allow withdrawal permission
- ❌ Set demo_mode=false without reading BINANCE_REAL_TRADING.md

---

## ✅ Do

- ✅ Use environment variables for API keys
- ✅ Test in demo mode first
- ✅ Monitor logs for first 24 hours
- ✅ Keep IP whitelist enabled
- ✅ Rotate API keys monthly
- ✅ Start with small amounts

---

## 🆘 Troubleshooting

**Bot won't start?**
- Check logs in Render
- Verify environment variables are set
- Try demo mode first

**"API Status: ⚠️ NO API CREDENTIALS"?**
- Environment variables not set
- Set them in Render Environment tab
- Render needs restart after adding vars

**Orders failing?**
- Check Binance account has balance
- Verify spot trading is enabled
- Check logs for specific error message

**Bot trading too much?**
- Increase `min_entry_score` in settings.json (default 70)
- Increase `trade_cooldown_seconds` (default 180)
- Both will reduce trade frequency

---

## 📈 Monitor Dashboard

While bot runs:
1. Open Streamlit dashboard
2. Check **Auto Status** indicator
3. Watch **Entry Score** for new trades
4. Monitor **Profit** and **Drawdown**
5. Check logs for any errors

Everything should work the same, just with real money now.

---

**Ready? Go to step 1!** 🚀

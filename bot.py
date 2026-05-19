#!/usr/bin/env python3
"""AlphaTrade Bot v2.0 - Professional Trading System
Upgraded with Risk Management, Smart Entries, Market Awareness, and Analytics
NOW WITH REAL BINANCE SUPPORT!
"""
#!/usr/bin/env python3
import csv, json, os, random, time, hashlib, hmac
from datetime import datetime, timedelta
import requests
from collections import deque

SETTINGS_FILE = "settings.json"
settings = None

# ============================================================================
# REAL BINANCE API SUPPORT (v3.0 Enhancement)
# ============================================================================

# Load API credentials from environment variables
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET", "")
BINANCE_BASE_URL = "https://api.binance.com"
MAX_TRADE_SIZE_USDT = 10.0  # Safety limit per trade

def binance_sign_request(params, secret):
    """Sign Binance API request with HMAC-SHA256"""
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(
        secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def binance_get_balance(symbol_base):
    """Get real balance from Binance for a symbol (e.g., 'BTC' from 'BTCUSDT')"""
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        log("⚠️  No Binance API credentials - cannot fetch real balance")
        return None
    
    try:
        timestamp = int(time.time() * 1000)
        params = {"timestamp": timestamp, "recvWindow": 5000}
        params["signature"] = binance_sign_request(params, BINANCE_API_SECRET)
        
        headers = {"X-MBX-APIKEY": BINANCE_API_KEY}
        r = requests.get(
            f"{BINANCE_BASE_URL}/api/v3/account",
            params=params,
            headers=headers,
            timeout=10
        )
        
        if r.status_code != 200:
            log(f"⚠️  Binance balance error: {r.status_code} - {r.text}")
            return None
        
        data = r.json()
        for balance_item in data.get("balances", []):
            if balance_item["asset"] == symbol_base:
                return float(balance_item.get("free", 0))
        
        return 0.0
    except Exception as e:
        log(f"⚠️  Binance balance fetch error: {str(e)}")
        return None

def binance_get_price(symbol):
    """Get real price from Binance"""
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        log("⚠️  No Binance API credentials - cannot fetch real price")
        return None
    
    try:
        r = requests.get(
            f"{BINANCE_BASE_URL}/api/v3/ticker/price",
            params={"symbol": symbol},
            timeout=10
        )
        
        if r.status_code != 200:
            log(f"⚠️  Binance price error: {r.status_code}")
            return None
        
        return float(r.json()["price"])
    except Exception as e:
        log(f"⚠️  Binance price error {symbol}: {str(e)}")
        return None

def binance_place_order(symbol, side, quantity_or_amount):
    """Place market order on Binance (BUY or SELL)
    For BUY: quantity_or_amount is USDT amount, uses quoteOrderQty
    For SELL: quantity_or_amount is asset quantity, uses quantity
    """
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        log("❌ TRADE ERROR: No Binance API credentials")
        return False, None
    
    try:
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "timestamp": timestamp,
            "recvWindow": 5000
        }
        
        # BUY uses quoteOrderQty (USDT amount), SELL uses quantity (asset qty)
        if side.upper() == "BUY":
            params["quoteOrderQty"] = quantity_or_amount
        else:
            params["quantity"] = quantity_or_amount
        
        params["signature"] = binance_sign_request(params, BINANCE_API_SECRET)
        
        headers = {"X-MBX-APIKEY": BINANCE_API_KEY}
        r = requests.post(
            f"{BINANCE_BASE_URL}/api/v3/order",
            params=params,
            headers=headers,
            timeout=10
        )
        
        if r.status_code != 200:
            log(f"❌ BINANCE ORDER FAILED: {r.status_code} - {r.text}")
            return False, None
        
        data = r.json()
        order_id = data.get("orderId")
        executed_qty = float(data.get("executedQty", 0))
        cummulative_quote = float(data.get("cummulativeQuoteAssetTransacted", 0))
        fill_price = (cummulative_quote / executed_qty) if executed_qty > 0 else 0
        
        log(f"✅ BINANCE ORDER FILLED: {side} {executed_qty} {symbol} @ {fill_price} (Order ID: {order_id})")
        return True, fill_price
    except Exception as e:
        log(f"❌ BINANCE ORDER ERROR: {str(e)}")
        return False, None

SETTINGS_FILE = "settings.json"
settings = None

DEFAULT_SETTINGS = {
    "demo_mode": True,
    "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    "base_currency": "USDT",
    "start_balance": 1000.0,
    "trade_size_usdt": 10.0,
    "prices_file": "prices.csv",
    "trades_file": "trades.csv",
    "log_file": "bot_log.txt",
    "state_file": "bot_state.json",
    "commands_file": "commands.json",
    "actions_file": "actions.csv",
    "refresh_interval": 60,
    "binance": {
        "use_testnet": True,
        "testnet_base_url": "https://testnet.binance.vision",
        "mainnet_base_url": "https://api.binance.com",
    },
    "default_strategy": "trend_scalper",
    "strategies": {
        "trend_scalper": {"label": "Trend Scalper"},
        "mean_reversion": {"label": "Mean Reversion"},
        "breakout_momentum": {"label": "Breakout Momentum"},
    },
    # PROFESSIONAL RISK MANAGEMENT SETTINGS
    "risk": {
        "max_risk_per_trade_pct": 2.0,
        "max_total_exposure_pct": 50.0,
        "max_drawdown_pct": 10.0,
        "max_consecutive_losses": 3,
        "volatility_threshold_pct": 3.0,
        "trade_cooldown_seconds": 180,
        "min_entry_score": 70,
        "use_trailing_stop": True,
        "trailing_stop_pct": 0.25,
    },
}

def load_settings():
    global settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            settings.setdefault(k, v)
    else:
        settings = DEFAULT_SETTINGS.copy()
        save_settings()
    
    # Read DEMO_MODE from Render environment variable
    demo_mode_env = os.environ.get("DEMO_MODE", "").lower()
    if demo_mode_env in ("true", "1", "yes"):
        settings["demo_mode"] = True
    elif demo_mode_env in ("false", "0", "no"):
        settings["demo_mode"] = False
    
    settings["refresh_interval"] = 60
    return settings

def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        log(f"⚠️  JSON load error {path}: {str(e)}")
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log(f"⚠️  JSON save error {path}: {str(e)}")

def log(msg):
    text = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | {msg}"
    print(text)
    try:
        with open(settings["log_file"], "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        pass

def get_price(symbol):
    """Get price - demo mode uses simulated prices, real mode uses Binance API only"""
    if settings.get("demo_mode", True):
        # DEMO MODE: Simulated prices
        base = {"BTCUSDT": 78400, "ETHUSDT": 2200, "SOLUSDT": 86}.get(symbol, 100)
        return round(base + base * random.uniform(-0.02, 0.02), 2)
    else:
        # REAL MODE: Use Binance API only, NO FALLBACK
        price = binance_get_price(symbol)
        if price is not None:
            return price
        # If API fails, log error and return None - no demo fallback
        log(f"❌ PRICE FETCH FAILED {symbol}: Binance API unavailable")
        return None

def append_price(symbol, price):
    try:
        with open(settings["prices_file"], "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([int(time.time()), symbol, price])
    except Exception as e:
        log(f"❌ Price append error: {str(e)}")

def recent_prices(symbol, limit=80):
    prices = []
    path = settings["prices_file"]
    if not os.path.exists(path):
        return prices

    try:
        with open(path, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        for row in rows[-500:]:
            if len(row) >= 3 and row[1] == symbol:
                try:
                    prices.append(float(row[2]))
                except Exception:
                    pass
    except Exception:
        pass

    return prices[-limit:]

def ema(values, period):
    if len(values) < period:
        return None
    k = 2 / (period + 1)
    value = values[0]
    for price in values[1:]:
        value = price * k + value * (1 - k)
    return value

def rsi(values, period=14):
    if len(values) < period + 1:
        return 50
    gains = 0
    losses = 0
    for i in range(-period, 0):
        diff = values[i] - values[i - 1]
        gains += max(diff, 0)
        losses += max(-diff, 0)
    if losses == 0:
        return 100
    rs = gains / losses
    return 100 - (100 / (1 + rs))

def save_action(symbol, action, amount, price, strategy, reason, result, qty):
    with open(settings["actions_file"], "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([int(time.time()), symbol, action.upper(), amount, price, strategy, reason, result, qty])

def save_trade(symbol, mode, action, price, amount, qty, reason):
    with open(settings["trades_file"], "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([symbol, mode, action.upper(), price, int(time.time()), amount, qty, reason])

def ensure_position(symbol, state):
    state["portfolio"]["positions"].setdefault(symbol, {
        "qty": 0.0,
        "entry_price": 0.0,
        "max_price": 0.0,
        "last_action": "idle",
        "last_reason": "waiting",
        "last_buy_time": 0,
        "manual_locked": False,
        "entry_signal": None,
    })

# ============================================================================
# PROFESSIONAL RISK MANAGEMENT ENGINE
# ============================================================================

class RiskManager:
    """Professional risk management layer that controls all trading decisions"""
    
    def __init__(self, state, settings):
        self.state = state
        self.settings = settings
        self.risk_config = settings.get("risk", {})
        self.trade_history = deque(maxlen=100)
        self.last_trade_times = {}
        
    def _update_analytics(self):
        """Update trading analytics for risk calculation"""
        portfolio = self.state["portfolio"]
        starting_balance = self.settings["start_balance"]
        cash = float(portfolio.get("cash", 0))
        
        total_value = cash
        for sym, pos in portfolio.get("positions", {}).items():
            if isinstance(pos, dict):
                qty = float(pos.get("qty", 0))
                price = self.state.get("market", {}).get("prices", {}).get(sym, 0)
                total_value += qty * price
        
        equity = total_value
        profit = equity - starting_balance
        drawdown = ((starting_balance - equity) / starting_balance * 100) if equity < starting_balance else 0
        
        self.state["analytics"] = {
            "equity": equity,
            "profit": profit,
            "max_equity": max(float(self.state.get("analytics", {}).get("max_equity", equity)), equity),
            "max_drawdown": max(float(self.state.get("analytics", {}).get("max_drawdown", 0)), drawdown),
            "total_trades": len(self.trade_history),
            "consecutive_losses": self._count_consecutive_losses(),
        }
    
    def _count_consecutive_losses(self):
        """Count consecutive losing trades"""
        if not self.trade_history:
            return 0
        losses = 0
        for trade in reversed(self.trade_history):
            if trade.get("pnl", 0) < 0:
                losses += 1
            else:
                break
        return losses
    
    def is_circuit_breaker_triggered(self):
        """Check if circuit breaker should stop trading"""
        self._update_analytics()
        analytics = self.state.get("analytics", {})
        
        max_drawdown = self.risk_config.get("max_drawdown_pct", 10.0)
        if analytics.get("max_drawdown", 0) >= max_drawdown:
            log(f"🚨 CIRCUIT BREAKER: Max drawdown reached ({analytics['max_drawdown']:.2f}% >= {max_drawdown}%)")
            return True
        
        consecutive_losses = self.risk_config.get("max_consecutive_losses", 3)
        if analytics.get("consecutive_losses", 0) >= consecutive_losses:
            log(f"🚨 CIRCUIT BREAKER: {consecutive_losses} consecutive losses, halting trades")
            return True
        
        return False
    
    def get_safe_trade_size(self, symbol):
        """Calculate safe trade size based on risk management"""
        try:
            portfolio = self.state["portfolio"]
            cash = float(portfolio.get("cash", 0))
            equity = float(self.state.get("analytics", {}).get("equity", self.settings["start_balance"]))
            
            # Max risk per trade
            max_risk_per_trade = (equity * self.risk_config.get("max_risk_per_trade_pct", 2.0)) / 100
            
            # Max total exposure
            max_exposure = (equity * self.risk_config.get("max_total_exposure_pct", 50.0)) / 100
            total_exposed = 0
            for sym, pos in portfolio.get("positions", {}).items():
                if isinstance(pos, dict):
                    qty = float(pos.get("qty", 0))
                    price = self.state.get("market", {}).get("prices", {}).get(sym, 0)
                    total_exposed += qty * price
            
            available_exposure = max_exposure - total_exposed
            
            safe_size = min(cash, max_risk_per_trade, available_exposure)
            return max(0, safe_size)
        except Exception as e:
            log(f"❌ Safe trade size error: {str(e)}")
            return 0
    
    def can_trade(self, symbol):
        """Check if trading is allowed given all constraints"""
        if self.is_circuit_breaker_triggered():
            return False, "circuit_breaker_active"
        
        # Cooldown check
        last_trade_time = self.last_trade_times.get(symbol, 0)
        cooldown_secs = self.risk_config.get("trade_cooldown_seconds", 180)
        if time.time() - last_trade_time < cooldown_secs:
            return False, f"cooldown_{int(cooldown_secs - (time.time() - last_trade_time))}s"
        
        return True, "allowed"
    
    def record_trade(self, symbol, entry_price, exit_price, qty):
        """Record trade for analytics"""
        pnl = ((exit_price - entry_price) / entry_price * 100) if entry_price > 0 else 0
        self.trade_history.append({
            "symbol": symbol,
            "entry": entry_price,
            "exit": exit_price,
            "pnl": pnl,
            "qty": qty,
            "time": time.time(),
        })
        self.last_trade_times[symbol] = time.time()

# ============================================================================
# MARKET REGIME & ENTRY INTELLIGENCE
# ============================================================================

def detect_market_regime(symbol):
    """Detect current market conditions"""
    try:
        prices = recent_prices(symbol, 100)
        if len(prices) < 20:
            return "unknown", 0
        
        recent = prices[-20:]
        volatility = (max(recent) - min(recent)) / (sum(recent) / len(recent)) * 100
        
        # Trend detection
        ema_short = ema(prices, 10)
        ema_long = ema(prices, 30)
        
        if ema_short and ema_long:
            if ema_short > ema_long * 1.02:
                regime = "uptrend"
            elif ema_short < ema_long * 0.98:
                regime = "downtrend"
            else:
                regime = "sideways"
        else:
            regime = "unknown"
        
        return regime, volatility
    except Exception as e:
        log(f"⚠️  Regime detection error {symbol}: {str(e)}")
        return "unknown", 0

def calculate_entry_score(symbol):
    """Multi-condition entry scoring system (0-100)
    
    Conditions:
    - EMA crossover trend
    - RSI zone
    - Momentum confirmation
    - Volatility filter
    - Higher timeframe confirmation
    
    Returns: (score, reason_dict)
    """
    try:
        prices = recent_prices(symbol, 80)
        if len(prices) < 55:
            return 0, {"reason": "insufficient_history", "score_components": {}}
        
        score = 0
        components = {}
        
        # 1. EMA Trend (0-30 points)
        ema20 = ema(prices, 20)
        ema50 = ema(prices, 50)
        ema200 = ema(prices, 60)  # Simulated longer-term
        
        if ema20 and ema50:
            if ema20 > ema50:
                trend_score = 30 if ema20 > ema200 else 20
                score += trend_score
                components["ema_trend"] = {"score": trend_score, "status": "bullish"}
            elif ema20 < ema50:
                components["ema_trend"] = {"score": 0, "status": "bearish"}
            else:
                components["ema_trend"] = {"score": 10, "status": "neutral"}
                score += 10
        
        # 2. RSI Zone (0-25 points)
        rsi_val = rsi(prices, 14)
        if 40 <= rsi_val <= 60:
            rsi_score = 25
            components["rsi_zone"] = {"score": rsi_score, "value": rsi_val, "status": "optimal"}
            score += rsi_score
        elif 30 <= rsi_val < 40:
            rsi_score = 15
            components["rsi_zone"] = {"score": rsi_score, "value": rsi_val, "status": "acceptable"}
            score += rsi_score
        else:
            components["rsi_zone"] = {"score": 0, "value": rsi_val, "status": "overbought" if rsi_val > 70 else "oversold"}
        
        # 3. Momentum Confirmation (0-25 points)
        last3_up = prices[-1] > prices[-2] > prices[-3]
        last5_up = all(prices[i] > prices[i-1] for i in range(-5, 0))
        
        if last5_up:
            momentum_score = 25
            components["momentum"] = {"score": momentum_score, "status": "strong"}
            score += momentum_score
        elif last3_up:
            momentum_score = 15
            components["momentum"] = {"score": momentum_score, "status": "moderate"}
            score += momentum_score
        else:
            components["momentum"] = {"score": 0, "status": "weak"}
        
        # 4. Volatility Filter (0-20 points)
        recent_vol = (max(prices[-20:]) - min(prices[-20:])) / (sum(prices[-20:]) / len(prices[-20:])) * 100
        if 0.5 < recent_vol < 3.0:
            vol_score = 20
            components["volatility"] = {"score": vol_score, "value": recent_vol, "status": "healthy"}
            score += vol_score
        elif 0.1 < recent_vol <= 0.5:
            vol_score = 10
            components["volatility"] = {"score": vol_score, "value": recent_vol, "status": "low"}
            score += vol_score
        else:
            components["volatility"] = {"score": 0, "value": recent_vol, "status": "extreme" if recent_vol >= 3.0 else "dead"}
        
        # 5. Dip Recovery Pattern (0-20 bonus points)
        if len(prices) >= 15:
            recent_low = min(prices[-15:])
            current = prices[-1]
            if current > recent_low * 1.005 and rsi_val < 55:
                dip_score = 20
                components["dip_recovery"] = {"score": dip_score, "status": "detected"}
                score += dip_score
        
        return min(100, score), {"components": components, "score": min(100, score)}
    
    except Exception as e:
        log(f"⚠️  Entry score error {symbol}: {str(e)}")
        return 0, {"reason": "error", "error": str(e)}

def simulate_buy(symbol, amount_usdt, reason, state, manual=False):
    """Buy - demo mode simulates, real mode uses Binance API"""
    try:
        ensure_position(symbol, state)
        cash = float(state["portfolio"].get("cash", 0))
        amount_usdt = min(float(amount_usdt), cash)
        
        # Safety limit for real trades
        if not settings.get("demo_mode", True):
            amount_usdt = min(amount_usdt, MAX_TRADE_SIZE_USDT)

        if amount_usdt <= 0:
            log("BUY skipped: no cash")
            return

        price = get_price(symbol)
        if price is None or price <= 0:
            log(f"❌ BUY ERROR {symbol}: Invalid price")
            return
        
        qty = round(amount_usdt / price, 8)
        pos = state["portfolio"]["positions"][symbol]

        # REAL MODE: Execute on Binance with USDT amount
        if not settings.get("demo_mode", True):
            success, actual_price = binance_place_order(symbol, "BUY", amount_usdt)
            if not success:
                log(f"❌ BUY FAILED on Binance {symbol}")
                return
            
            # Use actual filled price if available
            if actual_price:
                price = actual_price
                amount_usdt = round(qty * price, 2)

        # Update position (same for demo and real)
        old_qty = float(pos.get("qty", 0))
        old_entry = float(pos.get("entry_price", 0))
        new_qty = old_qty + qty

        pos["qty"] = round(new_qty, 8)
        pos["entry_price"] = ((old_entry * old_qty) + (price * qty)) / new_qty if new_qty > 0 else 0
        pos["max_price"] = max(float(pos.get("max_price", 0)), price)
        pos["last_action"] = "BUY"
        pos["last_reason"] = reason
        pos["last_buy_time"] = int(time.time())
        pos["manual_locked"] = False
        pos["entry_signal"] = reason

        state["portfolio"]["cash"] = round(cash - amount_usdt, 2)

        mode = "REAL" if not settings.get("demo_mode", True) else "DEMO"
        save_trade(symbol, mode, "BUY", price, amount_usdt, qty, reason)
        save_action(symbol, "BUY", amount_usdt, price, state["bot"]["current_strategy"], reason, "executed", qty)
        log(f"✅ BUY {symbol} [{mode}] | ${amount_usdt:.2f} qty={qty} @ {price} | {reason}")
    except Exception as e:
        log(f"❌ BUY ERROR {symbol}: {str(e)}")

def simulate_sell(symbol, qty, reason, state, manual=False):
    """Sell - demo mode simulates, real mode uses Binance API"""
    try:
        ensure_position(symbol, state)
        pos = state["portfolio"]["positions"][symbol]
        qty = min(float(qty), float(pos.get("qty", 0)))

        if qty <= 0:
            log("SELL skipped: no position")
            return

        price = get_price(symbol)
        if price is None or price <= 0:
            log(f"❌ SELL ERROR {symbol}: Invalid price")
            return

        # REAL MODE: Execute on Binance
        if not settings.get("demo_mode", True):
            success, actual_price = binance_place_order(symbol, "SELL", qty)
            if not success:
                log(f"❌ SELL FAILED on Binance {symbol}")
                return
            
            # Use actual filled price if available
            if actual_price:
                price = actual_price

        proceeds = round(qty * price, 2)
        entry_price = float(pos.get("entry_price", 0))
        pnl_pct = ((price - entry_price) / entry_price * 100) if entry_price > 0 else 0

        state["portfolio"]["cash"] = round(float(state["portfolio"].get("cash", 0)) + proceeds, 2)
        pos["qty"] = round(float(pos.get("qty", 0)) - qty, 8)

        if pos["qty"] <= 0.00000001:
            pos["qty"] = 0.0
            pos["entry_price"] = 0.0
            pos["max_price"] = 0.0

        pos["last_action"] = "SELL"
        pos["last_reason"] = reason
        pos["manual_locked"] = False

        mode = "REAL" if not settings.get("demo_mode", True) else "DEMO"
        save_trade(symbol, mode, "SELL", price, proceeds, qty, reason)
        save_action(symbol, "SELL", proceeds, price, state["bot"]["current_strategy"], reason, "executed", qty)
        log(f"✅ SELL {symbol} [{mode}] | qty={qty} @ {price} | PnL: {pnl_pct:+.2f}% | {reason}")
    except Exception as e:
        log(f"❌ SELL ERROR {symbol}: {str(e)}")

def process_command(command, state):
    try:
        action = command.get("action")
        symbol = command.get("symbol")
        payload = command.get("payload", {})

        if action == "manual_buy":
            amount = float(payload.get("amount", settings.get("trade_size_usdt", 10.0)))
            log(f"📍 MANUAL BUY TRIGGERED: {symbol} ${amount}")
            simulate_buy(symbol, amount, f"Manual BUY ${amount}", state, manual=True)

        elif action == "manual_sell":
            ensure_position(symbol, state)
            qty = state["portfolio"]["positions"][symbol].get("qty", 0)
            log(f"📍 MANUAL SELL TRIGGERED: {symbol} qty={qty}")
            simulate_sell(symbol, qty, "Manual SELL", state, manual=True)

        elif action == "start_auto":
            state["bot"]["auto_enabled"] = True
            for s in state["portfolio"]["positions"]:
                state["portfolio"]["positions"][s]["manual_locked"] = False
            log("🟢 AUTO MODE STARTED - bot will execute auto trades every 60s")

        elif action == "stop_auto":
            state["bot"]["auto_enabled"] = False
            log("🔴 AUTO MODE STOPPED - manual mode only")

        elif action == "set_strategy":
            strategy = payload.get("strategy")
            if strategy:
                state["bot"]["current_strategy"] = strategy
                settings["strategy"] = strategy
                save_settings()
                log(f"⚙️ STRATEGY CHANGED TO: {strategy}")

        elif action == "set_enabled_symbols":
            syms = payload.get("symbols", [])
            if syms:
                state["bot"]["enabled_symbols"] = syms
                log(f"📋 WATCHLIST UPDATED: {', '.join(syms)}")
    except Exception as e:
        log(f"❌ COMMAND ERROR: {str(e)}")

def run_auto_strategy(symbol, state, risk_manager):
    """Execute strategy with professional risk management"""
    try:
        ensure_position(symbol, state)
        pos = state["portfolio"]["positions"][symbol]

        if pos.get("manual_locked", False):
            log(f"⏸️  AUTO SKIPPED {symbol}: manual action in progress")
            return

        cash = float(state["portfolio"].get("cash", 0))
        price = get_price(symbol)

        # RISK CHECK: Can we trade?
        can_trade, reason = risk_manager.can_trade(symbol)
        if not can_trade:
            log(f"🚫 TRADE BLOCKED {symbol}: {reason}")
            return

        # ENTRY LOGIC: Smart scoring system
        if float(pos.get("qty", 0)) == 0 and cash > 1:
            score, score_details = calculate_entry_score(symbol)
            min_score = settings.get("risk", {}).get("min_entry_score", 70)
            
            if score >= min_score:
                safe_size = risk_manager.get_safe_trade_size(symbol)
                if safe_size > 0:
                    log(f"🔔 ENTRY SIGNAL {symbol}: Score {score}/100 (threshold: {min_score})")
                    log(f"   Entry components: {score_details}")
                    simulate_buy(symbol, safe_size, f"AUTO ENTRY (score:{score})", state, manual=False)
                else:
                    log(f"⚠️  SIGNAL BUT NO CAPITAL: {symbol} score={score} but safe_size=0")
            else:
                regime, volatility = detect_market_regime(symbol)
                log(f"⏳ WAIT {symbol}: Score {score}/100 < {min_score} (Regime: {regime}, Vol: {volatility:.2f}%)")
            return

        # EXIT LOGIC: Improved TP/SL with trailing stop
        if float(pos.get("qty", 0)) > 0:
            entry = float(pos.get("entry_price", 0))
            max_reached = float(pos.get("max_price", 0))
            pnl = ((price - entry) / entry * 100) if entry else 0
            
            # Update max price for trailing stop
            pos["max_price"] = max(max_reached, price)
            
            # Trailing Stop Loss
            if settings.get("risk", {}).get("use_trailing_stop", True):
                trailing_from_max = ((max_reached - price) / max_reached * 100) if max_reached > 0 else 0
                trailing_threshold = settings.get("risk", {}).get("trailing_stop_pct", 0.25)
                
                if trailing_from_max >= trailing_threshold:
                    log(f"💰 TRAILING STOP: {symbol} dropped {trailing_from_max:.2f}% from peak")
                    simulate_sell(symbol, pos["qty"], f"TRAILING STOP LOSS {pnl:+.2f}%", state, manual=False)
                    risk_manager.record_trade(symbol, entry, price, pos["qty"])
                    return
            
            # Take Profit (dynamic based on volatility)
            tp_target = 0.4
            regime, volatility = detect_market_regime(symbol)
            if regime == "uptrend" and volatility < 1.0:
                tp_target = 0.6
            elif regime == "sideways":
                tp_target = 0.3
            
            if pnl >= tp_target:
                log(f"💰 TAKE PROFIT: {symbol} reached +{pnl:.2f}%")
                simulate_sell(symbol, pos["qty"], f"AUTO TAKE PROFIT +{pnl:.2f}%", state, manual=False)
                risk_manager.record_trade(symbol, entry, price, pos["qty"])
            
            # Stop Loss
            elif pnl <= -0.3:
                log(f"🛑 STOP LOSS: {symbol} hit -{abs(pnl):.2f}%")
                simulate_sell(symbol, pos["qty"], f"AUTO STOP LOSS {pnl:.2f}%", state, manual=False)
                risk_manager.record_trade(symbol, entry, price, pos["qty"])
            
            else:
                log(f"📊 HOLD {symbol}: PnL={pnl:+.2f}% (Regime: {regime})")
    
    except Exception as e:
        log(f"❌ AUTO STRATEGY ERROR {symbol}: {str(e)}")

def execute_strategy(symbol, state, risk_manager):
    run_auto_strategy(symbol, state, risk_manager)

def init_state():
    state = load_json(settings["state_file"], {})

    if not state:
        state = {
            "bot": {
                "auto_enabled": True,
                "current_strategy": settings.get("default_strategy", "trend_scalper"),
                "enabled_symbols": settings.get("symbols", []),
            },
            "portfolio": {"cash": settings["start_balance"], "positions": {}},
            "market": {"prices": {}},
            "analytics": {
                "equity": settings["start_balance"],
                "profit": 0,
                "max_equity": settings["start_balance"],
                "max_drawdown": 0,
                "total_trades": 0,
                "consecutive_losses": 0,
            },
        }

    state.setdefault("bot", {})
    state.setdefault("portfolio", {})
    state.setdefault("market", {})
    state.setdefault("analytics", {})
    state["bot"].setdefault("auto_enabled", True)
    state["bot"].setdefault("current_strategy", settings.get("default_strategy", "trend_scalper"))
    state["bot"].setdefault("enabled_symbols", settings.get("symbols", []))
    state["portfolio"].setdefault("cash", settings["start_balance"])
    state["portfolio"].setdefault("positions", {})
    state["market"].setdefault("prices", {})
    state["analytics"].setdefault("equity", settings["start_balance"])

    for symbol in settings["symbols"]:
        ensure_position(symbol, state)

    return state

def run_bot_cycle(state, risk_manager):
    try:
        commands = load_json(settings["commands_file"], [])
        if commands:
            log(f"📬 Processing {len(commands)} command(s)")
        for cmd in commands:
            process_command(cmd, state)
        save_json(settings["commands_file"], [])

        enabled = state["bot"].get("enabled_symbols", settings["symbols"])

        for symbol in enabled:
            try:
                price = get_price(symbol)
                append_price(symbol, price)
                state["market"]["prices"][symbol] = price
            except Exception as e:
                log(f"❌ PRICE UPDATE ERROR {symbol}: {str(e)}")

        # Update analytics
        risk_manager._update_analytics()
        analytics = state.get("analytics", {})
        
        auto_status = "🟢 RUNNING" if state["bot"].get("auto_enabled", True) else "🔴 STOPPED"
        cb_status = "🚨 CB_ACTIVE" if risk_manager.is_circuit_breaker_triggered() else "✅ OK"
        log(f"🔄 CYCLE: Auto={auto_status} | CB={cb_status} | Equity=${analytics.get('equity', 0):.2f} | DD={analytics.get('max_drawdown', 0):.2f}%")

        if state["bot"].get("auto_enabled", True):
            for symbol in enabled:
                execute_strategy(symbol, state, risk_manager)
        else:
            log("⏸️  AUTO MODE OFF - awaiting manual commands or dashboard START AUTO")

        save_json(settings["state_file"], state)
    except Exception as e:
        log(f"❌ CYCLE CRITICAL ERROR: {str(e)}")
def main():
    try:
        load_settings()
        state = init_state()
        risk_manager = RiskManager(state, settings)

        log("=" * 80)
        log("🚀 AlphaTrade Bot v2.0 - PROFESSIONAL TRADING SYSTEM")
        log("=" * 80)
        
        mode_str = "REAL BINANCE 🌐" if not settings.get("demo_mode", True) else "DEMO MODE 🎮"
        api_status = "✅ API READY" if (BINANCE_API_KEY and BINANCE_API_SECRET) else "⚠️  NO API CREDENTIALS"
        
        log(f"Mode: {mode_str}")
        log(f"API Status: {api_status}")
        log(f"Strategy: {state['bot']['current_strategy']}")
        log(f"Starting Balance: ${settings['start_balance']}")
        log("=" * 80)
        log("📊 PROFESSIONAL FEATURES:")
        log("  ✅ Multi-condition entry scoring (0-100)")
        log("  ✅ Dynamic TP/SL based on market regime")
        log("  ✅ Trailing stop loss protection")
        log("  ✅ Circuit breaker (max drawdown, consecutive losses)")
        log("  ✅ Trade cooldown & position limits")
        log("  ✅ Real-time analytics & PnL tracking")
        log("  ✅ Market regime detection (trending/sideways/high-vol)")
        if not settings.get("demo_mode", True):
            log("  ✅ REAL BINANCE SPOT TRADING (max $10/trade for safety)")
        log("=" * 80)
        log("")

        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                log(f"\n[CYCLE #{cycle_count}] Starting at {datetime.utcnow().strftime('%H:%M:%S UTC')}")
                run_bot_cycle(state, risk_manager)
                log(f"[CYCLE #{cycle_count}] Completed - waiting 60s for next cycle...\n")
                time.sleep(60)
            except KeyboardInterrupt:
                log("\n⏹️  Bot interrupted by user - shutting down gracefully")
                save_json(settings["state_file"], state)
                log("✅ State saved - exiting")
                break
            except Exception as cycle_error:
                log(f"⚠️  CYCLE ERROR (will continue): {str(cycle_error)}")
                time.sleep(60)
    except Exception as e:
        log(f"❌ FATAL ERROR: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
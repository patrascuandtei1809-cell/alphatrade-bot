#!/usr/bin/env python3
"""AlphaTrade Dashboard - Fixed REAL/DEMO Display"""

import json
import os
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

SETTINGS_FILE = "settings.json"


def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {path}: {str(e)}")
    return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save {path}: {str(e)}")


settings = load_json(SETTINGS_FILE, {})

is_demo = bool(settings.get("demo_mode", True))
mode_str = "DEMO" if is_demo else "REAL"
mode_label = "DEMO MODE 🎮" if is_demo else "REAL BINANCE 🌐"

st.set_page_config(page_title=f"AlphaTrade {mode_str}", layout="wide", page_icon="🚀")
st_autorefresh(interval=5000, limit=None, key="refresh")

state = load_json(settings.get("state_file", "bot_state.json"), {})

prices_file = settings.get("prices_file", "prices.csv")
trades_file = settings.get("trades_file", "trades.csv")
actions_file = settings.get("actions_file", "actions.csv")
commands_file = settings.get("commands_file", "commands.json")

symbols = settings.get("symbols", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
symbol_names = settings.get("symbol_names", {})
enabled_symbols = state.get("bot", {}).get("enabled_symbols", symbols)
current_strategy = state.get("bot", {}).get("current_strategy", settings.get("default_strategy", "trend_scalper"))
auto_enabled = state.get("bot", {}).get("auto_enabled", False)

start_balance = float(settings.get("start_balance", 1000.0))
base_currency = settings.get("base_currency", "USDT")

strategy_map = settings.get("strategies", {})
strategy_labels = {k: v.get("label", k) for k, v in strategy_map.items()} or {
    "trend_scalper": "Trend Scalper",
    "mean_reversion": "Mean Reversion",
    "breakout_momentum": "Breakout Momentum",
}


def append_command(cmd):
    commands = load_json(commands_file, [])
    commands.append(cmd)
    save_json(commands_file, commands)


def load_prices():
    try:
        if not os.path.exists(prices_file):
            return pd.DataFrame(columns=["time", "symbol", "price", "date"])

        df = pd.read_csv(prices_file, names=["time", "symbol", "price"], on_bad_lines="skip")
        df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
        df["time"] = pd.to_numeric(df["time"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna(subset=["time", "symbol", "price"])
        df["date"] = pd.to_datetime(df["time"], unit="s", errors="coerce")
        df = df.dropna(subset=["date"])
        return df.sort_values("time")
    except Exception as e:
        print(f"Error loading prices: {e}")
        return pd.DataFrame(columns=["time", "symbol", "price", "date"])


def load_actions():
    try:
        if not os.path.exists(actions_file):
            return pd.DataFrame(columns=["time", "symbol", "action", "amount", "price", "strategy", "reason", "result", "qty", "date"])

        df = pd.read_csv(
            actions_file,
            names=["time", "symbol", "action", "amount", "price", "strategy", "reason", "result", "qty"],
            on_bad_lines="skip",
        )

        df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
        df["action"] = df["action"].astype(str).str.strip().str.upper()
        df["time"] = pd.to_numeric(df["time"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
        df = df.dropna(subset=["time", "symbol", "action", "price"])
        df["date"] = pd.to_datetime(df["time"], unit="s", errors="coerce")
        df = df.dropna(subset=["date"])
        return df.sort_values("time")
    except Exception as e:
        print(f"Error loading actions: {e}")
        return pd.DataFrame(columns=["time", "symbol", "action", "amount", "price", "strategy", "reason", "result", "qty", "date"])


def load_trades():
    try:
        if not os.path.exists(trades_file):
            return pd.DataFrame(columns=["symbol", "mode", "action", "price", "time", "amount", "qty", "reason", "date"])

        df = pd.read_csv(
            trades_file,
            names=["symbol", "mode", "action", "price", "time", "amount", "qty", "reason"],
            on_bad_lines="skip",
        )

        df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
        df["mode"] = df["mode"].astype(str).str.strip().str.upper()
        df["action"] = df["action"].astype(str).str.strip().str.upper()
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["time"] = pd.to_numeric(df["time"], errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
        df = df.dropna(subset=["symbol", "price", "time"])
        df["date"] = pd.to_datetime(df["time"], unit="s", errors="coerce")
        df = df.dropna(subset=["date"])
        return df.sort_values("time", ascending=False)
    except Exception as e:
        print(f"Error loading trades: {e}")
        return pd.DataFrame(columns=["symbol", "mode", "action", "price", "time", "amount", "qty", "reason", "date"])


def format_money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "-"


def format_qty(value):
    try:
        return f"{float(value):,.8f}"
    except Exception:
        return "-"


if not os.path.exists(commands_file):
    save_json(commands_file, [])

st.markdown("""
<style>
.stApp { background:#020817; color:#f7f8ff; }
.header-box {
    background:linear-gradient(135deg,#ff2b2b,#ff4d4d);
    padding:18px 20px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,.08);
    margin-bottom:18px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

st.title(f"🚀 AlphaTrade {mode_str}")

auto_status_color = "🟢" if auto_enabled else "🔴"
st.markdown(
    f"<div class='header-box'><strong>Status:</strong> {auto_status_color} {'AUTO RUNNING' if auto_enabled else 'MANUAL MODE'} | "
    f"<strong>Mode:</strong> {mode_label}</div>",
    unsafe_allow_html=True,
)

sidebar = st.sidebar
sidebar.header("Trading controls")

selected_symbol = sidebar.selectbox(
    "Coin",
    symbols,
    format_func=lambda s: f"{symbol_names.get(s, s)} ({s})",
)

selected_strategy = sidebar.radio(
    "Strategy",
    list(strategy_labels.keys()),
    index=list(strategy_labels.keys()).index(current_strategy) if current_strategy in strategy_labels else 0,
    format_func=lambda s: strategy_labels.get(s, s),
)

active_symbols = sidebar.multiselect(
    "Auto watchlist",
    symbols,
    default=enabled_symbols,
    format_func=lambda s: f"{symbol_names.get(s, s)} ({s})",
)

sidebar.markdown("---")
trade_amount = sidebar.number_input("Amount (USDT)", min_value=1.0, value=float(settings.get("trade_size_usdt", 10.0)), step=1.0)
trade_side = sidebar.selectbox("Order side", ["BUY", "SELL"])
manual_symbol = sidebar.selectbox("Order symbol", symbols, index=symbols.index(selected_symbol))

if sidebar.button("Place order"):
    append_command({
        "action": "manual_buy" if trade_side == "BUY" else "manual_sell",
        "symbol": manual_symbol,
        "payload": {"amount": trade_amount, "reason": f"Dashboard {trade_side}"}
    })
    st.success(f"{trade_side} command queued")

if sidebar.button("Start Auto"):
    append_command({"action": "start_auto", "payload": {"reason": "Dashboard auto start"}})
    st.success("Auto trading queued")

if sidebar.button("Stop Auto"):
    append_command({"action": "stop_auto", "payload": {"reason": "Dashboard auto stop"}})
    st.warning("Auto stop queued")

if sidebar.button("Apply strategy & watchlist"):
    append_command({"action": "set_strategy", "payload": {"strategy": selected_strategy}})
    append_command({"action": "set_enabled_symbols", "payload": {"symbols": active_symbols}})
    st.info("Strategy and watchlist update queued")

if sidebar.button("Refresh Now"):
    st.rerun()

market_summary = state.get("market", {}).get("prices", {})
portfolio = state.get("portfolio", {})
cash = float(portfolio.get("cash", start_balance))
positions = portfolio.get("positions", {})

selected_price = market_summary.get(selected_symbol)

if selected_price is None:
    selected_price = 0.0

equity = cash
total_qty = 0.0
open_pnl = 0.0

for sym, pos in positions.items():
    try:
        if isinstance(pos, dict):
            qty = float(pos.get("qty", 0))
            entry = float(pos.get("entry_price", 0))
        else:
            qty = float(pos)
            entry = 0

        total_qty += qty
        price = float(market_summary.get(sym, selected_price if sym == selected_symbol else 0))
        value = qty * price
        equity += value

        if qty > 0 and entry > 0:
            open_pnl += (price - entry) * qty
    except Exception:
        pass

profit = equity - start_balance

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("💰 Cash", format_money(cash))
c2.metric("📊 Qty", format_qty(total_qty))
c3.metric("🪙 Equity", format_money(equity))
c4.metric("📈 Profit", format_money(profit))
c5.metric("💹 Open PnL", format_money(open_pnl))
c6.metric("⚙️ Auto", f"{auto_status_color} {'ON' if auto_enabled else 'OFF'}", label_visibility="visible")

st.markdown(f"**Selected strategy:** {strategy_labels.get(selected_strategy, selected_strategy)} | **Enabled symbols:** {', '.join(active_symbols)}")
st.markdown("---")

st.subheader("📊 Symbol Overview")

prices_df = load_prices()
actions_df = load_actions()

selected_symbol_clean = selected_symbol.strip().upper()
symbol_chart = prices_df[prices_df["symbol"] == selected_symbol_clean].copy()

if not symbol_chart.empty:
    symbol_chart = symbol_chart.sort_values("date").tail(250)
    symbol_chart["ema20"] = symbol_chart["price"].ewm(span=20).mean()
    symbol_chart["ema50"] = symbol_chart["price"].ewm(span=50).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=symbol_chart["date"],
        y=symbol_chart["price"],
        mode="lines",
        name="Price",
        line=dict(color="#62f4ff", width=3),
    ))

    fig.add_trace(go.Scatter(
        x=symbol_chart["date"],
        y=symbol_chart["ema20"],
        mode="lines",
        name="EMA20",
        line=dict(color="#6ee7a8", width=2, dash="dash"),
    ))

    fig.add_trace(go.Scatter(
        x=symbol_chart["date"],
        y=symbol_chart["ema50"],
        mode="lines",
        name="EMA50",
        line=dict(color="#ffb86b", width=2, dash="dash"),
    ))

    fig.update_layout(
        height=520,
        paper_bgcolor="#020817",
        plot_bgcolor="#020817",
        font=dict(color="#f7f8ff"),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"),
        xaxis_rangeslider_visible=False,
    )

    fig.update_xaxes(showgrid=False, tickfont=dict(color="#cbd6ff"))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.12)", tickfont=dict(color="#cbd6ff"))

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No price history yet for the selected coin.")

if not actions_df.empty:
    last = actions_df.sort_values("time").iloc[-1]
    st.success(
        f"🔔 LIVE: {last['action']} {last['symbol']} @ {format_money(last['price'])} | "
        f"Qty: {format_qty(last['qty'])} | Strategy: {last['strategy']} | Reason: {last['reason']}"
    )
else:
    st.info("STATUS: WAITING FOR ACTIVITY")

st.markdown("---")
st.subheader("📊 Current Positions")

position_rows = []

for sym, pos in positions.items():
    if isinstance(pos, dict):
        qty = float(pos.get("qty", 0))
        entry = float(pos.get("entry_price", 0))
    else:
        qty = float(pos)
        entry = 0

    if qty > 0:
        current = float(market_summary.get(sym, selected_price if sym == selected_symbol else 0))
        value = qty * current
        pnl_pct = ((current - entry) / entry * 100) if entry else 0

        position_rows.append({
            "Symbol": sym,
            "Qty": format_qty(qty),
            "Entry": format_money(entry),
            "Current": format_money(current),
            "Value": format_money(value),
            "PnL %": f"{pnl_pct:+.2f}%",
        })

if position_rows:
    st.dataframe(pd.DataFrame(position_rows), use_container_width=True)
else:
    st.info("No open positions")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Actions")
    if not actions_df.empty:
        show = actions_df.sort_values("time", ascending=False).copy()
        show["price"] = show["price"].map(format_money)
        show["amount"] = show["amount"].map(format_money)
        show["qty"] = show["qty"].map(format_qty)
        st.dataframe(show[["date", "symbol", "action", "amount", "price", "strategy", "reason", "result", "qty"]].head(200), use_container_width=True)
    else:
        st.info("No live action events recorded yet.")

with col2:
    st.subheader("Actions Log")
    if not actions_df.empty:
        rows = []
        for _, row in actions_df.sort_values("time", ascending=False).head(25).iterrows():
            rows.append(
                f"{row['date'].strftime('%H:%M:%S')} | {row['symbol']} | {row['action']} | "
                f"{format_money(row['price'])} | {row['strategy']} | {row['reason']}"
            )
        st.code("\n".join(rows))
    else:
        st.info("No action history.")

st.markdown("---")
st.subheader("Trade History")

trades_df = load_trades()

if not trades_df.empty:
    show = trades_df.copy()
    show["price"] = show["price"].map(format_money)
    show["amount"] = show["amount"].map(format_money)
    show["qty"] = show["qty"].map(format_qty)
    st.dataframe(show[["date", "symbol", "mode", "action", "amount", "price", "qty", "reason"]], use_container_width=True)
else:
    st.info("No trades recorded yet.")

st.caption(f"Auto-refresh every 5 seconds. Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
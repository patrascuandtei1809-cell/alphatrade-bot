#!/usr/bin/env python3
"""Initialize app with required files and structure"""

import json
import os

def ensure_files():
    """Create necessary files if they don't exist"""
    
    # Ensure settings.json
    if not os.path.exists("settings.json"):
        settings = {
            "demo_mode": True,
            "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
            "symbol_names": {
                "BTCUSDT": "Bitcoin",
                "ETHUSDT": "Ethereum",
                "SOLUSDT": "Solana"
            },
            "default_symbol": "BTCUSDT",
            "base_currency": "USDT",
            "start_balance": 1000.0,
            "trade_size_usdt": 10.0,
            "refresh_interval": 5,
            "prices_file": "prices.csv",
            "trades_file": "trades.csv",
            "log_file": "bot_log.txt",
            "state_file": "bot_state.json",
            "commands_file": "commands.json",
            "actions_file": "actions.csv",
            "binance": {
                "use_testnet": True,
                "testnet_base_url": "https://testnet.binance.vision",
                "mainnet_base_url": "https://api.binance.com",
            },
            "default_strategy": "trend_scalper",
            "strategies": {
                "trend_scalper": {
                    "label": "Trend Scalper",
                    "description": "Buy into short uptrends and trail profit",
                    "buy": {"ema_fast": 20, "ema_slow": 50, "rsi_max": 68},
                    "sell": {"profit_target_pct": 0.45, "stop_loss_pct": -0.75}
                },
                "mean_reversion": {
                    "label": "Mean Reversion",
                    "description": "Buy dips on oversold signals",
                    "buy": {"rsi_threshold": 34, "dip_pct": -0.35},
                    "sell": {"rsi_exit": 62, "profit_target_pct": 0.85}
                }
            }
        }
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        print("✓ Created settings.json")
    
    # Ensure bot_state.json
    if not os.path.exists("bot_state.json"):
        state = {
            "bot": {
                "auto_enabled": True,
                "current_strategy": "trend_scalper",
                "enabled_symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
                "last_run": None
            },
            "portfolio": {
                "cash": 1000.0,
                "positions": {
                    "BTCUSDT": {"qty": 0.0, "entry_price": 0.0, "max_price": 0.0, "last_action": "idle", "last_reason": "waiting"},
                    "ETHUSDT": {"qty": 0.0, "entry_price": 0.0, "max_price": 0.0, "last_action": "idle", "last_reason": "waiting"},
                    "SOLUSDT": {"qty": 0.0, "entry_price": 0.0, "max_price": 0.0, "last_action": "idle", "last_reason": "waiting"}
                }
            },
            "market": {
                "prices": {"BTCUSDT": 78400, "ETHUSDT": 2200, "SOLUSDT": 86}
            }
        }
        with open("bot_state.json", "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print("✓ Created bot_state.json")
    
    # Ensure commands.json
    if not os.path.exists("commands.json"):
        with open("commands.json", "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        print("✓ Created commands.json")
    
    # Ensure prices.csv exists
    if not os.path.exists("prices.csv"):
        with open("prices.csv", "w", encoding="utf-8") as f:
            f.write("")
        print("✓ Created prices.csv")
    
    # Ensure trades.csv exists
    if not os.path.exists("trades.csv"):
        with open("trades.csv", "w", encoding="utf-8") as f:
            f.write("")
        print("✓ Created trades.csv")
    
    # Ensure actions.csv exists
    if not os.path.exists("actions.csv"):
        with open("actions.csv", "w", encoding="utf-8") as f:
            f.write("")
        print("✓ Created actions.csv")
    
    # Ensure bot_log.txt exists
    if not os.path.exists("bot_log.txt"):
        with open("bot_log.txt", "w", encoding="utf-8") as f:
            f.write("Bot initialized\n")
        print("✓ Created bot_log.txt")
    
    print("\n✓ All files initialized successfully!")

if __name__ == "__main__":
    ensure_files()

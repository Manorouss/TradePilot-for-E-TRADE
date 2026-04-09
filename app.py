#!/usr/bin/env python3
"""Public-safe showcase app for TradePilot for E*TRADE."""

from __future__ import annotations

import random
import re
from datetime import datetime

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


WATCHLIST = [
    "TSLA",
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "NVDA",
    "ADBE",
    "BA",
    "DIS",
    "SBUX",
    "NKE",
]


MARKET_PRICES = {
    "TSLA": {"price": 430.33, "change": -4.81, "change_pct": -1.11, "name": "Tesla, Inc."},
    "AAPL": {"price": 247.25, "change": -2.09, "change_pct": -0.84, "name": "Apple Inc."},
    "MSFT": {"price": 428.15, "change": 3.21, "change_pct": 0.75, "name": "Microsoft Corporation"},
    "GOOGL": {"price": 167.89, "change": 1.45, "change_pct": 0.87, "name": "Alphabet Inc."},
    "AMZN": {"price": 215.43, "change": -0.13, "change_pct": -0.06, "name": "Amazon.com, Inc."},
    "META": {"price": 595.78, "change": 8.32, "change_pct": 1.42, "name": "Meta Platforms, Inc."},
    "NVDA": {"price": 138.25, "change": 2.15, "change_pct": 1.58, "name": "NVIDIA Corporation"},
    "ADBE": {"price": 487.62, "change": 3.14, "change_pct": 0.65, "name": "Adobe Inc."},
    "BA": {"price": 212.51, "change": -1.50, "change_pct": -0.70, "name": "The Boeing Company"},
    "DIS": {"price": 110.12, "change": -1.58, "change_pct": -1.42, "name": "The Walt Disney Company"},
    "SBUX": {"price": 84.76, "change": 1.91, "change_pct": 2.30, "name": "Starbucks Corporation"},
    "NKE": {"price": 67.23, "change": -1.23, "change_pct": -1.80, "name": "NIKE, Inc."},
}


DEMO_POSITIONS = [
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "quantity": 24,
        "market_value": 5934.00,
        "gain_loss": 468.24,
        "gain_loss_pct": 8.57,
    },
    {
        "symbol": "ADBE",
        "name": "Adobe Inc.",
        "quantity": 8,
        "market_value": 3900.96,
        "gain_loss": 244.40,
        "gain_loss_pct": 6.68,
    },
    {
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "quantity": 30,
        "market_value": 4147.50,
        "gain_loss": 712.80,
        "gain_loss_pct": 20.75,
    },
]


DEMO_BALANCE = {
    "cash": 18250.00,
    "buying_power": 36500.00,
    "total_value": 32232.46,
    "margin_balance": 0.00,
}


RESEARCH_DATA = {
    "undervalued": [
        {"symbol": "ADBE", "company": "Adobe Inc", "last": 487.62, "trefis": 540.00, "upside": 10.74, "report": "Demo Quant Model", "date": "2026-04-09"},
        {"symbol": "NKE", "company": "NIKE, Inc.", "last": 67.23, "trefis": 78.50, "upside": 16.76, "report": "Demo Quant Model", "date": "2026-04-09"},
        {"symbol": "DIS", "company": "The Walt Disney Company", "last": 110.12, "trefis": 125.00, "upside": 13.51, "report": "Demo Analyst Pack", "date": "2026-04-09"},
        {"symbol": "BA", "company": "The Boeing Company", "last": 212.51, "trefis": 236.00, "upside": 11.05, "report": "Demo Analyst Pack", "date": "2026-04-09"},
        {"symbol": "SBUX", "company": "Starbucks Corporation", "last": 84.76, "trefis": 95.00, "upside": 12.08, "report": "Demo Analyst Pack", "date": "2026-04-09"},
    ],
    "overvalued": [
        {"symbol": "TSLA", "company": "Tesla, Inc.", "last": 430.33, "target": 398.00, "upside": -7.51, "report": "Demo Risk Screen", "date": "2026-04-09"},
        {"symbol": "META", "company": "Meta Platforms, Inc.", "last": 595.78, "target": 560.00, "upside": -6.01, "report": "Demo Risk Screen", "date": "2026-04-09"},
        {"symbol": "NVDA", "company": "NVIDIA Corporation", "last": 138.25, "target": 131.00, "upside": -5.24, "report": "Demo Risk Screen", "date": "2026-04-09"},
        {"symbol": "MSFT", "company": "Microsoft Corporation", "last": 428.15, "target": 410.00, "upside": -4.24, "report": "Demo Risk Screen", "date": "2026-04-09"},
        {"symbol": "AAPL", "company": "Apple Inc.", "last": 247.25, "target": 239.00, "upside": -3.34, "report": "Demo Risk Screen", "date": "2026-04-09"},
    ],
    "buyrated": [
        {"symbol": "AAPL", "company": "Apple Inc.", "last": 247.25, "rating": "Strong Buy", "analyst": "Demo Street Consensus", "upside": 8.90},
        {"symbol": "ADBE", "company": "Adobe Inc", "last": 487.62, "rating": "Buy", "analyst": "Demo Street Consensus", "upside": 10.74},
        {"symbol": "AMZN", "company": "Amazon.com, Inc.", "last": 215.43, "rating": "Buy", "analyst": "Demo Street Consensus", "upside": 7.25},
        {"symbol": "MSFT", "company": "Microsoft Corporation", "last": 428.15, "rating": "Buy", "analyst": "Demo Street Consensus", "upside": 5.40},
        {"symbol": "NVDA", "company": "NVIDIA Corporation", "last": 138.25, "rating": "Buy", "analyst": "Demo Street Consensus", "upside": 9.80},
    ],
    "sellrated": [
        {"symbol": "TSLA", "company": "Tesla, Inc.", "last": 430.33, "rating": "Reduce", "analyst": "Demo Risk Desk", "downside": 7.51},
        {"symbol": "DIS", "company": "The Walt Disney Company", "last": 110.12, "rating": "Hold/Sell", "analyst": "Demo Risk Desk", "downside": 4.10},
        {"symbol": "NKE", "company": "NIKE, Inc.", "last": 67.23, "rating": "Hold/Sell", "analyst": "Demo Risk Desk", "downside": 3.45},
        {"symbol": "BA", "company": "The Boeing Company", "last": 212.51, "rating": "Reduce", "analyst": "Demo Risk Desk", "downside": 5.05},
        {"symbol": "META", "company": "Meta Platforms, Inc.", "last": 595.78, "rating": "Trim", "analyst": "Demo Risk Desk", "downside": 6.01},
    ],
    "bullish": [
        {"symbol": "NVDA", "company": "NVIDIA Corporation", "last": 138.25, "signal": "Momentum breakout", "momentum": "+9.8%", "description": "Semis leading the tape with improving breadth."},
        {"symbol": "ADBE", "company": "Adobe Inc", "last": 487.62, "signal": "Trend continuation", "momentum": "+6.4%", "description": "Software group rotation remains constructive."},
        {"symbol": "SBUX", "company": "Starbucks Corporation", "last": 84.76, "signal": "Higher lows", "momentum": "+4.9%", "description": "Consumer discretionary pocket showing relative strength."},
        {"symbol": "AAPL", "company": "Apple Inc.", "last": 247.25, "signal": "Institutional accumulation", "momentum": "+5.2%", "description": "Mega-cap leadership remains intact."},
        {"symbol": "AMZN", "company": "Amazon.com, Inc.", "last": 215.43, "signal": "Range breakout", "momentum": "+4.1%", "description": "Retail cloud mix supports the tape."},
    ],
    "bearish": [
        {"symbol": "TSLA", "company": "Tesla, Inc.", "last": 430.33, "signal": "Failed breakout", "momentum": "-5.8%", "description": "High-beta weakness after extended upside run."},
        {"symbol": "DIS", "company": "The Walt Disney Company", "last": 110.12, "signal": "Relative weakness", "momentum": "-3.4%", "description": "Lagging the broader media basket."},
        {"symbol": "BA", "company": "The Boeing Company", "last": 212.51, "signal": "Resistance rejection", "momentum": "-4.6%", "description": "Aerospace volatility remains elevated."},
        {"symbol": "NKE", "company": "NIKE, Inc.", "last": 67.23, "signal": "Trend deterioration", "momentum": "-3.1%", "description": "Consumer margin concerns still weigh."},
        {"symbol": "META", "company": "Meta Platforms, Inc.", "last": 595.78, "signal": "Momentum cooling", "momentum": "-2.7%", "description": "Near-term overextension after a strong run."},
    ],
}


def build_quote(symbol: str) -> dict:
    symbol = symbol.upper()
    data = MARKET_PRICES.get(
        symbol,
        {"price": 100.00, "change": 0.00, "change_pct": 0.00, "name": symbol},
    ).copy()
    drift = random.uniform(-0.35, 0.35)
    data["price"] = round(data["price"] + drift, 2)
    data["change"] = round(data["change"] + drift / 3, 2)
    if data["price"]:
        data["change_pct"] = round((data["change"] / (data["price"] - data["change"])) * 100, 2)
    data["symbol"] = symbol
    data["volume"] = random.randint(900000, 52000000)
    data["timestamp"] = datetime.now().isoformat()
    return data


def extract_symbol(message: str) -> str | None:
    uppercase_words = re.findall(r"\b[A-Z]{1,5}\b", message.upper())
    for word in uppercase_words:
        if word in MARKET_PRICES:
            return word
    return None


def extract_order(message: str) -> dict | None:
    action_match = re.search(r"\b(buy|sell)\b", message, re.IGNORECASE)
    symbol = extract_symbol(message)
    if not action_match or not symbol:
        return None

    quantity_match = re.search(r"\b(\d+)\s*(?:shares?|stocks?)\b", message, re.IGNORECASE)
    if not quantity_match:
        quantity_match = re.search(r"\b(?:buy|sell)\s+(\d+)\b", message, re.IGNORECASE)

    price_match = re.search(
        r"(?:\bat\b|\blimit\b|@)\s*\$?(\d+(?:\.\d{1,2})?)",
        message,
        re.IGNORECASE,
    )
    order_type = "LIMIT" if "limit" in message.lower() or "at" in message.lower() else "MARKET"

    return {
        "action": action_match.group(1).upper(),
        "symbol": symbol,
        "quantity": int(quantity_match.group(1)) if quantity_match else 1,
        "price": float(price_match.group(1)) if price_match and order_type == "LIMIT" else None,
        "order_type": order_type,
    }


def generate_demo_response(message: str) -> str:
    lower = message.lower()

    if any(
        phrase in lower
        for phrase in [
            "what do you do",
            "how does it work",
            "what is this",
            "what can you do",
            "how can you help",
            "ai active",
            "etrade account",
        ]
    ):
        return (
            "TradePilot is designed to make an E*TRADE account AI-active. In the full product, the assistant connects through the E*TRADE API, stays aware of market data, research, portfolio context, and news, and helps you manage trading decisions through chat. You can ask it for analysis, portfolio help, entry and exit thinking, and buy or sell workflows. This public build demonstrates that experience with safe demo data."
        )

    if "portfolio" in lower or "positions" in lower:
        return (
            "This demo is showing a sample portfolio with AAPL, ADBE, and NVDA so visitors can preview how TradePilot presents positions, P&L, and account context. In the full product, this view is meant to reflect your connected E*TRADE account and give the AI assistant the context it needs to help with decisions."
        )

    if "balance" in lower or "buying power" in lower or "cash" in lower:
        return (
            f"Demo account summary: ${DEMO_BALANCE['total_value']:,.2f} total value, "
            f"${DEMO_BALANCE['cash']:,.2f} cash, and ${DEMO_BALANCE['buying_power']:,.2f} buying power. "
            "In the full product, this is the account context the AI assistant uses to help size trades, review risk, and manage your next move."
        )

    order = extract_order(message)
    if order:
        quote = build_quote(order["symbol"])
        if order["order_type"] == "LIMIT" and order["price"] is not None:
            return (
                f"Demo order preview: {order['action']} {order['quantity']} shares of {order['symbol']} "
                f"at ${order['price']:.2f} limit. Last trade is ${quote['price']:.2f}. "
                "In the full product, TradePilot is built to take this kind of chat request, evaluate it with account context and market inputs, and route the workflow through the E*TRADE API."
            )
        return (
            f"Demo order preview: {order['action']} {order['quantity']} shares of {order['symbol']} at market. "
            f"Last trade is ${quote['price']:.2f}. In the full product, TradePilot is built to turn this into an AI-assisted execution workflow through the E*TRADE API."
        )

    symbol = extract_symbol(message)
    if "quote" in lower or "price" in lower or symbol:
        symbol = symbol or "AAPL"
        quote = build_quote(symbol)
        direction = "up" if quote["change"] >= 0 else "down"
        return (
            f"{quote['name']} ({quote['symbol']}) is ${quote['price']:.2f}, {direction} "
            f"${abs(quote['change']):.2f} ({abs(quote['change_pct']):.2f}%) in this demo market feed. "
            "TradePilot is designed to combine quotes like this with research, portfolio context, and news so the AI assistant can help you make better trading decisions."
        )

    return (
        "TradePilot is built to make an E*TRADE account AI-active. Ask about quotes, portfolio context, account status, research, or trade workflows, and this public demo will show how the assistant experience works using safe sample data."
    )


@app.route("/")
def index():
    return render_template("apple_stocks_ui.html")


@app.get("/api/portfolio")
def portfolio():
    total_positions = sum(position["market_value"] for position in DEMO_POSITIONS)
    return jsonify(
        {
            "total_value": round(total_positions + DEMO_BALANCE["cash"], 2),
            "cash": DEMO_BALANCE["cash"],
            "buying_power": DEMO_BALANCE["buying_power"],
            "positions": DEMO_POSITIONS,
        }
    )


@app.get("/api/balance")
def balance():
    return jsonify(DEMO_BALANCE)


@app.get("/api/watchlist")
def watchlist():
    return jsonify({"symbols": WATCHLIST})


@app.get("/api/market/<symbols>")
def market(symbols: str):
    return jsonify([build_quote(symbol) for symbol in symbols.split(",") if symbol])


@app.get("/api/quote/<symbol>")
def quote(symbol: str):
    return jsonify(build_quote(symbol))


@app.get("/api/research/<category>")
def research(category: str):
    return jsonify(RESEARCH_DATA.get(category, RESEARCH_DATA["undervalued"]))


@app.get("/api/models")
def models():
    return jsonify(
        [
            {
                "id": "demo-assistant",
                "name": "Demo Assistant",
                "description": "AI-active E*TRADE workflow preview",
                "available": True,
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "description": "Full-product AI assistant option",
                "available": False,
                "setup": "Not enabled in the public demo",
            },
            {
                "id": "claude-4.5",
                "name": "Claude 4.5",
                "description": "Full-product AI assistant option",
                "available": False,
                "setup": "Not enabled in the public demo",
            },
        ]
    )


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400
    return jsonify({"response": generate_demo_response(message)})


@app.post("/api/order/place")
def place_order():
    payload = request.get_json(silent=True) or {}
    symbol = (payload.get("symbol") or "").upper()
    action = (payload.get("action") or "").upper()
    quantity = int(payload.get("quantity") or 1)
    price = payload.get("price")
    order_type = (payload.get("order_type") or "LIMIT").upper()
    quote = build_quote(symbol or "AAPL")
    return jsonify(
        {
            "order_id": f"DEMO-{random.randint(100000, 999999)}",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "price": price,
            "order_type": order_type,
            "current_price": quote["price"],
            "status": "PREVIEW_ONLY",
            "message": "Demo preview only: this order was not sent to a broker. In the full product, this workflow is designed to run through the E*TRADE API.",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


if __name__ == "__main__":
    print("Starting TradePilot for E*TRADE demo at http://127.0.0.1:8080")
    app.run(debug=True, port=8080, use_reloader=False)

# E*TRADE AI Trading Terminal Demo

An Apple Stocks-inspired trading terminal concept for E*TRADE, built to showcase how a modern broker experience could combine market dashboards, research panels, portfolio visibility, and chat-driven trade workflows in one interface.

This repository is the public demo edition of the project. It is designed for showcasing the software on GitHub without exposing private credentials, real account access, or live order execution.

## About

`A public demo of an E*TRADE-inspired AI trading terminal with live-style charts, research panels, portfolio views, and chat-based trade previews.`

## What this project shows

- A polished three-panel trading UI inspired by Apple Stocks
- Market cards and watchlist-driven chart views
- Research panels for idea discovery and stock screening
- Portfolio and balance widgets that show how account data is presented
- A chat assistant flow for quotes, portfolio questions, and order previews
- A clear path from conversational intent to trading actions

## Why this public demo exists

The original private workspace contains experimental broker integration code, local notes, and material that should not be published directly.

This demo keeps the product story and interface intact while removing anything sensitive:

- no E*TRADE consumer keys
- no live brokerage connection
- no real account credentials
- no real order placement
- no private `.env` dependency

## Demo behavior

- Portfolio and balance values are sample data for presentation.
- Market prices are seeded demo values with light random drift.
- Research panels are populated with mock showcase data.
- Trade flows stop at preview mode and never reach a broker.
- Chat runs in a lightweight demo mode so the app is easy to open locally.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:8080`.

## Live demo

The public demo is live here:

- [trade-pilot-for-e-trade.vercel.app](https://trade-pilot-for-e-trade.vercel.app)

This repo includes a minimal `vercel.json` for deploying the Flask demo to Vercel.

## Repository positioning

If you want the GitHub page to read well to visitors, use:

- Repo name: `etrade-ai-trading-terminal-demo`
- Short description: `Public demo of an E*TRADE-inspired AI trading terminal with charts, research panels, portfolio views, and chat-based trade previews.`

## Notes

This repository contains only the public-safe demo package. The original private workspace still includes legacy and sensitive material that should remain unpublished.

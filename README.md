# E*TRADE AI Trading Terminal Demo

TradePilot for E*TRADE is an AI-powered trading assistant concept built to make an E*TRADE account AI-active. It shows how a modern broker experience could combine market dashboards, research panels, portfolio visibility, live news awareness, and chat-driven trade workflows in one interface.

The core idea is simple: connect your E*TRADE account, activate an AI trading assistant through the E*TRADE API, and manage analysis, portfolio support, trade planning, and buy or sell workflows through natural conversation.

This repository is the public demo edition of the project. It is designed to showcase that product vision on GitHub without exposing private credentials, real account access, or live order execution.

## About

`AI-powered E*TRADE trading terminal that makes an account AI-active with research, news, portfolio context, and chat-driven trade workflows.`

## What this project shows

- A polished three-panel trading UI inspired by Apple Stocks
- Market cards and watchlist-driven chart views
- Research panels for idea discovery and stock screening
- A product direction where the assistant stays aware of market news and account context
- Portfolio and balance widgets that show how account data is presented
- A chat assistant flow for quotes, portfolio questions, order previews, and AI-guided trade workflows
- A clear path from conversational intent to E*TRADE API-backed actions in the full product

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
- Trade workflows stop at preview mode and never reach a broker in this public build.
- The copy and interaction model are designed to show how the full product would help manage an E*TRADE account through an AI assistant.

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
- Short description: `AI-powered E*TRADE trading terminal that makes an account AI-active with research, news, portfolio context, and chat-driven trade workflows.`

## Notes

This repository contains only the public-safe demo package. The original private workspace still includes legacy and sensitive material that should remain unpublished.

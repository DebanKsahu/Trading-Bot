# Binance Trading Bot

A simple command-line trading bot for Binance Futures using the Python Binance API. The bot supports basic trading operations like placing market orders, limit orders, and viewing account information.

## Features

- Market order execution
- Limit order placement
- Stop-limit order placement
- Account balance viewing
- Testnet support
- CLI interface

## Prerequisites

- Python 3.12+
- Binance Testnet API credentials
- UV package installer (`pip install uv`)

## Installation

1. Clone the repository:
```sh
git clone [your-repository-url]
cd trading-bot
```

2. Install dependencies using UV:
```sh
uv sync
```

3. Set up your environment variables in `.env`:
```env
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
BASE_URL=https://testnet.binancefuture.com
```

## Usage

Run the bot:
```sh
uv run main.py
```

### Available Commands

- `market`: Place a market order
- `limit`: Place a limit order
- `account_info`: View account balances
- `quit`: Exit the bot

### Example Usage

```sh
Enter command: market
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter quantity: 0.001
```

## Safety Notes

- This bot is configured to use Binance's testnet by default
- Always test with small amounts first
- Keep your API keys secure and never share them

## Dependencies

- python-binance >= 1.0.29
- pydantic >= 2.11.7
- pydantic-settings >= 2.10.1
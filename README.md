# Simplified Binance Futures Trading Bot (USDT-M)

A small Python application to place Market and Limit orders on the Binance Futures Testnet (USDT-M).

## Features
- **Place Market/Limit Orders**: Full support for BUY and SELL sides.
- **Enhanced CLI**: Built with `Click` and `Rich` for a premium, interactive user experience.
- **Robust Validation**: Ensures symbols, quantities, and sides are correct before sending requests.
- **Detailed Logging**: All requests, responses, and errors are logged to the `logs/` directory.
- **Testnet Ready**: Uses `https://testnet.binancefuture.com` for safe testing.

## Setup

1. **Python Version**: Ensure you have Python 3.x installed.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **API Credentials**:
   - Register on [Binance Futures Testnet](https://testnet.binancefuture.com).
   - Generate your API Key and Secret.
   - Create a `.env` file in the root directory:
     ```bash
     cp .env.example .env
     ```
   - Add your keys to the `.env` file.

## Usage

The bot now supports subcommands for easier interaction:

### 1. Place an Order
#### Place a Market Buy Order
```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Place a Limit Sell Order
```bash
python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500.5
```

#### Place a Stop-Market Sell Order
```bash
python cli.py order --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --price 60000
```

### 2. Check Account Balance
```bash
python cli.py balance --asset USDT
```

### Options
- `order`: Subcommand to place a trade.
- `balance`: Subcommand to check your account equity.
- `--symbol, -s`: Trading symbol (e.g., BTCUSDT).
- `--side, -d`: BUY or SELL.
- `--type, -t`: MARKET, LIMIT, or STOP_MARKET.
- `--quantity, -q`: Quantity.
- `--price, -p`: Price (Required for LIMIT/STOP_MARKET).

## Project Structure
```
trading_bot/
  bot/
    __init__.py
    client.py        # Binance client wrapper
    orders.py        # Order placement logic
    validators.py    # Input validation
    logging_config.py # Unified logging setup
  cli.py             # CLI entry point
  README.md          # Project documentation
  requirements.txt   # Dependencies
  .env               # API credentials (git-ignored)
  logs/              # Order logs
```

## Logs
All trading activity, including raw API responses, is logged in the `logs/` folder. Check these files for detailed debugging information or confirmation of your trades.

## Assumptions
- Uses USDS-M (USDT Marginated) Futures on Testnet.
- Requires valid API keys with 'Futures' permissions enabled on the testnet account.
- Quantity and price precision must match Binance requirements (e.g., BTCUSDT usually accepts 0.001 precision for quantity).

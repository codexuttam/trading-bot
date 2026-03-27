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

Run the bot using `cli.py`:

### Place a Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a Limit Order
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2500.5
```

### Options
- `--symbol, -s`: Trading symbol (e.g., BTCUSDT).
- `--side, -d`: Order side (BUY/SELL).
- `--type, -t`: Order type (MARKET/LIMIT).
- `--quantity, -q`: Order quantity.
- `--price, -p`: Order price (Required for LIMIT orders).

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

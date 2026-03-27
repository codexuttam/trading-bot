import os
import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_all_inputs
from bot.logging_config import logger

# Initialize Rich console
console = Console()

@click.command()
@click.option('--symbol', '-s', required=True, help='Trading symbol (e.g., BTCUSDT)')
@click.option('--side', '-d', type=click.Choice(['BUY', 'SELL', 'buy', 'sell']), required=True, help='Order side (BUY/SELL)')
@click.option('--type', '-t', 'order_type', type=click.Choice(['MARKET', 'LIMIT', 'market', 'limit']), required=True, help='Order type (MARKET/LIMIT)')
@click.option('--quantity', '-q', type=float, required=True, help='Order quantity')
@click.option('--price', '-p', type=float, help='Order price (required for LIMIT)')
def main(symbol, side, order_type, quantity, price):
    """Simplified Binance Futures Trading Bot CLI."""
    
    # Load API keys from environment
    load_dotenv()
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        console.print("[bold red]Error:[/] API credentials (BINANCE_API_KEY/BINANCE_API_SECRET) not found in .env file.", style="red")
        sys.exit(1)

    # 1. Input Validation
    if not validate_all_inputs(symbol.upper(), side.upper(), order_type.upper(), quantity, price):
        console.print(Panel("[bold red]Validation Failed![/]\nPlease check your inputs.", title="Error", border_style="red"))
        sys.exit(1)

    # 2. Display Order Summary Before Sending
    table = Table(title="Order Summary", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="dim", width=12)
    table.add_column("Value")
    table.add_row("Symbol", symbol.upper())
    table.add_row("Side", side.upper())
    table.add_row("Type", order_type.upper())
    table.add_row("Quantity", str(quantity))
    if order_type.upper() == 'LIMIT':
        table.add_row("Price", str(price))
    console.print(table)

    # 3. Connection and Execution
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        try:
            progress.add_task(description="Connecting to Binance Futures Testnet...", total=None)
            client_wrapper = BinanceFuturesClient(api_key, api_secret, testnet=True)
            bot_client = client_wrapper.get_client()
            order_manager = OrderManager(bot_client)

            progress.add_task(description=f"Placing {order_type.upper()} {side.upper()} order...", total=None)
            response = order_manager.place_order(symbol.upper(), side.upper(), order_type.upper(), quantity, price)

            # 4. Display Success Result
            success_panel = Panel(
                f"[bold green]Order Placed Successfully![/]\n\n"
                f"Order ID: [cyan]{response.get('orderId')}[/]\n"
                f"Status: [yellow]{response.get('status')}[/]\n"
                f"Executed Qty: {response.get('executedQty')}\n"
                f"Avg Price: {response.get('avgPrice', '0.0')}",
                title="Success",
                border_style="green"
            )
            console.print(success_panel)

        except Exception as e:
            error_panel = Panel(
                f"[bold red]Order Failed![/]\n\n"
                f"Error: {e}",
                title="Failure",
                border_style="red"
            )
            console.print(error_panel)
            sys.exit(1)

if __name__ == '__main__':
    main()

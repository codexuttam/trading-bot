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

@click.group()
def cli():
    """Enhanced Binance Futures Trading Bot CLI."""
    load_dotenv()

def get_bot_tools():
    """Helper to initialize client and order manager."""
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        console.print("[bold red]Error:[/] API credentials not found in .env file.", style="red")
        sys.exit(1)

    try:
        client_wrapper = BinanceFuturesClient(api_key, api_secret, testnet=True)
        bot_client = client_wrapper.get_client()
        return OrderManager(bot_client)
    except Exception as e:
        console.print(f"[bold red]Initialization Failed:[/] {e}")
        sys.exit(1)

@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading symbol (e.g., BTCUSDT)')
@click.option('--side', '-d', type=click.Choice(['BUY', 'SELL', 'buy', 'sell']), required=True, help='Order side (BUY/SELL)')
@click.option('--type', '-t', 'order_type', type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET', 'market', 'limit', 'stop_market']), required=True, help='Order type')
@click.option('--quantity', '-q', type=float, required=True, help='Order quantity')
@click.option('--price', '-p', type=float, help='Price (Required for LIMIT/STOP_MARKET)')
def order(symbol, side, order_type, quantity, price):
    """Place a new order on Binance Futures."""
    
    # 1. Validation
    if not validate_all_inputs(symbol.upper(), side.upper(), order_type.upper(), quantity, price):
        console.print(Panel("[bold red]Validation Failed![/]\nPlease check your inputs.", title="Error", border_style="red"))
        sys.exit(1)

    # 2. Display Order Summary
    table = Table(title="Order Preview", show_header=True, header_style="bold cyan")
    table.add_column("Field", style="dim")
    table.add_column("Value")
    table.add_row("Symbol", symbol.upper())
    table.add_row("Side", side.upper())
    table.add_row("Type", order_type.upper())
    table.add_row("Quantity", str(quantity))
    if price:
        table.add_row("Price/Stop", str(price))
    console.print(table)

    # 3. Execution
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        try:
            order_manager = get_bot_tools()
            progress.add_task(description=f"Placing {order_type.upper()} order...", total=None)
            response = order_manager.place_order(symbol.upper(), side.upper(), order_type.upper(), quantity, price)

            success_panel = Panel(
                f"[bold green]Success![/]\n"
                f"ID: [cyan]{response.get('orderId')}[/]\n"
                f"Status: [yellow]{response.get('status')}[/]\n"
                f"Avg Price: {response.get('avgPrice', '0.0')}",
                border_style="green"
            )
            console.print(success_panel)
        except Exception as e:
            console.print(Panel(f"[bold red]Execution Error:[/] {e}", border_style="red"))

@cli.command()
@click.option('--asset', '-a', default='USDT', help='Asset to check balance for')
def balance(asset):
    """Check Binance Futures account balance."""
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        try:
            order_manager = get_bot_tools()
            progress.add_task(description=f"Fetching {asset} balance...", total=None)
            data = order_manager.get_account_balance(asset.upper())
            
            if data:
                table = Table(title=f"Balance: {asset.upper()}", show_header=True, header_style="bold green")
                table.add_column("Metric")
                table.add_column("Value")
                table.add_row("Total Wallet Balance", data.get('balance', '0'))
                table.add_row("Withdrawal Available", data.get('availableBalance', '0'))
                table.add_row("Unrealized PNL", data.get('crossUnPnl', '0'))
                console.print(table)
            else:
                console.print(f"[yellow]No balance info found for {asset.upper()}.[/]")
        except Exception as e:
            console.print(Panel(f"[bold red]Balance Fetch Error:[/] {e}", border_style="red"))

if __name__ == '__main__':
    cli()

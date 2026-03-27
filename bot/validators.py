import re
from typing import Optional, Union, Any
from bot.logging_config import logger

def validate_symbol(symbol: str) -> bool:
    """Validate symbol format (e.g., BTCUSDT)."""
    if not symbol:
        return False
    # Typical Binance symbols are upper case strings
    return bool(re.match(r'^[A-Z0-9]{3,12}$', symbol))

def validate_side(side: str) -> bool:
    """Validate side (BUY/SELL)."""
    return side.upper() in ["BUY", "SELL"]

def validate_order_type(order_type: str) -> bool:
    """Validate order type (MARKET/LIMIT/STOP_MARKET)."""
    return order_type.upper() in ["MARKET", "LIMIT", "STOP_MARKET"]

def validate_quantity(quantity: Union[str, float, int]) -> bool:
    """Validate quantity - must be positive."""
    try:
        qty = float(quantity)
        return qty > 0
    except ValueError:
        return False

def validate_price(price: Optional[Union[str, float, int]], order_type: str) -> bool:
    """Validate price - required and positive for LIMIT and STOP_MARKET orders."""
    if order_type.upper() in ["LIMIT", "STOP_MARKET"]:
        if price is None:
            return False
        try:
            p = float(price)
            return p > 0
        except ValueError:
            return False
    return True

def validate_all_inputs(symbol: str, side: str, order_type: str, quantity: Any, price: Optional[Any] = None) -> bool:
    """Check all inputs for validity."""
    if not validate_symbol(symbol):
        logger.error(f"Invalid symbol: {symbol}")
        return False
    if not validate_side(side):
        logger.error(f"Invalid side: {side}")
        return False
    if not validate_order_type(order_type):
        logger.error(f"Invalid order type: {order_type}")
        return False
    if not validate_quantity(quantity):
        logger.error(f"Invalid quantity: {quantity}")
        return False
    if not validate_price(price, order_type):
        logger.error(f"Invalid price (required and positive for LIMIT): {price}")
        return False
    return True

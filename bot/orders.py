import json
from binance.exceptions import BinanceAPIException
from bot.logging_config import logger

class OrderManager:
    """Manages order placement logic on Binance Futures."""

    def __init__(self, client):
        """
        Initialize the Order Manager.
        
        :param client: An initialized Binance Client.
        """
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """
        Place a Market or Limit order.
        
        :param symbol: Symbol (e.g., BTCUSDT)
        :param side: BUY/SELL
        :param order_type: MARKET/LIMIT
        :param quantity: Quantity to buy/sell
        :param price: Required if LIMIT order
        """
        try:
            # Side should be in uppercase
            side = side.upper()
            order_type = order_type.upper()
            
            logger.info(f"Placing {order_type} {side} order for {quantity} {symbol} (Price: {price})...")
            
            # Use futures_create_order for USDT-M Futures
            if order_type == "MARKET":
                response = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == "LIMIT":
                if price is None:
                    raise ValueError("Price is required for LIMIT orders.")
                response = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce="GTC",  # Good-Till-Canceled
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            # Summarize result
            order_id = response.get('orderId')
            status = response.get('status')
            executed_qty = response.get('executedQty')
            avg_price = response.get('avgPrice', '0.0')

            logger.info(f"Order Placed Successfully! ID: {order_id}, Status: {status}, ExecQty: {executed_qty}, AvgPrice: {avg_price}")
            
            # Optionally log JSON for record keeping
            logger.debug(f"Full response: {json.dumps(response, indent=2)}")
            
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: Code: {e.code}, Message: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected Error during order placement: {e}")
            raise e

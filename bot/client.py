import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import logger
from dotenv import load_dotenv

load_dotenv()

class BinanceFuturesClient:
    """Wrapper for Binance Futures Testnet client."""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the Binance Futures client.
        
        :param api_key: Binance API Key
        :param api_secret: Binance API Secret
        :param testnet: Use Testnet (default True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize and return the Binance Client."""
        try:
            client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            # Ensure the client is using the futures testnet URL
            if self.testnet:
                client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi/v1'
                client.FUTURES_DATA_URL = 'https://testnet.binancefuture.com/fapi/v1'
            
            # Verify connectivity (Optional, e.g., get server time)
            server_time = client.futures_time()
            logger.info(f"Successfully connected to Binance Futures {'Testnet' if self.testnet else 'Mainnet'}.")
            return client
        except BinanceAPIException as e:
            logger.error(f"Error connecting to Binance: {e}")
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred during client initialization: {e}")
            raise e

    def get_client(self):
        """Returns the inner Client instance."""
        return self.client

import logging
from typing import Literal

from binance.async_client import AsyncClient, BinanceAPIException
from pydantic import validate_call


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='trading_bot.log')

class BasicBot():

    @validate_call
    def __init__(self, api_key: str, secret_key: str, testnet: bool = True):
        self.api_key = api_key
        self.secret_key = secret_key
        self.testnet = testnet

    async def run(self):
        try:
            self.client = await AsyncClient().create(
                api_key=self.api_key,
                api_secret=self.secret_key,
                testnet=self.testnet
            )

            await self.client.get_account()
            logging.info("Successfully connected to Binance Futures Testnet.")
        except* BinanceAPIException as e:
            logging.error(f"Failed to connect to Binance API: {e}")
        except* Exception as e:
            logging.error(f"An unexpected error occurred during initialization: {e}")

    @validate_call
    async def place_market_order(self, symbol: str, side: Literal["BUY", "SELL"], quantity: float):
        try:
            await self.run()
            logging.info(f"Attempting to place a MARKET {side} order for {quantity} {symbol}...")
            order = await self.client.order_market_buy(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity,
            )

            logging.info("Successfully placed market order.")
            print("--- Order Details ---")
            print(f"  Symbol: {order['symbol']}")
            print(f"  Order ID: {order['orderId']}")
            print(f"  Side: {order['side']}")
            print(f"  Type: {order['type']}")
            print(f"  Status: {order['status']}")
            print("---------------------")
            return order
        
        except BinanceAPIException as e:
            logging.error(f"API Error placing market order: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred placing market order: {e}")
            return None
        finally:
            await self.close_connection()

    @validate_call
    async def place_limit_order(self, symbol: str, side: Literal["BUY", "SELL"], quantity: float, price: float):

        try:
            await self.run()
            logging.info(f"Attempting to place a LIMIT {side} order for {quantity} {symbol} at price {price}...")
            
            order = await self.client.order_market_buy(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'
            )
            
            logging.info("Successfully placed limit order.")
            print("--- Order Details ---")
            print(f"  Symbol: {order['symbol']}")
            print(f"  Order ID: {order['orderId']}")
            print(f"  Side: {order['side']}")
            print(f"  Type: {order['type']}")
            print(f"  Price: {order['price']}")
            print(f"  Status: {order['status']}")
            print("---------------------")
            return order

        except BinanceAPIException as e:
            logging.error(f"API Error placing limit order: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred placing limit order: {e}")
            return None
        finally:
            await self.close_connection()

    @validate_call  
    async def place_stop_limit_order(self, symbol: str, side: Literal["BUY", "SELL"], quantity: float, price: float, stop_price: float):
            
        try:
            await self.run()
            logging.info(f"Attempting to place a STOP-LIMIT {side} order for {quantity} {symbol} with stop price {stop_price} and limit price {price}...")

            order = await self.client.order_market_buy(
                symbol=symbol,
                side=side,
                type='STOP_LIMIT',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce='GTC'
            )
            
            logging.info("Successfully placed stop-limit order.")
            print("--- Order Details ---")
            print(f"  Symbol: {order['symbol']}")
            print(f"  Order ID: {order['orderId']}")
            print(f"  Side: {order['side']}")
            print(f"  Type: {order['type']}")
            print(f"  Limit Price: {order['price']}")
            print(f"  Stop Price: {order['stopPrice']}")
            print(f"  Status: {order['status']}")
            print("---------------------")
            return order

        except BinanceAPIException as e:
            logging.error(f"API Error placing stop-limit order: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred placing stop-limit order: {e}")
            return None
        finally:
            await self.close_connection()
        
    async def close_connection(self):
        await self.client.close_connection()

    async def display_account_info(self):
        try:
            await self.run()
            logging.info("Fetching account information...")
            account_info = await self.client.get_account()
            
            print("\n--- Spot Account Balances ---")
            balances = account_info['balances']
            
            for asset in balances:
                free_balance = float(asset['free'])
                locked_balance = float(asset['locked'])
                
                if free_balance > 0 or locked_balance > 0:
                    print(f"  - Asset: {asset['asset']:<6} | Available: {free_balance:<15} | In Orders: {locked_balance}")
            
            print("-----------------------------")
            logging.info("Successfully fetched and displayed account info.")

        except BinanceAPIException as e:
            logging.error(f"API Error fetching account info: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred fetching account info: {e}")
        finally:
            await self.close_connection()
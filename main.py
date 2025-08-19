import asyncio

from bot_class import BasicBot
from config import settings


async def run_cli(bot: BasicBot):
    print("--- Simplified Trading Bot CLI ---")
    print("Commands: market, limit, quit, account_info")

    while True:
        command = input("\nEnter command: ").lower()
        
        if command == "quit":
            print("Exiting bot.")
            break
        elif command == "account_info":
            await bot.display_account_info()
            
        elif command in ("market", "limit"):
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            
            while True:
                side = input("Enter side (BUY/SELL): ").upper()
                if side in ('BUY', 'SELL'):
                    break
                print("Invalid side. Please enter 'buy' or 'sell'.")
            
            while True:
                try:
                    quantity = float(input("Enter quantity: "))
                    break
                except ValueError:
                    print("Invalid quantity. Please enter a number.")
            
            if command == 'market':
                await bot.place_market_order(symbol, side, quantity)
            
            elif command == 'limit':
                while True:
                    try:
                        price = float(input("Enter limit price: "))
                        break
                    except ValueError:
                        print("Invalid price. Please enter a number.")
                await bot.place_limit_order(symbol, side, quantity, price)
        
        else:
            print("Unknown command. Please use 'market', 'limit', or 'quit'.")
    await bot.close_connection()

async def main():
    if settings.BINANCE_API_KEY == "YOUR_TESTNET_API_KEY" or settings.BINANCE_SECRET_KEY == "YOUR_TESTNET_API_SECRET":
        print("Please replace 'YOUR_TESTNET_API_KEY' and 'YOUR_TESTNET_API_SECRET' with your actual testnet credentials.")
    else:
        try:
            bot = BasicBot(api_key=settings.BINANCE_API_KEY, secret_key=settings.BINANCE_SECRET_KEY)
            await run_cli(bot)
        except Exception as e:
            print(f"Failed to start the bot. Please check your API credentials and connection. Error = {e}")

if __name__ == '__main__':
    asyncio.run(main())

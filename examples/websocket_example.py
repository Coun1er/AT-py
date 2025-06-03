import asyncio
import logging
from axiomtradeapi.websocket._client import AxiomTradeWebSocketClient

async def handle_new_tokens(tokens):
    """Handle new token updates."""
    for token in tokens:
        print(f"\nNew Token Detected:")
        print(f"Name: {token['tokenName']} ({token['tokenTicker']})")
        print(f"Address: {token['tokenAddress']}")
        print(f"Protocol: {token['protocol']}")
        print(f"Market Cap: {token['marketCapSol']} SOL")
        print(f"Volume: {token['volumeSol']} SOL")
        if token['website']:
            print(f"Website: {token['website']}")
        if token['twitter']:
            print(f"Twitter: {token['twitter']}")
        if token['telegram']:
            print(f"Telegram: {token['telegram']}")
        print("-" * 50)

async def main():
    # Initialize client with debug logging
    client = AxiomTradeWebSocketClient(log_level=logging.DEBUG)
    
    # Subscribe to new token updates
    await client.subscribe_new_tokens(handle_new_tokens)
    
    # Start listening for updates
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from axiomtradeapi import AxiomTradeClient
import logging

async def handle_tokens(tokens):
    for token in tokens:
        print(f"New token: {token['tokenName']}")

async def main():
    client = AxiomTradeClient(
        log_level=logging.DEBUG
    )
    await client.GetTokenPrice("8ScCaba6Uix9eDh6Jv2PyNfKMWa6iMBC1weU6Zaqj3SL")
    await client.ws.start()

asyncio.run(main())
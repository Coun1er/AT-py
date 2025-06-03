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
    await client.subscribe_new_tokens(handle_tokens)
    await client.ws.start()

asyncio.run(main())
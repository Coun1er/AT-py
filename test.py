import asyncio
from axiomtradeapi import AxiomTradeClient
import logging
import dotenv
import os

dotenv.load_dotenv()

async def handle_tokens(tokens):
    print(tokens)

async def main():
    client = AxiomTradeClient(
        log_level=logging.DEBUG,
        auth_token=os.getenv("auth_access_token"),
        refresh_token=os.getenv("auth_refresh_token")
    )
    await client.subscribe_new_tokens(handle_tokens)
    await client.ws.start()

asyncio.run(main())
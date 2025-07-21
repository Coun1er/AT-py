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
        username=os.getenv("email"),
        password=os.getenv("password"),
    )
    client.complete_login(
        email=os.getenv("email"),
        b64_password=os.getenv("password")
    )
    await client.subscribe_new_tokens(handle_tokens)
    await client.ws.start()

asyncio.run(main())
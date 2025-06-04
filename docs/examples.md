---
layout: page
title: "Code Examples - AxiomTradeAPI"
description: "Complete collection of code examples for AxiomTradeAPI-py including trading bots, WebSocket integration, and portfolio management."
---

# AxiomTradeAPI Code Examples

## Quick Start Examples

### Basic Setup and Balance Query

```python
from axiomtradeapi import AxiomClient

# Initialize client
client = AxiomClient()

# Get wallet balance
wallet_address = "YOUR_SOLANA_WALLET_ADDRESS"
balance = client.get_balance(wallet_address)

print(f"SOL Balance: {balance['sol']}")
print(f"Token Count: {len(balance['tokens'])}")
```

### WebSocket Real-Time Monitoring

```python
from axiomtradeapi import AxiomWebSocket
import asyncio

class TokenMonitor:
    def __init__(self):
        self.ws = AxiomWebSocket()
    
    async def start_monitoring(self):
        await self.ws.connect()
        
        # Subscribe to new token events
        await self.ws.subscribe('new_tokens', self.on_new_token)
        
        # Keep connection alive
        await self.ws.listen_forever()
    
    def on_new_token(self, data):
        print(f"🚀 New token detected: {data['name']}")
        print(f"Contract: {data['contract_address']}")
        print(f"Initial Price: ${data['price']}")

# Run the monitor
monitor = TokenMonitor()
asyncio.run(monitor.start_monitoring())
```

### Simple Trading Bot

```python
from axiomtradeapi import AxiomClient
import time

class SimpleBot:
    def __init__(self, wallet_address):
        self.client = AxiomClient()
        self.wallet = wallet_address
        self.running = True
    
    def check_balance_and_trade(self):
        balance = self.client.get_balance(self.wallet)
        
        if balance['sol'] > 1.0:  # If we have more than 1 SOL
            print("💰 Sufficient balance for trading")
            # Add your trading logic here
            
    def run(self):
        while self.running:
            try:
                self.check_balance_and_trade()
                time.sleep(30)  # Check every 30 seconds
            except KeyboardInterrupt:
                print("🛑 Bot stopped by user")
                self.running = False
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)  # Wait longer on error

# Initialize and run bot
bot = SimpleBot("YOUR_WALLET_ADDRESS")
bot.run()
```

## Advanced Examples

### Portfolio Tracking Bot

```python
from axiomtradeapi import AxiomClient
from datetime import datetime
import json

class PortfolioTracker:
    def __init__(self, wallets):
        self.client = AxiomClient()
        self.wallets = wallets
        self.history = []
    
    def track_portfolio(self):
        total_value = 0
        portfolio_data = {
            'timestamp': datetime.now().isoformat(),
            'wallets': {}
        }
        
        for wallet in self.wallets:
            balance = self.client.get_balance(wallet)
            wallet_value = self.calculate_wallet_value(balance)
            
            portfolio_data['wallets'][wallet] = {
                'balance': balance,
                'usd_value': wallet_value
            }
            
            total_value += wallet_value
        
        portfolio_data['total_usd_value'] = total_value
        self.history.append(portfolio_data)
        
        return portfolio_data
    
    def calculate_wallet_value(self, balance):
        # Simplified calculation - in real implementation,
        # you'd fetch current token prices
        sol_price = 150  # Example SOL price
        return balance['sol'] * sol_price
    
    def save_history(self, filename='portfolio_history.json'):
        with open(filename, 'w') as f:
            json.dump(self.history, f, indent=2)

# Usage
wallets = ["WALLET_1", "WALLET_2", "WALLET_3"]
tracker = PortfolioTracker(wallets)

# Track portfolio
data = tracker.track_portfolio()
print(f"Total Portfolio Value: ${data['total_usd_value']:,.2f}")

# Save history
tracker.save_history()
```

### Arbitrage Detection Bot

```python
from axiomtradeapi import AxiomClient, AxiomWebSocket
import asyncio
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ArbitrageOpportunity:
    token: str
    buy_price: float
    sell_price: float
    profit_margin: float
    buy_exchange: str
    sell_exchange: str

class ArbitrageBot:
    def __init__(self):
        self.client = AxiomClient()
        self.ws = AxiomWebSocket()
        self.price_data: Dict[str, Dict] = {}
        self.min_profit_margin = 0.02  # 2% minimum profit
    
    async def start_monitoring(self):
        await self.ws.connect()
        
        # Subscribe to price updates from multiple exchanges
        await self.ws.subscribe('price_updates', self.on_price_update)
        
        # Start arbitrage detection loop
        asyncio.create_task(self.detect_arbitrage())
        
        await self.ws.listen_forever()
    
    def on_price_update(self, data):
        token = data['token']
        exchange = data['exchange']
        price = data['price']
        
        if token not in self.price_data:
            self.price_data[token] = {}
        
        self.price_data[token][exchange] = {
            'price': price,
            'timestamp': data['timestamp']
        }
    
    async def detect_arbitrage(self):
        while True:
            opportunities = self.find_arbitrage_opportunities()
            
            for opportunity in opportunities:
                await self.execute_arbitrage(opportunity)
            
            await asyncio.sleep(1)  # Check every second
    
    def find_arbitrage_opportunities(self) -> List[ArbitrageOpportunity]:
        opportunities = []
        
        for token, exchanges in self.price_data.items():
            if len(exchanges) < 2:
                continue
            
            prices = [(exchange, data['price']) for exchange, data in exchanges.items()]
            prices.sort(key=lambda x: x[1])  # Sort by price
            
            # Check for arbitrage between lowest and highest price
            if len(prices) >= 2:
                buy_exchange, buy_price = prices[0]
                sell_exchange, sell_price = prices[-1]
                
                profit_margin = (sell_price - buy_price) / buy_price
                
                if profit_margin > self.min_profit_margin:
                    opportunities.append(ArbitrageOpportunity(
                        token=token,
                        buy_price=buy_price,
                        sell_price=sell_price,
                        profit_margin=profit_margin,
                        buy_exchange=buy_exchange,
                        sell_exchange=sell_exchange
                    ))
        
        return opportunities
    
    async def execute_arbitrage(self, opportunity: ArbitrageOpportunity):
        print(f"🎯 Arbitrage opportunity found!")
        print(f"Token: {opportunity.token}")
        print(f"Buy at {opportunity.buy_exchange}: ${opportunity.buy_price:.4f}")
        print(f"Sell at {opportunity.sell_exchange}: ${opportunity.sell_price:.4f}")
        print(f"Profit margin: {opportunity.profit_margin:.2%}")
        
        # In a real implementation, you would execute the trades here
        # This is just for demonstration purposes

# Run the arbitrage bot
bot = ArbitrageBot()
asyncio.run(bot.start_monitoring())
```

## Integration Examples

### Discord Bot Integration

```python
import discord
from discord.ext import commands
from axiomtradeapi import AxiomClient

class TradingBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.axiom = AxiomClient()
    
    @commands.command(name='balance')
    async def check_balance(self, ctx, wallet_address: str):
        """Check wallet balance"""
        try:
            balance = self.axiom.get_balance(wallet_address)
            
            embed = discord.Embed(
                title="💰 Wallet Balance",
                color=0x00ff00
            )
            embed.add_field(
                name="SOL Balance",
                value=f"{balance['sol']:.4f} SOL",
                inline=False
            )
            
            if balance['tokens']:
                token_list = []
                for token, amount in balance['tokens'].items():
                    token_list.append(f"{token}: {amount:,.2f}")
                
                embed.add_field(
                    name="Token Holdings",
                    value="\n".join(token_list[:10]),  # Show first 10 tokens
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error checking balance: {e}")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(TradingBot(bot))

# bot.run('YOUR_DISCORD_BOT_TOKEN')
```

## Error Handling Examples

### Robust Error Handling

```python
from axiomtradeapi import AxiomClient
from axiomtradeapi.exceptions import (
    ValidationError,
    ConnectionError,
    AxiomAPIError,
    RateLimitError
)
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustTradingBot:
    def __init__(self):
        self.client = AxiomClient()
        self.max_retries = 3
        self.retry_delay = 5
    
    def get_balance_with_retry(self, wallet_address):
        """Get balance with automatic retry on errors"""
        for attempt in range(self.max_retries):
            try:
                return self.client.get_balance(wallet_address)
                
            except ValidationError as e:
                logger.error(f"Invalid wallet address: {e}")
                raise  # Don't retry on validation errors
                
            except RateLimitError as e:
                logger.warning(f"Rate limit hit: {e}")
                sleep_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                logger.info(f"Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
                
            except ConnectionError as e:
                logger.warning(f"Connection error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Max retries reached for connection error")
                    raise
                    
            except AxiomAPIError as e:
                logger.error(f"API error: {e}")
                if e.is_retryable():
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    else:
                        raise
                else:
                    raise  # Don't retry on non-retryable errors
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
        
        return None

# Usage
bot = RobustTradingBot()
try:
    balance = bot.get_balance_with_retry("YOUR_WALLET_ADDRESS")
    print(f"Balance retrieved successfully: {balance}")
except Exception as e:
    print(f"Failed to get balance after all retries: {e}")
```

## Support and Resources

- 📚 [Complete Documentation](index.html)
- 🔧 [API Reference](api-reference.html)
- 🤝 [Professional Support at chipa.tech](https://chipa.tech)
- 💬 [Discord Community](https://discord.gg/p7YyFqSmAz)

## Next Steps

1. Try the basic examples above
2. Read the [Installation Guide](installation.html)
3. Learn about [WebSocket Integration](websocket-guide.html)
4. Build your first [Trading Bot](trading-bots.html)
5. Explore [Advanced Features](performance.html)

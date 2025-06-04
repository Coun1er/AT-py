---
layout: api
title: "API Reference - AxiomTradeAPI Methods"
description: "Complete API reference for all AxiomTradeAPI methods including balance queries, WebSocket connections, and trading operations."
endpoint: "/api/v1"
method: "Multiple"
---

# AxiomTradeAPI Complete API Reference

## Core API Methods

### Balance Operations

#### `get_balance(wallet_address)`

Retrieve the balance for a specific Solana wallet address.

**Parameters:**
- `wallet_address` (string, required): The Solana wallet address to query
- `token_type` (string, optional): Filter by specific token type (default: all)

**Returns:**
- `balance` (object): Wallet balance information
- `timestamp` (string): Query timestamp
- `status` (string): Request status

**Example:**
```python
from axiomtradeapi import AxiomClient

client = AxiomClient()
balance = client.get_balance("YOUR_WALLET_ADDRESS")
print(f"SOL Balance: {balance['sol']}")
```

**Response:**
```json
{
  "balance": {
    "sol": 12.5,
    "tokens": {
      "USDC": 1000.0,
      "BONK": 50000000
    }
  },
  "timestamp": "2025-06-04T10:30:00Z",
  "status": "success"
}
```

### WebSocket Operations

#### `connect_websocket(callback=None)`

Establish a WebSocket connection for real-time data streaming.

**Parameters:**
- `callback` (function, optional): Callback function for message handling
- `auto_reconnect` (boolean, optional): Enable automatic reconnection (default: True)
- `max_retries` (integer, optional): Maximum reconnection attempts (default: 5)

**Example:**
```python
def message_handler(data):
    print(f"New token: {data['token_name']}")

client.connect_websocket(callback=message_handler)
```

### Trading Operations

#### `place_order(order_type, amount, price=None)`

Place a trading order on the Axiom Trade platform.

**Parameters:**
- `order_type` (string, required): "buy" or "sell"
- `amount` (float, required): Order amount
- `price` (float, optional): Limit price (market order if not specified)

**Returns:**
- `order_id` (string): Unique order identifier
- `status` (string): Order status
- `executed_at` (string): Execution timestamp

## Error Handling

All API methods include comprehensive error handling:

```python
try:
    balance = client.get_balance("invalid_address")
except ValidationError as e:
    print(f"Invalid address: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except AxiomAPIError as e:
    print(f"API error: {e}")
```

## Rate Limits

- **Balance queries**: 100 requests per minute
- **WebSocket connections**: 5 concurrent connections
- **Trading operations**: 50 requests per minute

## Authentication

Most operations require API authentication. See the [Authentication Guide](authentication.html) for setup instructions.

## Support

For technical support and advanced features, visit [chipa.tech](https://chipa.tech) or join our [Discord community](https://discord.gg/p7YyFqSmAz).

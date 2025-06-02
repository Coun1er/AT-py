from axiomtradeapi import AxiomTradeClient
import logging

# Initialize client with debug logging
client = AxiomTradeClient(log_level=logging.DEBUG)

# Test single wallet balance
wallet_address = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
balance = client.GetBalance(wallet_address)
print(f"\nSingle wallet balance: {balance}")

# Test multiple wallet balances
wallet_addresses = [
    "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh",
    "Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb"
]
balances = client.GetBatchedBalance(wallet_addresses)
print(f"\nBatched wallet balances: {balances}")
from axiomtradeapi import AxiomTradeClient

# test to get balance
client = AxiomTradeClient()
wallet_address = "Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb"
balance = client.GetBalance(wallet_address)
print(balance)
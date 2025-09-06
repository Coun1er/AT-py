from axiomtradeapi.client import AxiomTradeClient
import dotenv
import os
import time

dotenv.load_dotenv()
access_token = os.getenv('auth-access-token')
refresh_token = os.getenv('auth-refresh-token')
private_key = os.getenv('PRIVATE_KEY')
client = AxiomTradeClient(
    auth_token=access_token,
    refresh_token=refresh_token
)

# Example token mint address (replace with actual token you want to trade)
token_mint = "9SkhnfNU5kx3VhngR9F2X7YSKnRZsNxGzcipHoCNGakK"

print("🚀 Testing Buy and Sell Functions")
print("=" * 50)

print(f"\n💰 Testing Buy: 0.001 SOL worth of {token_mint}")
buy_result = client.buy_token(
    private_key=private_key,
    token_mint=token_mint, 
    amount=0.001,  # Amount in SOL
    slippage_percent=10,  # PumpPortal expects integer
    priority_fee=0.005,
    pool="auto",
    denominated_in_sol=True  # True means amount is in SOL
)

print(f"Buy result: {buy_result}")

if buy_result["success"]:
    print(f"✅ Buy successful! Transaction: {buy_result['signature']}")
    print(f"🔗 Explorer: {buy_result.get('explorer_url', 'N/A')}")
else:
    print(f"❌ Buy failed: {buy_result['error']}")

print("\nWaiting 2 seconds...")
time.sleep(2)

print(f"\n💸 Testing Sell: 100 tokens of {token_mint}")
sell_result = client.sell_token(
    private_key=private_key,
    token_mint=token_mint,
    amount=100,  # Number of tokens to sell
    slippage_percent=10,  # PumpPortal expects integer
    priority_fee=0.005,
    pool="auto",
    denominated_in_sol=False  # False means amount is in tokens
)

print(f"Sell result: {sell_result}")

if sell_result["success"]:
    print(f"✅ Sell successful! Transaction: {sell_result['signature']}")
    print(f"🔗 Explorer: {sell_result.get('explorer_url', 'N/A')}")
else:
    print(f"❌ Sell failed: {sell_result['error']}")

print("\n🎉 Buy and Sell test completed!")

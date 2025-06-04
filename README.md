[docs](https://chipadevteam.github.io/AxiomTradeAPI-py) <br>
👉 [Join us on Discord](https://discord.gg/p7YyFqSmAz) <br>
if you are looking to build a bot, let us build it for you! check [Our shop](https://chipa.tech/shop/)
# AxiomTradeAPI-py

A Python wrapper for the [Axiom Trade](https://axiom.trade/@chipa) API. Easily interact with Axiom Trade's trading features using Python.

## 📌 Features
- Access market data  
- Place and manage trades  
- Retrieve account details  
- Comprehensive logging support
- More features coming soon!  

## 🚀 Installation
```bash
pip install axiomtradeapi
```

## 🔧 Usage
```python
import logging
from axiomtradeapi import AxiomTradeClient

# Initialize client with debug logging
client = AxiomTradeClient(log_level=logging.DEBUG)

# Get account balance
balance = client.get_balance()
print(balance)

# Or use default INFO level logging
client = AxiomTradeClient()  # Uses logging.INFO by default
balance = client.get_balance()
print(balance)
```

## 💡 Support Us
If you find this project useful, consider supporting us by signing up with our affiliate link:  
👉 [Axiom Trade Affiliate](https://axiom.trade/@chipa)  

## 🐜 License
This project is licensed under the MIT License.

## 📩 Contact
For questions or suggestions, feel free to open an issue or reach out!


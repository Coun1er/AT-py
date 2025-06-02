from axiomtradeapi.content.endpoints import Endpoints
from axiomtradeapi.helpers.help import Helping
import requests
import logging
import json
from typing import List, Dict, Union

class AxiomTradeClient:
    def __init__(self, log_level=logging.INFO) -> None:
        self.endpoints = Endpoints()
        self.base_url_api = self.endpoints.BASE_URL_API
        self.helper = Helping()
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json, text/plain, */*",
            "origin": "https://axiom.trade",
            "referer": "https://axiom.trade/discover"
        }
        
        # Setup logging
        self.logger = logging.getLogger("AxiomTradeAPI")
        self.logger.setLevel(log_level)
        
        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def GetBalance(self, wallet_address: str) -> Dict[str, Union[float, int]]:
        """Get balance for a single wallet address."""
        return self.GetBatchedBalance([wallet_address])[wallet_address]
            
    def GetBatchedBalance(self, wallet_addresses: List[str]) -> Dict[str, Dict[str, Union[float, int]]]:
        """Get balances for multiple wallet addresses in a single request."""
        try:
            payload = {
                "publicKeys": wallet_addresses
            }
            
            self.logger.debug(f"Sending batched balance request for wallets: {wallet_addresses}")
            self.logger.debug(f"Request payload: {json.dumps(payload)}")
            
            url = f"{self.base_url_api}{self.endpoints.ENDPOINT_GET_BATCHED_BALANCE}"
            self.logger.debug(f"Request URL: {url}")
            
            response = requests.post(url, headers=self.headers, json=payload)
            self.logger.debug(f"Response status code: {response.status_code}")

            if response.status_code == 200:
                response_data = response.json()
                self.logger.debug(f"Response data: {json.dumps(response_data)}")
                
                result = {}
                for address in wallet_addresses:
                    if address in response_data:
                        balance_data = response_data[address]
                        sol = balance_data["solBalance"]
                        lamports = int(sol * 1_000_000_000)  # Convert SOL back to lamports
                        
                        result[address] = {
                            "sol": sol,
                            "lamports": lamports,
                            "slot": balance_data["slot"]
                        }
                        self.logger.info(f"Successfully retrieved balance for {address}: {sol} SOL")
                    else:
                        self.logger.warning(f"No balance data received for address: {address}")
                        result[address] = None
                
                return result
            else:
                error_msg = f"Error: {response.status_code}"
                self.logger.error(error_msg)
                return {addr: None for addr in wallet_addresses}
                
        except requests.exceptions.RequestException as err:
            error_msg = f"An error occurred: {err}"
            self.logger.error(error_msg)
            return {addr: None for addr in wallet_addresses}


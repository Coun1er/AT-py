from axiomtradeapi.content.endpoints import Endpoints
from axiomtradeapi.helpers.help import Helping
import requests

class AxiomTradeClient:
    def __init__(self) -> None:
        self.endpoints = Endpoints()
        self.base_url_api = self.endpoints.BASE_URL_API
        self.helper = Helping()
        self.headers = {"Content-Type": "application/json"}
    def GetBalance(self, wallet_address: str):
        try:
            payload = {
                "jsonrpc":"2.0",
                "id":1,
                "method":"getBalance",
                "params":
                [
                    f"{wallet_address}",
                    {
                        "commitment":"confirmed"
                    }
                ]
            }
            response = requests.post(f"{self.base_url_api}{self.endpoints.ENDPOINT_GET_BALANCE}", headers=self.headers, json=payload)

            if response.status_code == 200:
                lamports = response.json()["result"]['value']
                sol = self.helper.lamports_to_sol(lamports)
                return {
                    "sol": sol,
                    "lamports": lamports,
                }

            else:
                print(f"Error: {response.status_code}")
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            return f"An error occurred: {err}"

        
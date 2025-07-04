from axiomtradeapi._client import AxiomTradeClient
from axiomtradeapi.client import AxiomTradeClient as NewAxiomTradeClient, quick_login_and_get_trending, get_trending_with_token
from axiomtradeapi.auth.login import AxiomAuth

__all__ = ['AxiomTradeClient', 'NewAxiomTradeClient', 'AxiomAuth', 'quick_login_and_get_trending', 'get_trending_with_token']
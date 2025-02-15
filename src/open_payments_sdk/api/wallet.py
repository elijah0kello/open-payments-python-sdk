import json
import urllib.parse

from open_payments_sdk.http import Client as HttpClient
from open_payments_sdk.configuration import Configuration
from open_payments_sdk.models.wallet import WalletAddress, JsonWebKeySet


class Wallet:
    def __init__(self, wallet_address_server_endpoint: str, http_client: HttpClient = None):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client
        self.wallet_address_server_endpoint = wallet_address_server_endpoint


    def get_wallet_address(self) -> WalletAddress:
        """Get wallet address from address server"""
        response = self.http_client.get(self.wallet_address_server_endpoint)
        return WalletAddress.model_validate(json.loads(response))

    def get_keys(self) -> JsonWebKeySet:
        """Get keys from address server"""
        base_url = self.wallet_address_server_endpoint.rstrip('/')
        url = f'{base_url}/jwks.json'
        response = self.http_client.get(url)
        return JsonWebKeySet.model_validate(json.loads(response))

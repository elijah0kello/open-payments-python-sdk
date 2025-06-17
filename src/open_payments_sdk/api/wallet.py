import json

from open_payments_sdk.configuration import Configuration
from open_payments_sdk.http import HttpClient as HttpClient
from open_payments_sdk.models.wallet import JsonWebKeySet, WalletAddress


class Wallet:
    """
    Class for handling Wallet resource
    """
    def __init__(
        self, http_client: HttpClient = None
    ):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client

    def get_wallet_address(self, wallet_address_server_endpoint: str) -> WalletAddress:
        """Get wallet address from address server"""
        response = self.http_client.get(wallet_address_server_endpoint)
        return WalletAddress.model_validate(json.loads(response))

    def get_keys(self, wallet_address_server_endpoint: str) -> JsonWebKeySet:
        """Get keys from address server"""
        base_url = wallet_address_server_endpoint.rstrip("/")
        url = f"{base_url}/jwks.json"
        response = self.http_client.get(url)
        return JsonWebKeySet.model_validate(json.loads(response))

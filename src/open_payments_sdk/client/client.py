"""
Open Payments API Client Module
"""

from open_payments_sdk.api.auth import AccessTokens, Grants
from open_payments_sdk.api.resource import IncomingPayments, OutgoingPayments, Quotes
from open_payments_sdk.api.wallet import Wallet
from open_payments_sdk.http import HttpClient


class OpenPayemntsClient:
    """
    Open Payments API Client
    """
    def __init__(self, keyid: str, private_key: str, http_client: HttpClient = None):
        if not http_client :
            self.http_client = HttpClient()
        self.keyid = keyid
        self.private_key = private_key
        self.http_client = http_client
        self.grants = Grants(
            keyid=keyid, 
            private_key=private_key,
            http_client=self.http_client
        )
        self.access_tokens = AccessTokens(
            keyid=keyid,
            private_key=private_key,
            http_client=self.http_client
        )
        self.wallet = Wallet(self.http_client)
        self.incoming_payments = IncomingPayments(
            keyid=keyid,
            private_key=private_key,
            http_client=self.http_client
        )
        self.outgoing_payments = OutgoingPayments(
            keyid=keyid,
            private_key=private_key,
            http_client=self.http_client
        )
        self.quotes = Quotes(
            keyid=keyid,
            private_key=private_key,
            http_client=self.http_client
        )


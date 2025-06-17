"""
Shared class for making secure requests
"""
import base64
import hashlib
from open_payments_sdk.gnap_utils.hash import HashManager
from open_payments_sdk.gnap_utils.http_signatures import HTTPSignatureClient
from open_payments_sdk.gnap_utils.keys import KeyManager


class SecurityBase():
    """
    Base class to provide shared functionality for making authenticated requests
    """
    def __init__(self, keyid: str, private_key: str):
        self.key_manager = KeyManager()
        self.hash_manager = HashManager()
        self.http_signatures = HTTPSignatureClient(self.key_manager)
        self.keyid = keyid
        self.private_key = private_key

    def get_auth_header(self, access_token: str) -> dict:
        """
        Prepare Authorization GNAP header
        """
        return {
            "authorization": f"GNAP {access_token}"
        }
    
    def get_signature_headers(self, headers: dict, method: str, target_uri: str)-> dict:
        """
        Prepare http signature headers
        """
        signature_headers = self.http_signatures.get_signature_headers(
            headers=headers,
            method=method,
            target_uri=target_uri.rstrip("/"),
            key_id=self.keyid,
            private_key=self.private_key)
        return {
            "Signature-Input":signature_headers.signature_input,
            "Signature": signature_headers.signature
        }

    def get_default_headers(self) -> dict:
        """
        Get default headers
        """
        return {
            "content-type": "application/json"
        }
       
    def get_content_digest(self, data: bytes) -> str:
        """
        Compute Digest
        """
        sha512_hash = hashlib.sha512(data).digest()
        b64_hash = base64.b64encode(sha512_hash).decode('ascii')
        return f"sha-512=:{b64_hash}:"
    
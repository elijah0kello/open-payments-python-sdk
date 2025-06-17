import time
import hashlib
import base64

from open_payments_sdk.gnap_utils.keys import KeyManager
from open_payments_sdk.models.http_signatures import SignatureBaseReturn, SignatureHeaders

class HTTPSignatureClient:
    @staticmethod
    def build_signature_base(headers: dict, method: str, target_uri: str, key_id: str, algorithm="ed25519") -> SignatureBaseReturn:
        created = int(time.time())
        covered_components = [
            "content-type",
            "authorization",
            "content-digest",
            "content-length",
            "@method",
            "@target-uri"
        ]

        signature_lines = []

        for field in covered_components:
            if field.startswith("@"):
                if field == "@method":
                    signature_lines.append(f'"@method": {method.upper()}')
                elif field == "@target-uri":
                    signature_lines.append(f'"@target-uri": {target_uri}')
            else:
                value = headers.get(field)
                if value is not None:
                    signature_lines.append(f'"{field}": {value}')

        sig_params = f'("content-type" "content-digest" "content-length" "authorization" "@method" "@target-uri");alg="{algorithm}";keyid="{key_id}";created={created}'
        signature_lines.append(f'"@signature-params": {sig_params}')

        signature_base = "\n".join(signature_lines)
        return SignatureBaseReturn(signature_params=sig_params,signature_base=signature_base)

    @staticmethod
    def hash_signature_base(signature_base: str) -> bytes:
        """
        Hash the signature base string using SHA-512 and return the digest (bytes)
        """
        sha512_hasher = hashlib.sha512()
        sha512_hasher.update(signature_base.encode('utf-8'))
        return sha512_hasher.digest()
    
    @staticmethod
    def build_signature(hashed_signature_base: str, private_key: str) -> str:
        key = KeyManager.load_ed25519_private_key_from_pem(private_key)
        signature = key.sign(hashed_signature_base)
        # Return the Base64-encoded signature string
        return base64.b64encode(signature).decode("utf-8")
    
    @staticmethod
    def get_signature_headers(headers: dict, method: str, target_uri: str, key_id: str, private_key: str, algorithm="ed25519") -> SignatureHeaders:
        """
        Returns signature and signature params as string to be used in headers
        """
        signature_base_details = HTTPSignatureClient.build_signature_base(headers, method, target_uri, key_id, algorithm)
        signature_base_hash = HTTPSignatureClient.hash_signature_base(signature_base_details.signature_base)
        signature = HTTPSignatureClient.build_signature(signature_base_hash,private_key=private_key)
        return SignatureHeaders(signature_input=signature_base_details.signature_params,signature=signature)
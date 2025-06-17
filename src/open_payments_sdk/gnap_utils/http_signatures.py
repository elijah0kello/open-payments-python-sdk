import time
import hashlib
import base64

from open_payments_sdk.gnap_utils.keys import KeyManager
from open_payments_sdk.models.http_signatures import SignatureBaseReturn, SignatureHeaders

class HTTPSignatureClient:
    """
    Class for http signature work flows
    """
    def __init__(self, key_manager : KeyManager ):
        self.key_manager = key_manager

    def build_signature_base(self,headers: dict, method: str, target_uri: str, key_id: str, algorithm="ed25519") -> SignatureBaseReturn:
        """
        Method to build an http signature base
        """
        created = int(time.time())
        pseudo_headers = ["@method", "@target-uri"]
        allowed_headers = {"content-type", "authorization", "content-digest", "content-length"}
        included_headers = [h for h in allowed_headers if h in headers]

        covered_components = included_headers + pseudo_headers

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

        quoted_fields = " ".join(f'"{field}"' for field in covered_components)
        sig_params = f'({quoted_fields});alg="{algorithm}";keyid="{key_id}";created={created}'

        signature_lines.append(f'"@signature-params": {sig_params}')
        signature_base = "\n".join(signature_lines)

        signature_base_return = SignatureBaseReturn(signature_params=sig_params,signature_base=signature_base)
        return SignatureBaseReturn.model_validate(signature_base_return)

    def hash_signature_base(self, signature_base: str) -> bytes:
        """
        Hash the signature base string using SHA-512 and return the digest (bytes)
        """
        sha512_hasher = hashlib.sha512()
        sha512_hasher.update(signature_base.encode('utf-8'))
        return sha512_hasher.digest()
    
    def build_signature(self, hashed_signature_base: str, private_key: str) -> str:
        """
        Function to build a signature base
        """
        key = self.key_manager.load_ed25519_private_key_from_pem(private_key)
        signature = key.sign(hashed_signature_base)
        # Return the Base64-encoded signature string
        return base64.b64encode(signature).decode("utf-8")
    
    def get_signature_headers(self, headers: dict, method: str, target_uri: str, key_id: str, private_key: str, algorithm="ed25519") -> SignatureHeaders:
        """
        Returns signature and signature params as string to be used in headers
        """
        signature_base_details = self.build_signature_base(headers, method, target_uri, key_id, algorithm)
        signature_base_hash = self.hash_signature_base(signature_base_details.signature_base)
        signature = self.build_signature(signature_base_hash,private_key=private_key)
        signature_headers = SignatureHeaders(signature_input=signature_base_details.signature_params,signature=signature)
        return SignatureHeaders.model_validate(signature_headers)
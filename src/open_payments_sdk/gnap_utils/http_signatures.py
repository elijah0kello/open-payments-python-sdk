import time
import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

class HTTPSignatureClient:
    @staticmethod
    def build_signature_base(headers: dict, method: str, target_uri: str, key_id="eddsa_key_1", algorithm="ed25519") -> str:
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

        sig_params = f'("content-type" "authorization" "content-digest" "content-length" "@method" "@target-uri");alg="{algorithm}";keyid="{key_id}";created={created}'
        signature_lines.append(f'"@signature-params": {sig_params}')

        signature_base = "\n".join(signature_lines)
        return signature_base

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
        key_bytes = bytes.fromhex(private_key)
        key = Ed25519PrivateKey.from_private_bytes(key_bytes)
        
        signature = key.sign(hashed_signature_base)

        # Return the Base64-encoded signature string
        return base64.b64encode(signature).decode("utf-8")
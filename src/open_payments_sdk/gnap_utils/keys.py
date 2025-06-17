import base64
import uuid
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from open_payments_sdk.models.keys import Key, KeyJwks, KeyPair

class KeyManager:

    def generate_key_pair(self) -> KeyPair:
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_pem = private_pem.decode('utf-8')
        raw_public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        x = base64.urlsafe_b64encode(raw_public_bytes).rstrip(b'=').decode()
        kid = str(uuid.uuid4())
        key = Key(
            kid=kid,
            x=x,
            alg="EdDSA",
            kty="OKP",
            crv="Ed25519"
        )
        key_jwks = KeyJwks(keys=[key])
        keypair = KeyPair(jwks=key_jwks, private_key_pem=private_key_pem)
        return KeyPair.model_validate(keypair)
    
    def load_ed25519_private_key_from_pem(self,pem_str: str) -> Ed25519PrivateKey:
        private_key = serialization.load_pem_private_key(
            data=pem_str.encode("utf-8"),
            password=None
        )

        if not isinstance(private_key, Ed25519PrivateKey):
            raise ValueError("Loaded key is not an Ed25519PrivateKey")

        return private_key


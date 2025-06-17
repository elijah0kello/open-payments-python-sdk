from open_payments_sdk.gnap_utils.keys import KeyManager
from open_payments_sdk.models.keys import KeyJwks, KeyPair


def test_key_generation():
    key_manager = KeyManager()
    key_result = key_manager.generate_key_pair()
    assert isinstance(key_result, KeyPair)
    assert isinstance(key_result.jwks, KeyJwks)
    assert len(key_result.jwks.keys) == 1
    key = key_result.jwks.keys[0]
    assert key.kty == "OKP"
    assert key.crv == "Ed25519"
    assert key.alg == "EdDSA"
    assert isinstance(key.kid, str)
    assert isinstance(key.x, str)
    assert len(key.x) >= 43 

def test_read_key_from_str():
    key_manager = KeyManager()
    key_result = key_manager.generate_key_pair()
    private_key = key_result.private_key_pem
    ed25519PrivateKey = key_manager.load_ed25519_private_key_from_pem(private_key)
    signature = ed25519PrivateKey.sign(b"my authenticated message")
    public_key = ed25519PrivateKey.public_key()
    public_key.verify(signature, b"my authenticated message")
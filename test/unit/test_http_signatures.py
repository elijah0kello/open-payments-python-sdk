import pytest
import time
import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from open_payments_sdk.gnap_utils.http_signatures import HTTPSignatureClient
from cryptography.hazmat.primitives import serialization


@pytest.fixture
def sample_headers():
    return {
        "content-type": "application/json",
        "authorization": "GNAP 123454321",
        "content-digest": "sha-512=:abc123xyz=",
        "content-length": "18"
    }


def test_build_signature_base(sample_headers):
    base = HTTPSignatureClient.build_signature_base(
        headers=sample_headers,
        method="POST",
        target_uri="https://example.com/payments"
    )

    # It should include all expected lines
    assert '"content-type": application/json' in base
    assert '"authorization": GNAP 123454321' in base
    assert '"@method": POST' in base
    assert '"@target-uri": https://example.com/payments' in base
    assert "@signature-params" in base


def test_hash_signature_base_consistency():
    sig_base = '"authorization": test\n"@method": POST'
    digest = HTTPSignatureClient.hash_signature_base(sig_base)

    expected = hashlib.sha512(sig_base.encode("utf-8")).digest()
    assert digest == expected
    assert isinstance(digest, bytes)

 

def test_build_signature():
    hashed_signature_base = b'\x00' * 64  # Example hash
    private_key = Ed25519PrivateKey.generate()
    
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Convert to hex string
    private_key_hex = private_key_bytes.hex()

    # Call the method to test
    signature = HTTPSignatureClient.build_signature(hashed_signature_base, private_key_hex)

    # Decode signature and check
    signature_bytes = base64.b64decode(signature)
    assert isinstance(signature, str)
    assert len(signature_bytes) == 64
    
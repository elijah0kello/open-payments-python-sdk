import uuid
import pytest
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

@pytest.fixture
def private_key_str():
    privkey = Ed25519PrivateKey.generate()
    private_pem = privkey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    return private_pem.decode("utf-8")


def test_build_signature_base(sample_headers):
    base = HTTPSignatureClient.build_signature_base(
        headers=sample_headers,
        method="POST",
        target_uri="https://example.com/payments",
        key_id=uuid.uuid4()
    )

    # It should include all expected lines
    assert '"content-type": application/json' in base.signature_base
    assert '"authorization": GNAP 123454321' in base.signature_base
    assert '"@method": POST' in base.signature_base
    assert '"@target-uri": https://example.com/payments' in base.signature_base
    assert "@signature-params" in base.signature_base


def test_hash_signature_base_consistency():
    sig_base = '"authorization": test\n"@method": POST'
    digest = HTTPSignatureClient.hash_signature_base(sig_base)

    expected = hashlib.sha512(sig_base.encode("utf-8")).digest()
    assert digest == expected
    assert isinstance(digest, bytes)

 

def test_build_signature():
    hashed_signature_base = b'\x00' * 64  # Example hash
    private_key = Ed25519PrivateKey.generate()
    
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Call the method to test
    signature = HTTPSignatureClient.build_signature(hashed_signature_base, private_key_pem.decode("utf-8"))

    # Decode signature and check
    signature_bytes = base64.b64decode(signature)
    assert isinstance(signature, str)
    assert len(signature_bytes) == 64
    
def test_get_signature_headers(private_key_str,sample_headers):
    signature_headers = HTTPSignatureClient.get_signature_headers(
            headers=sample_headers,
            method="POST",
            target_uri="https://example.com/payments",
            key_id=uuid.uuid4(),
            private_key=private_key_str
        )
    print(f"Signature-Input: {signature_headers.signature_input}")
    print(f"Signature: {signature_headers.signature}")
    assert "alg=\"ed25519\"" in signature_headers.signature_input
    assert "keyid=" in signature_headers.signature_input
    assert signature_headers.signature_input.startswith('("content-type"')
    
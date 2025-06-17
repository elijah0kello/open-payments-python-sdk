# test_hash_manager.py
import base64
import hashlib
from open_payments_sdk.gnap_utils.hash import HashManager  # Replace with actual module name or use relative import

def test_verify_hash():
    client_nonce = "abc123"
    interact_nonce = "xyz456"
    ref = "ref789"
    url = "https://auth.example.com"
    data = f"{client_nonce}\n{interact_nonce}\n{ref}\n{url}/"
    expected = base64.b64encode(hashlib.sha256(data.encode()).digest()).decode()

    assert HashManager.verify_hash(client_nonce, interact_nonce, ref, url, expected)
    assert not HashManager.verify_hash(client_nonce, interact_nonce, ref, url, "wrong-hash")

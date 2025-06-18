import pytest
from open_payments_sdk.api.auth import AccessTokens, Grants
from open_payments_sdk.api.resource import IncomingPayments, OutgoingPayments, Quotes
from open_payments_sdk.client.client import OpenPayemntsClient
from open_payments_sdk.gnap_utils.keys import KeyManager

@pytest.fixture
def keyid_private_key() -> dict:
    key_manager = KeyManager()
    key_pair = key_manager.generate_key_pair()
    return {
        "private_key": key_pair.private_key_pem,
        "keyid": key_pair.jwks.keys[0].kid
    }

def test_create_op_client(keyid_private_key):
    keyid = keyid_private_key["keyid"]
    private_key = keyid_private_key["private_key"]
    client = OpenPayemntsClient(keyid=keyid_private_key["keyid"],private_key=keyid_private_key["private_key"])

    assert client.keyid == keyid
    assert client.private_key == private_key

    assert isinstance(client.grants, Grants)
    assert isinstance(client.access_tokens, AccessTokens)
    assert isinstance(client.incoming_payments, IncomingPayments)
    assert isinstance(client.outgoing_payments, OutgoingPayments)
    assert isinstance(client.quotes, Quotes)


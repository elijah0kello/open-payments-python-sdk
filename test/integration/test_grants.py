import pytest
import yaml

from open_payments_sdk.api.auth import Grants
from open_payments_sdk.gnap_utils.keys import KeyManager
from open_payments_sdk.models.auth import GrantRequest


@pytest.fixture
def auth_server(request):
    root = request.config.rootpath
    path = root / "spec" / "auth-server.yaml"
    with open(path) as f:
        spec = yaml.safe_load(f)
        return spec["servers"][0]["url"]


@pytest.fixture
def example_grant_requests(request):
    root = request.config.rootpath
    spec_path = root / "spec" / "auth-server.yaml"
    with open(spec_path) as f:
        spec = yaml.safe_load(f)
        path = spec["paths"]["/"]["post"]
        examples = path["requestBody"]["content"]["application/json"]["examples"]
        return examples.values()

@pytest.fixture
def keyid_private_key() -> dict:
    key_manager = KeyManager()
    key_pair = key_manager.generate_key_pair()
    return {
        "private_key": key_pair.private_key_pem,
        "keyid": key_pair.jwks.keys[0].kid
    }


def test_post_grant_request(auth_server, example_grant_requests,keyid_private_key):
    grant = Grants(keyid=keyid_private_key["keyid"],private_key=keyid_private_key["private_key"])
    for example in example_grant_requests:
        grant_request = GrantRequest.model_validate(example["value"])
        grant.post_grant_request(grant_request, auth_server)

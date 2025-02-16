import pytest
import yaml

from open_payments_sdk.api.auth import Grants
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


def test_post_grant_request(auth_server, example_grant_requests):
    grant = Grants(auth_server)
    for example in example_grant_requests:
        grant_request = GrantRequest.model_validate(example["value"])
        grant.post_grant_request(grant_request)

import pytest
import yaml

from open_payments_sdk.api.wallet import Wallet


@pytest.fixture
def wallet_address_server(request):
    root = request.config.rootpath
    path = root / "spec" / "wallet-address-server.yaml"
    with open(path) as f:
        spec = yaml.safe_load(f)
        return spec["servers"][0]["url"]


def test_get_wallet_address(wallet_address_server):
    wallet = Wallet(wallet_address_server)
    wallet.get_wallet_address()


def test_get_wallet_address_keys(wallet_address_server):
    wallet = Wallet(wallet_address_server)
    wallet.get_keys()

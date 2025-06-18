# Python Open Payments SDK

<p align="center">
  <img src="https://raw.githubusercontent.com/interledger/open-payments/main/docs/public/img/logo.svg" width="700" alt="Open Payments">
</p>

> This project is still a work in progress

## Open Payments

Open Payments is an open API standard that can be implemented by account servicing entities (e.g. banks, digital wallet providers, and mobile money providers) to facilitate interoperability in the setup and completion of payments for different use cases including:

- Web Monetization
- Tipping/Donations (low value/low friction)
- eCommerce checkout
- P2P transfers
- Subscriptions
- Invoice Payments

An Open Payments server runs two sub-systems, a resource server which exposes APIs for performing functions against the underlying accounts and authorization server which exposes APIs compliant with the GNAP standard for getting grants to access the resource server APIs.

## Local development



- Python >= 3.11

  To install python visit [Python Download](https://www.python.org/downloads/)
- Poetry
  To install poetry visiit [Poetry Documentation](https://python-poetry.org/docs/)

### Installation

1. Activate your virtual emvironment. No need to create one, Poetry creates one. 
   [Read Poetry documentation](https://python-poetry.org/docs/managing-environments/)  to read how to activate


2. Install the dependencies in the poetry.lock

```
> poetry install
```
## Usage 
To use this sdk, you will first need to install it in your project.  Currently you will need to build from source but once it is hosted on pypi you will be able to install it with pip

```bash
python3 -m pip install open-payments-python-sdk #currently not setup
```
## Installing from source

Clone the repository 
```bash
git clone https://github.com/interledger/open-payments-python-sdk.git
cd open-payments-python-sdk
```

Build the package
```bash
poetry build
```
After running this command, the wheel package will be written to the `dist/` folder in the repo you just cloned

Install it in your project

```bash
pip install </path/to/>open-payments-python-sdk/dist/open_payments_sdk-0.1.0-py3-none-any.whl
```

# Initialising the Client
To create a client you can do so by importing the `OpenPaymentsClient` defined in the [`client`](./src/client/client.py) module and instantiating it.

```python
from open_payments_sdk.client.client import OpenPayemntsClient

with open("privkey.pem","r",encoding="utf_8") as privkey:
    private_key = privkey.read()

op_client = OpenPayemntsClient(keyid="27b4f8d2-746c-4522-b3f0-874ca15bfe65",private_key=private_key)
```

The client is to be created after you have created a key pair and have obtained the `kid` and `private_key`

Some helper functions have been created to ease key pair creation. A class called `KeyManager` has been created and it provides functions to create a key pair and load a private key from UTF-8 string. It also returns an object that has information to be registered at the AS when registering the public key.

```python
import json
from open_payments_sdk.gnap_utils.keys import KeyManager

key_manager = KeyManager()
key_pair = key_manager.generate_key_pair() # generate key pair

with open("privkey.pem", "w",encoding="utf_8") as pem_file: # save private key to file
    pem_file.write(key_pair.private_key_pem)


with open("jwks.json","w", encoding="utf_8") as jwks_file: # save jwks.json file
    jwks_file.write(json.dumps(key_pair.jwks.keys[0].__dict__))


with open("privkey.pem", "r", encoding="utf_8") as privkey: # load private key from file system
    private_key = privkey.read()

private_key = key_manager.load_ed25519_private_key_from_pem(
    private_key
) # load private key fron file utf_8 string

public_key = private_key.public_key() # derive public key from private key
```
## Wallets
You can use the created client to interact with the resource server. In this case we will use it to interact with a wallet address to get the wallet address details and jwks.json 

```python
#get wallet address
wallet_address_details = op_client.wallet.get_wallet_address("https://ilp.interledger-test.dev/elijahokellosalary")

# Output
{'id': AnyUrl('https://ilp.interledger-test.dev/elijahokellosalary'), 'publicName': 'elijahokellosalary', 'assetCode': AssetCode(root='USD'), 'assetScale': AssetScale(root=2), 'authServer': AnyUrl('https://auth.interledger-test.dev/'), 'resourceServer': AnyUrl('https://ilp.interledger-test.dev/')}

```
Get Wallet jwks

```python
#get wallet jwks
wallet_jwks = op_client.wallet.get_keys("https://ilp.interledger-test.dev/elijahokellosalary")

# Output 
{'keys': []}

```

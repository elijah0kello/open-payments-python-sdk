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


## Interledger

If you would like to learn more about Interledger, here are some excellent resources:

- [Interledger Website](https://interledger.org/)
- [Interledger Specification](https://interledger.org/developers/rfcs/interledger-protocol/)
- [Interledger Explainer Video](https://x.com/Interledger/status/1567916000074678272)
- [Open Payments](https://openpayments.dev/)
- [Web monetization](https://webmonetization.org/)


## Local development



- Python >= 3.11

  To install python visit [Python Download](https://www.python.org/downloads/)
- Poetry
  To install poetry visiit [Poetry Documentation](https://python-poetry.org/docs/)

### Installation

1. Activate your virtual emvironment. No need to create one, Poetry creates one. 
   [Read Poetry documentation](https://python-poetry.org/docs/managing-environments/)  to read how to activate


2. Install the dependencies un the poetry.lock

```
> poetry install
```

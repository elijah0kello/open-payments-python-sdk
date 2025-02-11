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

## Project RoadMap
This project will draw inspiration from the typescript Open Payments SDK with a python implementation. The goal is to have the SDK library(s) hosted on [PyPi](https://pypi.org/) and therefore installable via pip

Here is an outline of the project implementation roadmap and release timelines

|Item | Description| Start Date | Duration |End Date |Status 
|-----|------------|-------|---------|--------|-------|
|Project Planning |This will involve conducting detailed research about open payments, planning the project execution and generating any pre project requirements | 10th Jan 2025| 1 month|10th Feb 2025 |Done 🟢|
|Designing the SDK while benchmarking on Typescript OP SDK| This will involve designing of the SDK based on the already existing Typescript Open Payments SDK. The milestone for this phase will be a design documentation for the SDK. Make design decisions regarding the `openapi`, `http-signature` and `py-openpayments-sdk` libraries and implementation plans |10th Feb 2025 | 1 month | 10th March 2025| In Progress 🟡|
| Setup folder structure and initialize project | This will involve setting up the project by adding code folder structure, linting, tests, pre commit checks and pipeline configuration. Creating a PR to the upstream and getting feedback | 10th March 2025 | 3 weeks | 31st March 2025 | In Progress 🟡 |
|Implementing auth functions | Implementing the Authentication and Authorization functions of the SDK including creating any required libraries based on the design adopted. Creating a PR and getting feedback from the community and any maintainers. | 31st March 2025 | 1.5 months | 15th May 2025 | Not Started ⚫️ |
|Implementing payments functions | Implementing the payments functions of the SDK including creating or updating any required libraries based on the design adopted. Creating a PR and getting feedback from the community and any maintainers. | 15th May 2025 | 2 months | 15th July 2025 | Not Started ⚫️ |
| Implementing feedback from Pull Requests | Working on implementing PR feedback to ensure quality of the SDK. | TBD | TBD |TDB| Not Started ⚫️ |







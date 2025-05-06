from open_payments_sdk.configuration import Configuration
from open_payments_sdk.http import Client as HttpClient
from open_payments_sdk.models.resource import (IncomingPayment,
                                               IncomingPaymentRequest,
                                               IncomingPaymentResponse,
                                               OutgoingPayment,
                                               OutgoingPaymentRequest,
                                               PaginatedIncomingPayments,
                                               PaginatedOutgoingPayments,
                                               PaymentListQuery, Quote,
                                               QuoteRequest)


class IncomingPayments:
    def __init__(self, resource_server_endpoint: str, http_client: HttpClient = None):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client
        self.resource_server_endpoint = resource_server_endpoint.rstrip("/")

    def post_create_payment(self, payment: IncomingPaymentRequest) -> IncomingPayment:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/incoming-payments"
        data = payment.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.post(url, json=data)
        return IncomingPayment.model_validate(response.json())

    def get_incoming_payments(
        self, query: PaymentListQuery
    ) -> PaginatedIncomingPayments:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/incoming-payments"
        query_params = query.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.get(url, params=query_params)
        return PaginatedIncomingPayments.model_validate(response.json())

    def get_incoming_payment(self, payment_id: str) -> IncomingPayment:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/incoming-payments/{payment_id}"
        response = self.http_client.get(url)
        return IncomingPaymentResponse.model_validate(response.json())

    def post_complete_incoming_payment(self, payment_id: str) -> IncomingPayment:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/incoming-payments/{payment_id}/complete"
        response = self.http_client.post(url)
        return IncomingPayment.model_validate(response.json())


class OutgoingPayments:
    def __init__(self, resource_server_endpoint: str, http_client: HttpClient = None):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client
        self.resource_server_endpoint = resource_server_endpoint.rstrip("/")

    def post_create_payment(self, payment: OutgoingPaymentRequest) -> OutgoingPayment:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/outgoing-payments"
        data = payment.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.post(url, json=data)
        return OutgoingPayment.model_validate(response.json())

    def get_outgoing_payments(
        self, query: PaymentListQuery
    ) -> PaginatedOutgoingPayments:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/outgoing-payments"
        query_params = query.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.get(url, params=query_params)
        return PaginatedOutgoingPayments.model_validate(response.json())

    def get_outgoing_payment(self, payment_id: str) -> OutgoingPayment:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/outgoing-payments/{payment_id}"
        response = self.http_client.get(url)
        return OutgoingPayment.model_validate(response.json())


class Quotes:
    def __init__(self, resource_server_endpoint: str, http_client: HttpClient = None):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client
        self.resource_server_endpoint = resource_server_endpoint.rstrip("/")

    def post_create_quote(self, quote: QuoteRequest) -> Quote:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/quotes"
        data = quote.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.post(url, json=data)
        return Quote.model_validate(response.json())

    def get_quote(self, quote_id: str) -> Quote:
        base_url = self.resource_server_endpoint
        url = f"{base_url}/quotes/{quote_id}"
        response = self.http_client.get(url)
        return Quote.model_validate(response.json())

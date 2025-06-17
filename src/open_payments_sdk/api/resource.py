"""
Resource Server Module
"""
import json
from open_payments_sdk.configuration import Configuration
from open_payments_sdk.gnap_utils.security import SecurityBase
from open_payments_sdk.http import HttpClient 
from open_payments_sdk.models.resource import (IncomingPayment,
                                               IncomingPaymentRequest,
                                               IncomingPaymentResponse,
                                               OutgoingPayment,
                                               OutgoingPaymentRequest,
                                               PaginatedIncomingPayments,
                                               PaginatedOutgoingPayments,
                                               PaymentListQuery, Quote,
                                               QuoteRequest)


class IncomingPayments(SecurityBase):
    """
    Class for handling incoming payments resources
    """
    def __init__(self, keyid: str, private_key: str, http_client: HttpClient = None):
        super().__init__(keyid=keyid,private_key=private_key)
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client

    def post_create_payment(
            self,
            payment: IncomingPaymentRequest,
            resource_server_endpoint: str,
            access_token: str
        ) -> IncomingPayment:
        """
        Create Incoming Payment
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/incoming-payments"
        data = payment.model_dump(exclude_unset=True, mode="json")
        data_bytes = json.dumps(data).encode("utf-8")
        req_headers = {
            **self.get_default_headers(),
            **self.get_auth_header(access_token=access_token),
            "content-length": str(len(data_bytes)),
            "content-digest":self.get_content_digest(data_bytes)
        }
        response = self.http_client.post(url, json=data_bytes, headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="POST",
                target_uri=resource_server_endpoint
            )
        })
        return IncomingPayment.model_validate(response.json())

    def get_incoming_payments(
            self, query: PaymentListQuery,
            resource_server_endpoint: str,
            access_token: str
        ) -> PaginatedIncomingPayments:
        """
        Get Incoming Payment
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/incoming-payments"
        query_params = query.model_dump(exclude_unset=True, mode="json")
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.get(url, params=query_params, headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="GET",
                target_uri=resource_server_endpoint
            )
        })
        return PaginatedIncomingPayments.model_validate(response.json())

    def get_incoming_payment(
            self,
            payment_id: str,
            resource_server_endpoint: str,
            access_token: str
        ) -> IncomingPayment:
        """
        Get Incoming Payment
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/incoming-payments/{payment_id}"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.get(url,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="GET",
                target_uri=resource_server_endpoint
            )
        })
        return IncomingPaymentResponse.model_validate(response.json())

    def post_complete_incoming_payment(
            self,
            payment_id: str,
            resource_server_endpoint: str,
            access_token: str
        ) -> IncomingPayment:
        """
        Complete Incoming Payment
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/incoming-payments/{payment_id}/complete"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.post(url,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="GET",
                target_uri=resource_server_endpoint
            )
        })
        return IncomingPayment.model_validate(response.json())


class OutgoingPayments(SecurityBase):
    """
    Class for handling outgoing payments resources
    """
    def __init__(self, keyid: str, private_key: str, http_client: HttpClient = None):
        super().__init__(keyid=keyid,private_key=private_key)
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client

    def post_create_payment(
            self, payment: OutgoingPaymentRequest,
            resource_server_endpoint: str,
            access_token: str
        ) -> OutgoingPayment:
        """
        Create an Outgoing Payment Resource
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/outgoing-payments"
        data = payment.model_dump(exclude_unset=True, mode="json")
        data_bytes = json.dumps(data).encode("utf-8")
        req_headers = {
            **self.get_default_headers(),
            **self.get_auth_header(access_token=access_token),
            "content-length": str(len(data_bytes)),
            "content-digest":self.get_content_digest(data_bytes)
        }
        response = self.http_client.post(url, json=data_bytes, headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="POST",
                target_uri=resource_server_endpoint
            )
        })
        return OutgoingPayment.model_validate(response.json())

    def get_outgoing_payments(
        self, 
        query: PaymentListQuery,
        resource_server_endpoint: str,
        access_token: str
    ) -> PaginatedOutgoingPayments:
        """
        Get Outgoing Payments
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/outgoing-payments"
        query_params = query.model_dump(exclude_unset=True, mode="json")
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.get(url, params=query_params,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="GET",
                target_uri=resource_server_endpoint
            )
        })
        return PaginatedOutgoingPayments.model_validate(response.json())

    def get_outgoing_payment(
            self, payment_id: str,
            resource_server_endpoint: str,
            access_token: str
        ) -> OutgoingPayment:
        """
        Get Outgoing Payment
        """
        base_url = resource_server_endpoint
        url = f"{base_url}/outgoing-payments/{payment_id}"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.get(url,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="GET",
                target_uri=resource_server_endpoint
            )
        })
        return OutgoingPayment.model_validate(response.json())


class Quotes(SecurityBase):
    """
    Class for handling Quote resources
    """
    def __init__(self, keyid: str, private_key: str, http_client: HttpClient = None):
        super().__init__(keyid=keyid,private_key=private_key)
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client

    def post_create_quote(
            self, quote: QuoteRequest,
            resource_server_endpoint: str,
            access_token: str
        ) -> Quote:
        """
        Create a Quote 
        """
        base_url = resource_server_endpoint.rstrip("/")
        url = f"{base_url}/quotes"
        data = quote.model_dump(exclude_unset=True, mode="json")
        data_bytes = json.dumps(data).encode("utf-8")
        req_headers = {
            **self.get_default_headers(),
            **self.get_auth_header(access_token=access_token),
            "content-length": str(len(data_bytes)),
            "content-digest":self.get_content_digest(data_bytes)
        }
        response = self.http_client.post(url, json=data_bytes,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="POST",
                target_uri=resource_server_endpoint
            )
        })
        return Quote.model_validate(response.json())

    def get_quote(
            self, 
            quote_id: str, 
            resource_server_endpoint: str,
            access_token: str
        ) -> Quote:
        """
        Get a Quote
        """
        base_url = resource_server_endpoint.strip("/")
        url = f"{base_url}/quotes/{quote_id}"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.get(url, headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="GET",
                target_uri=resource_server_endpoint
            )
        })
        return Quote.model_validate(response.json())

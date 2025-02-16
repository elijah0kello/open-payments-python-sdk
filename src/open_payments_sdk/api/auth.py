import json

from open_payments_sdk.configuration import Configuration
from open_payments_sdk.http import Client as HttpClient
from open_payments_sdk.models.auth import AccessToken
from open_payments_sdk.models.auth import Grant as AuthGrant
from open_payments_sdk.models.auth import (GrantContinueResponse, GrantRequest,
                                           InteractRef)


class Grants:
    def __init__(self, auth_server_endpoint: str, http_client: HttpClient = None):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client
        self.auth_server_endpoint = auth_server_endpoint

    def post_grant_request(self, grant_request: GrantRequest) -> AuthGrant:
        data = grant_request.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.post(self.auth_server_endpoint, json=data)
        return AuthGrant.model_validate(json.loads(response))

    def post_grant_continuation_request(self, req_id: str, interact_ref: InteractRef):
        base_url = self.auth_server_endpoint.rstrip("/")
        url = f"{base_url}/continue/{req_id}"
        data = interact_ref.model_dump(exclude_unset=True, mode="json")
        response = self.http_client.post(url, json=data)
        return GrantContinueResponse.model_validate(json.loads(response))

    def delete_grant(self, req_id: str) -> None:
        base_url = self.auth_server_endpoint.rstrip("/")
        url = f"{base_url}/continue/{req_id}"
        self.http_client.delete(url)


class AccessTokens:
    def __init__(self, auth_server_endpoint: str, http_client: HttpClient = None):
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client
        self.auth_server_endpoint = auth_server_endpoint

    def post_rotate_access_token(self, token_id: str) -> AccessToken:
        base_url = self.auth_server_endpoint.rstrip("/")
        url = f"{base_url}/token/{token_id}"
        response = self.http_client.post(url)
        return AccessToken.model_validate(json.loads(response))

    def delete_access_token(self, token_id: str) -> None:
        base_url = self.auth_server_endpoint.rstrip("/")
        url = f"{base_url}/token/{token_id}"
        self.http_client.delete(url)

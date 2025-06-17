"""
Grants Module
"""

import json

from open_payments_sdk.configuration import Configuration
from open_payments_sdk.gnap_utils.security import SecurityBase
from open_payments_sdk.http import HttpClient
from open_payments_sdk.models.auth import AccessToken
from open_payments_sdk.models.auth import Grant as AuthGrant
from open_payments_sdk.models.auth import (GrantContinueResponse, GrantRequest,
                                           InteractRef)



class Grants(SecurityBase):
    """
    Class to handle Grants in the sdk
    """
    def __init__(self, keyid: str, private_key: str ,http_client: HttpClient = None):
        super().__init__(keyid=keyid, private_key=private_key)
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client

    def post_grant_request(
            self,
            grant_request: GrantRequest,
            auth_server_endpoint: str
        ) -> AuthGrant:
        """
        Grant Request
        """
        data = grant_request.model_dump(exclude_unset=True, mode="json")
        data_bytes = json.dumps(data).encode("utf-8")

        req_headers = {
            **self.get_default_headers(),
            "content-length":str(len(data_bytes)),
            "content-digest":self.get_content_digest(data_bytes)
        }
        response = self.http_client.post(auth_server_endpoint, json=data_bytes,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="POST",
                target_uri=auth_server_endpoint
            )}
        )
        return AuthGrant.model_validate(json.loads(response))

    def post_grant_continuation_request(
            self,
            req_id: str,
            interact_ref: InteractRef,
            auth_server_endpoint: str,
            access_token: str
        ) -> GrantContinueResponse:
        """
        Continue Grant Request
        """
        base_url = auth_server_endpoint.rstrip("/")
        url = f"{base_url}/continue/{req_id}"
        data = interact_ref.model_dump(exclude_unset=True, mode="json")
        data_bytes = json.dumps(data).encode("utf-8")
        req_headers = {
            **self.get_default_headers(),
            "content-length": str(len(data_bytes)),
            "content-digest": self.get_content_digest(data_bytes),
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.post(
            url,
            json=data,
            headers={
                **req_headers,
                **self.get_signature_headers(
                headers=req_headers,
                method="POST",
                target_uri=auth_server_endpoint
            )
            }
        )
        return GrantContinueResponse.model_validate(json.loads(response))

    def delete_grant(
            self,
            req_id: str,
            auth_server_endpoint: str,
            access_token: str
        ) -> None:
        """
        Delete Grant
        """
        base_url = auth_server_endpoint.rstrip("/")
        url = f"{base_url}/continue/{req_id}"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        self.http_client.delete(url,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="DELETE",
                target_uri=auth_server_endpoint
            )
        })



class AccessTokens(SecurityBase):
    """
    Access Token Class
    """
    def __init__(self, keyid: str , private_key: str, http_client: HttpClient = None):
        super().__init__(keyid=keyid, private_key=private_key)
        if not http_client:
            cfg = Configuration()
            http_client = HttpClient(cfg)

        self.http_client = http_client

    def post_rotate_access_token(
            self, 
            token_id: str, 
            auth_server_endpoint: str, 
            access_token: str
        ) -> AccessToken:
        """
        Rotate Access Token
        """
        base_url = auth_server_endpoint.rstrip("/")
        url = f"{base_url}/token/{token_id}"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        response = self.http_client.post(url,headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="POST",
                target_uri=auth_server_endpoint
            )
        })
        return AccessToken.model_validate(json.loads(response))

    def delete_access_token(
            self,
            token_id: str,
            auth_server_endpoint: str,
            access_token: str
        ) -> None:
        """
        Delete Access Token
        """
        base_url = auth_server_endpoint.rstrip("/")
        url = f"{base_url}/token/{token_id}"
        req_headers = {
            **self.get_auth_header(access_token=access_token)
        }
        self.http_client.delete(url, headers={
            **req_headers,
            **self.get_signature_headers(
                headers=req_headers,
                method="DELETE",
                target_uri=auth_server_endpoint
            )
        })
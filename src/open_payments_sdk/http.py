"""
HTTP Client 
"""
import httpx

class HttpClient:
    """
    HTTP Client
    """
    http_timeout: float

    def __init__(self, http_timeout: float):
        self.http_timeout = http_timeout

    def build_request(
            self,
            method: str,
            url: str,
            headers = None,
            data = None,
            json: dict = None,
            params: dict = None
    ) -> httpx.Request:
        """
        Build httpx request
        """
        return httpx.Request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            data=data,
            params=params
        )

    def send(self, request: httpx.Request) -> httpx.Response:
        """
        Make an http request
        """ 
        with httpx.Client(timeout=self.http_timeout) as client:
            res = client.send(request=request)
        res.raise_for_status()
        return res

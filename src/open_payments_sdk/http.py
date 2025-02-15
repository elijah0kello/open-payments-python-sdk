import httpx
import logging

from open_payments_sdk import configuration


class Client:
    def __init__(self, cfg: configuration.Configuration):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(cfg.get_log_handler())
        self.user_agent = cfg.user_agent

    @staticmethod
    def is_json(res):
        return res.headers["content-type"] == "application/json"

    def parse_response(self, res: httpx.Response):
        if self.is_json(res):
            return res.json()
        return res.text

    def get(self, url, params=None, headers=None):
        res = httpx.get(url, params=params, headers=headers)
        res.raise_for_status()
        return self.parse_response(res)

    def post(self, url, data=None, headers=None):
        res = httpx.post(url, data=data, headers=headers)
        res.raise_for_status()
        return self.parse_response(res)

    def delete(self, url, params=None, headers=None):
        res = httpx.delete(url, params=params, headers=headers)
        res.raise_for_status()
        return self.parse_response(res)

import logging

import httpx

from open_payments_sdk import configuration


class HttpClient:
    def __init__(self, cfg: configuration.Configuration = None):
        if not cfg:
            cfg = configuration.Configuration()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(cfg.get_log_handler())
        self.user_agent = cfg.user_agent

    @staticmethod
    def get(url, params=None, headers=None):
        res = httpx.get(url, params=params, headers=headers)
        res.raise_for_status()
        return res.text

    @staticmethod
    def post(url, json=None, headers=None):
        res = httpx.post(url, content=json, headers=headers)
        res.raise_for_status()
        return res.text

    @staticmethod
    def delete(url, params=None, headers=None):
        res = httpx.delete(url, params=params, headers=headers)
        res.raise_for_status()
        return res.text

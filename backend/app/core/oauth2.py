from typing import Any, Mapping, Optional, Union

from pydantic import BaseSettings
from httpx import AsyncClient

OAUTH_CLIENT_PARAMS = (
    "client_id",
    "client_secret",
    "redirect_uri",
    "authorization_url",
    "access_token_url",
    "api_base_url",
)


class OAuth2:
    def __init__(self, config: Any):
        self._registry = {}
        self._clients = {}
        self.config = config

    def create_client(self, name: str):
        if name in self._clients:
            return self._clients[name]

        if name not in self._registry:
            return None
        config = {}
        for key in OAUTH_CLIENT_PARAMS:
            conf_key = f"{name}_{key}".upper()
            conf_value = self.config.get(conf_key, default=None)
            if conf_value:
                config[key] = conf_value
        client = OAuth2Client(**config)
        self._clients[name] = client
        return client

    def register(self, name: str, **kwargs):
        self._registry[name] = kwargs
        return self.create_client(name)


class OAuth2Client(AsyncClient):
    SESSION_CLIENT_PARAMS = [
    'headers', 'cookies', 'verify', 'cert', 'http1', 'http2',
    'proxies', 'timeout', 'follow_redirects', 'limits', 'max_redirects',
    'event_hooks', 'base_url', 'transport', 'app', 'trust_env',
    ]

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        authorization_url: str,
        access_token_url: str,
        api_base_url: str,
        **kwargs: Any
    ):
        self.client_id = (client_id,)
        self.client_secret = (client_secret,)
        self.redirect_uri = redirect_uri
        self.authorization_url = authorization_url
        self.access_token_url = (access_token_url,)
        self.api_base_url = api_base_url
        client_kwargs = self._extract_session_client_params(kwargs)
        super().__init__(**client_kwargs)

    def _extract_session_client_params(self, params: dict[str, Any]):
        result = {}
        for k in self.SESSION_CLIENT_PARAMS:
            result[k] = params.get(k, default=None)
        return result

    async   
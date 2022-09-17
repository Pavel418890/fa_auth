from typing import Any, Mapping, Optional

from pydantic import BaseSettings


class OAuth2:
    def __init__(self):
        self._registry = {}
        self._clients = {}

    async def create_client(self, name: str):
        pass

    async def register(self):
        pass


class AppIntegration:
    def __init__(self, name: str, cache=None):
        self.name = name
        self.cache = cache

    @staticmethod
    def load_config(
        oauth: OAuth2, name: str, params: dict[str, int | str | Any]
    ) -> dict[Optional[str], int | str | Any]:
        result = {}
        for key in params:
            conf_key = f"{name}_{key}".upper()
            conf_value = oauth.config.get(conf_key, default=None)
            if conf_value is not None:
                result[key] = conf_value

        return result

import functools
import json
from aiohttp import web


class Decorators:
    @staticmethod
    def is_logged_by_cookie(coro):
        """Check if logged by cookie"""
        @functools.wraps(coro)
        async def wrapped(*args, **kwargs):
            self_request = args[0].request
            self_db = args[0].request.app["mongo_db"]

            cookies_item = self_request.cookies

            if len(cookies_item) == 0 or "authorization" not in cookies_item:
                return web.json_response(
                    {"error": "no cookie"},
                    status=403,
                    content_type="application/json"
                )

            auth_key = cookies_item["authorization"]
            db_key_querry = await self_db.find_auth_by_key(key=auth_key)
            if not db_key_querry:
                return web.json_response(
                    {"error": "invalid api key"},
                    status=403,
                    content_type="application/json"
                )

            return await coro(*args, **kwargs)
        return wrapped

    @staticmethod
    def validate_json_body(pass_json_body: bool=False):
        """Validate json body"""
        def inner(coro):
            @functools.wraps(coro)
            async def wrapped(*args, **kwargs):
                self_request = args[0].request

                try:
                    json_payload = await self_request.json()
                except json.decoder.JSONDecodeError:
                    return web.json_response(
                        {"status": "incorrect body"},
                        status=400,
                        content_type="application/json"
                    )
                if pass_json_body:
                    return await coro(*args, json_payload, **kwargs)
                return await coro(*args, **kwargs)
            return wrapped
        return inner

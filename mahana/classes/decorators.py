import functools
from aiohttp import web


class Decorators:
    @staticmethod
    def is_logged_by_cookie(coro):
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

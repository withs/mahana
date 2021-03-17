import uuid
import json

import aiohttp_jinja2
from aiohttp import web

from classes import (
    Decorators,
    Utils
)

class Worker(web.View):

    @Decorators.is_logged_by_cookie
    async def get(self):
        """get workers"""

        try:
            json_payload = await self.request.json()
        except json.decoder.JSONDecodeError:
            return web.json_response(
                {"status": "incorrect body"},
                status=400,
                content_type="application/json"
            )

        db = self.request.app["mongo_db"]

        worker_name = json_payload.get("worker_name")

        if worker_name is None:
            return web.json_response(
                {"status": "incorrect body"},
                status=400,
                content_type="application/json"
            )

        is_a_worker_with_this_name = await db.find_by_worker_name(worker_name)

        if not is_a_worker_with_this_name.result:
            return web.json_response(
                {"status": "No worker found with this name"},
                status=400,
                content_type="application/json"
            )

        worker_data = is_a_worker_with_this_name.result_data
        worker_data.pop("auth_keys")

        return web.json_response(
            worker_data,
            status=200,
            content_type="application/json"
        )

    @Decorators.is_logged_by_cookie
    async def put(self):
        """add new worker"""

        try:
            json_payload = await self.request.json()
        except json.decoder.JSONDecodeError:
            return web.json_response(
                {"status": "incorrect body"},
                status=400,
                content_type="application/json"
            )

        db = self.request.app["mongo_db"]

        worker_name = json_payload.get("worker_name")

        if worker_name is not None:
            is_already_a_worker_with_this_name = await db.find_by_worker_name(worker_name)
            print(is_already_a_worker_with_this_name)

        if is_already_a_worker_with_this_name.result:
            return web.json_response(
                {"status": "Already an existing worker with this name"},
                status=400,
                content_type="application/json"
            )

        api_key = Utils.ur_safe_key(key_len=36)

        new_user = {
            "woker_name": json_payload.get("worker_name", "undefined"),
            "worker_display_name": json_payload.get("worker_name", "undefined"),
            "worker_id": str(uuid.uuid4()),
            "last_data_sent": None,
            "auth_keys": [api_key],
            "sensors": [],
            "worker_config": {
              "send_data_interval": 0 # prendre cette valuer depuis la config modulaire (config.toml)
            }
        }

        return web.json_response(
            {"status": "worker created", "api_key":api_key},
            status=201,
            content_type="application/json"
        )

    @Decorators.is_logged_by_cookie
    async def delete(self):
        """delete a worker"""

    @Decorators.is_logged_by_cookie
    async def patch(self):
        """edit worker"""

import uuid
import json
import asyncio

import aiohttp_jinja2
from aiohttp import web

from rich import print

from classes import (
    Decorators,
    Utils
)

from classes import (
    Worker
)

class WorkerView(web.View):

    # TODO: ajouter possiblité de trouver un worker par sont id
    # TODO: ajouter argument url dans le get pour return tout les worker + arg

    @Decorators.is_logged_by_cookie
    async def get(self):
        """get workers"""


    @Decorators.is_logged_by_cookie
    @Decorators.validate_json_body(pass_json_body=True)
    async def put(self, json_payload):
        """add new worker"""

        db_con = self.request.app["mongo_db"]
        new_worker = await Worker.create_new_worker(json_payload, db_con)

        if new_worker[0] is True:
            return web.json_response(
                {
                    "status": "new worker added",
                    "error": "",
                    "return_data": {
                        "worker_name": new_worker[1].name,
                        "worker_id": new_worker[1].id,
                        "auth_keys": new_worker[1].auth_keys
                    }
                },
                status=201,
                content_type="application/json"
            )

        return web.json_response(
            {
                "status": "An error occured",
                "error": new_worker[1],
                "return_data": {}
            },
            status=409,
            content_type="application/json"
        )

    
    @Decorators.is_logged_by_cookie
    async def delete(self):
        """delete a worker"""


    @Decorators.is_logged_by_cookie
    async def patch(self):
        """edit worker"""

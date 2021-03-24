import uuid
import json
import asyncio

import aiohttp_jinja2
from aiohttp import web

from rich import print

from classes import (
    Decorators,
    Utils,
    Worker
)

class WorkerView(web.View):

    # TODO: ajouter possiblité de trouver un worker par sont id
    # TODO: ajouter argument url dans le get pour return tout les worker + arg

    @Decorators.is_logged_by_cookie
    @Decorators.validate_json_body(pass_json_body=True)
    async def get(self, json_payload):
        """get workers"""

        desired_keys = json_payload.get("keys", None)
        if desired_keys is None:
            return web.json_response(
                {
                    "status": "An error occured",
                    "error": "missing key : keys",
                    "return_data": {}
                },
                status=400,
                content_type="application/json"
            )

        db_con = self.request.app["mongo_db"]

        worker = await db_con.find_worker(
            worker_id=json_payload.get("worker_id", None),
            worker_name=json_payload.get("worker_name", None)
            )
        if not worker:
            return web.json_response(
                {
                    "status": "An error occured",
                    "error": "cannot find this worker",
                    "return_data": {}
                },
                status=400,
                content_type="application/json"
            )

        returned_keys = {}

        if "*" in desired_keys:
            returned_keys = worker.to_dict()
        else:
            for key in desired_keys:
                val = worker[key]
                if val is not None:
                    returned_keys[key] = val

        return web.json_response(
            {
                "status": "Ok",
                "error": "",
                "return_data": returned_keys
            },
            status=200,
            content_type="application/json"
        )

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
    @Decorators.validate_json_body(pass_json_body=True)
    async def delete(self, json_payload):
        """delete a worker"""

        db_con = self.request.app["mongo_db"]

        worker = await db_con.find_worker(
            worker_id=json_payload.get("worker_id", None),
            worker_name=json_payload.get("worker_name", None)
            )
        if not worker:
            return web.json_response(
                {
                    "status": "An error occured",
                    "error": "cannot find this worker",
                    "return_data": {}
                },
                status=400,
                content_type="application/json"
            )

        delete_req = await worker.delete()
        if delete_req[0]:
            return web.json_response(
                {
                    "status": "worker deleted",
                    "error": "",
                    "return_data": {}
                },
                status=200,
                content_type="application/json"
            )
        return web.json_response(
            {
                "status": "An error occured",
                "error": "cannot delete the worker",
                "return_data": {}
            },
            status=204,
            content_type="application/json"
        )


    @Decorators.is_logged_by_cookie
    @Decorators.validate_json_body(pass_json_body=True)
    async def patch(self, json_payload):
        """edit worker"""

        db_con = self.request.app["mongo_db"]

        worker = await db_con.find_worker(worker_id=json_payload.get("worker_id", None))
        if not worker:
            return web.json_response(
                {
                    "status": "An error occured",
                    "error": "missing key: worker_id or cannot find worker with this id",
                    "return_data": {}
                },
                status=400,
                content_type="application/json"
            )
        to_edit_keys = []
        for key, val in json_payload.items():
            old_val = worker[key]
            if key == "worker_name":
                if val != worker.name:
                    await worker.change_name(val)

            elif isinstance(val, list):
                worker[key] += val
            elif isinstance(val, dict):
                worker[key] = (worker[key] | val)
            else:
                worker[key] = val

            to_edit_keys.append(dict(key=key, old=old_val))

        update_req = await worker.update_db()

        edited_keys = []
        if update_req[0] is True:
            for edited_key in to_edit_keys:
                key = edited_key["key"]
                old = edited_key["old"]
                new = worker[key]

                if new != old:
                    edited_key["new"] = new
                    edited_keys.append(edited_key)

            return web.json_response(
                {
                    "status": "edited",
                    "error": "",
                    "return_data": edited_keys
                },
                status=201,
                content_type="application/json"
            )

        return web.json_response(
            {
                "status": "An error occured",
                "error": "unknow",
                "return_data": {}
            },
            status=500,
            content_type="application/json"
        )

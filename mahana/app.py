from configs.config import AppConfig, DatabaseConfig
from motor.motor_asyncio import AsyncIOMotorClient
from aiohttp import web

import jinja2
import aiohttp_jinja2

from web.views import (
    Home
)


class Mahana:
    def __init__(self):
        self.app = None

    def _setup_jinja(self):
        jinja_loader = jinja2.FileSystemLoader(str(AppConfig.APP_PATH.joinpath("web", "templates")))
        aiohttp_jinja2.setup(self.app, loader=jinja_loader)

    def _setup_routes(self):
        routes = web.RouteTableDef()

        self.app.router.add_view("/", Home)

        routes.static("/static", str(AppConfig.APP_PATH.joinpath("web", "static")), show_index=True)
        self.app.add_routes(routes)

    def _setup_mongo(self):
        mongo_db_client = AsyncIOMotorClient(DatabaseConfig.CONNECT_URI)[DatabaseConfig.BASE_DB]
        self.app["mongo"] = mongo_db_client


    def _setup(self):
        self.app = web.Application()

        self._setup_jinja()
        self._setup_routes()
        #self._setup_mongo()



    def start(self):
        self._setup()
        web.run_app(app=self.app, host=AppConfig.WEB_HOST, port=AppConfig.WEB_PORT)

import jinja2
import aiohttp_jinja2

from configs.config import AppConfig, DatabaseConfig
from motor.motor_asyncio import AsyncIOMotorClient
from aiohttp import web

from web.views import (
    HomeView,
    WorkerView
)

from classes import (
    Mongo
)


class Mahana:
    def __init__(self):
        self.app = None

    def _setup_jinja(self):
        jinja_loader = jinja2.FileSystemLoader(str(AppConfig.APP_PATH.joinpath("web", "templates")))
        aiohttp_jinja2.setup(self.app, loader=jinja_loader)

    def _setup_routes(self):
        routes = web.RouteTableDef()

        self.app.router.add_view("/", HomeView)
        self.app.router.add_view("/worker", WorkerView)

        routes.static("/static", str(AppConfig.APP_PATH.joinpath("web", "static")), show_index=True)
        self.app.add_routes(routes)

    def _setup_mongo(self):
        mongo_db_connection = AsyncIOMotorClient(DatabaseConfig.CONNECT_URI)
        mongo_obj = Mongo(mongo_client=mongo_db_connection)
        self.app["mongo_db"] = mongo_obj


    def _setup(self):
        self.app = web.Application()

        self._setup_jinja()
        self._setup_routes()
        self._setup_mongo()



    def start(self):
        self._setup()
        web.run_app(app=self.app, host=AppConfig.WEB_HOST, port=AppConfig.WEB_PORT)

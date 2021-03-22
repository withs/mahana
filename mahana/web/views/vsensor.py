import aiohttp_jinja2
from aiohttp import web

from rich import print


class SensorView(web.View):


    async def get(self):
        return {"Home": ":)"}


    async def put(self):
        """add a sensor"""


    async def patch(self):
        pass


    async def delete(self):
        pass

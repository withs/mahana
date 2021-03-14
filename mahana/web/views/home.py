import aiohttp_jinja2
from aiohttp import web


class Home(web.View):
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        return {"Home": ":)"}

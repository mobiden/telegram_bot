from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, querystring_schema


from app.garden.schemes import (
    FloraAddSchema,
    FloraTypeAddSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class FloraTypeAddView(AuthRequiredMixin, View):
    @request_schema(FloraTypeAddSchema)
    @response_schema(FloraTypeAddSchema)
    async def post(self):

        type = self.data["type"]
        existing_type = await self.store.store_flora.get_flora_type(type)
        if existing_type:
            raise HTTPConflict
        new_type = await self.store.store_flora.create_flora_type(type=type)

        return json_response(data=FloraTypeAddSchema().dump(new_type))


class FloraNameAddView(AuthRequiredMixin, View):
    @request_schema(FloraAddSchema)
    @response_schema(FloraAddSchema)
    async def post(self):

        name = self.data["name"]
        type = self.data["type"]
        planting_time = self.data["planting_time"]
        harvest_time = self.data["harvest_time"]
        existing_name = await self.store.store_flora.get_flora_by_name(name)
        if existing_name:
            raise HTTPConflict
        new_flora = await self.store.store_flora.create_flora(
            name=name,
            type=type,
            planting_time=planting_time,
            harvest_time=harvest_time,
        )
        return json_response(data=FloraAddSchema().dump(new_flora))


class Flora_Operation_AddView(AuthRequiredMixin, View):
    pass


from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest, HTTPMethodNotAllowed
from aiohttp_apispec import request_schema, response_schema, querystring_schema


from app.garden.schemes import (FloraAddSchema, FloraTypeSchema,)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class FloraTypeAddView(AuthRequiredMixin, View):
    @request_schema(FloraTypeSchema)
    @response_schema(FloraTypeSchema, 200)
    async def get(self):
        raise HTTPMethodNotAllowed

    async def post(self):
        flora_type = (await self.request.json())['flora_type']
       # flora_type = self.data["flora_type"]
        existing_type = await self.store.store_flora.get_flora_type(flora_type)
        if existing_type:
            raise HTTPConflict(reason='type was already added earlier')
        new_type = await self.store.store_flora.create_flora_type(type=flora_type)
        temp1 = FloraTypeSchema().dumps(new_type)
        temp2 = FloraTypeSchema().dump(new_type)
        return json_response(data=FloraTypeSchema().dump(new_type))


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


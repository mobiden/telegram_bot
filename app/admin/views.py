from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema, RegisterSchema, LoginSchema
from app.web.app import View
from aiohttp.web import HTTPForbidden, HTTPUnauthorized

from app.web.utils import json_response

# TODO: создавать нового админа и удалять по умолчанию
# TODO: добавить токенизацию


class AdminLoginView(View):
    @docs(tags=["admin"], summary="admin login")
    @request_schema(RegisterSchema)
    @response_schema(LoginSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        admin = await self.store.admins.get_admin_by_email(email)
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden
        admin_data = AdminSchema().dump(admin)
        response = json_response(data=admin_data)
        session = await new_session(request=self.request)
        session["token"] = await self.store.admins.get_token_by_admin_id(admin.id)
        return response


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if self.request.admin:
            return json_response(data=AdminSchema().dump(self.request.admin))
        raise HTTPUnauthorized

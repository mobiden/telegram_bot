from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema, RegisterSchema, LoginSchema
from app.store.admin.admin_accessor import AdminAccessor
from app.web.app import View
from aiohttp.web import HTTPForbidden, HTTPUnauthorized

from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response

# TODO: создавать нового админа и удалять по умолчанию
# TODO: добавить токенизацию


class AdminLoginView(View):
    @docs(tags=["admin"], summary="admin login")
    @request_schema(RegisterSchema)
    @response_schema(LoginSchema, 200)
    async def post(self):
        my_request = await self.request.json()
        email, password = self.data["email"], self.data["password"]
        admin = await self.store.admins.get_admin_by_email(email)
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden(reason='Wrong email or password')

        new_admin_session = await self.store.admins._create_admin_session(admin.id)
        response = json_response(data={"token": new_admin_session.adm_sess_token})
        #session = await new_session(request=self.request)
        #session["admin_id"] = await self.store.admins.get_token_by_admin_id(admin.id)
        return response


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if self.request.admin:
            return json_response(data=AdminSchema().dump(self.request.admin))
        raise HTTPUnauthorized


class AdminCreateView(AuthRequiredMixin, View):
    @request_schema(RegisterSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        if email and password:
            new_admin = await self.request.app.store.admins.create_admin(email, password)
            return json_response(data=AdminSchema().dump(new_admin))
        else:
            raise HTTPBadRequest(text='Need email with password')

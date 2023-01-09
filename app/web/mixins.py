from datetime import datetime

from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized

from app.admin.models import AdminModel, Admin_Session


class AuthRequiredMixin: #
    async def _iter(self) -> StreamResponse:
        if getattr(self.request, "token", None):
            request_token = await self.request.get('token')
            admin_session = await self.store.admins.get_admin_session_by_token(token=request_token)
            if not admin_session or admin_session.expires > datetime.now():
                    raise HTTPUnauthorized
        else:
            raise HTTPUnauthorized
        return await super(AuthRequiredMixin, self)._iter()

from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.future import select as f_select
from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized

from app.admin.models import AdminModel, Admin_Session
from app.web.middlewares import get_token


class AuthRequiredMixin:  #
    async def _iter(self) -> StreamResponse:
        token = get_token(self.request)
        if token:
            async with self.request.app.database.db_async_session() as db_session:
                web_session = await db_session.executive(f_select(Admin_Session).where(
                    and_(
                        Admin_Session.adm_sess_token == token,
                        Admin_Session.expires >= datetime.datetime.utcnow(),
                    )
                ).first())
            if web_session:
                self.request["admin_id"] = web_session.admin_id
            else:
                raise HTTPUnauthorized(reason='Invalid or obsolete token')
        else:
            raise HTTPUnauthorized(reason="There isn't token")

 #       if getattr(self.request, "token", None):
 #          request_token = await self.request.get("token")
 #           admin_session = await self.store.admins.get_admin_session_by_token(
 #               token=request_token)
 #           if not admin_session or admin_session.expires > datetime.now():
#                raise HTTPUnauthorized
 #       else:
 #           raise HTTPUnauthorized
        return await super(AuthRequiredMixin, self)._iter()

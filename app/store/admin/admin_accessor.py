import uuid
import datetime
from hashlib import sha256
from typing import Optional, Union, TYPE_CHECKING

from aiohttp.web_exceptions import HTTPForbidden
from sqlalchemy.future import select as f_select

from app.base.base_accessor import BaseAccessor
from app.admin.models import AdminModel, Admin_Session, AGE_DAYS
from app.web.utils import now

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):

    async def connect(self, app: "Application"):
        await super().connect(app)
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )


    async def get_admin_by_email(self, email: str) -> Optional[AdminModel]:

        async with self.app.database.db_async_session() as session:
            expect_admin = (
                await session.execute(
                    f_select(AdminModel).where(AdminModel.email == email)
                )
            ).scalar()
        if expect_admin:
            return expect_admin
        return None


    async def create_admin(self, email: str, password: str) -> AdminModel:
        admin = await self.get_admin_by_email(email)
        if not admin:
            async with self.app.database.db_async_session() as session:
                admin = AdminModel(
                    email=email,
                    password=sha256(password.encode("utf-8")).hexdigest(),
                )
                session.add(admin)
                await session.commit()
                _ = await self._create_admin_session(admin_id=admin.id)

        else:
            if admin.password != sha256(password.encode("utf-8")).hexdigest():
                raise HTTPForbidden
        return admin


    async def _create_admin_session(self, admin_id: Union[str, int]) -> Admin_Session:
        async with self.app.database.db_async_session() as db_session:
            admin_session = Admin_Session(
                admin_id=admin_id,
                adm_sess_token=str(uuid.uuid4().hex),
                created=now(),
                expires=now() + datetime.timedelta(days=AGE_DAYS),
                                )
            db_session.add(admin_session)
            await db_session.commit()
            return admin_session


    async def get_admin_session_by_token(self, token: str) -> Optional[Admin_Session]:

        async with self.app.database.db_async_session() as session:
            expect_session = (
                await session.execute(
                    f_select(Admin_Session).where(Admin_Session.adm_sess_token == token)
                )
            ).scalar()
        if expect_session:
            return expect_session
        return None

    async def get_token_by_admin_id(self, admin_id: int) -> Optional[str]:

        async with self.app.database.db_async_session() as session:
            admin_session = (
                await session.execute(
                    f_select(Admin_Session).where(Admin_Session.admin_id == admin_id)
                )
            ).scalar()
        if admin_session:
            return admin_session.adm_sess_token
        return None

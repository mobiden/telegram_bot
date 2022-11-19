import typing
from hashlib import sha256
from typing import Optional

from aiohttp.web_exceptions import HTTPForbidden
from sqlalchemy.future import select as f_select

from app.base.base_accessor import BaseAccessor
from app.admin.models import AdminModel

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await super().connect(app)
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )

    async def get_by_email(self, email: str) -> Optional[AdminModel]:

        async with  self.app.database.async_session() as session:
           expect_admin = (await session.execute(
                    f_select(AdminModel).where(AdminModel.email == email)
                                                 )).scalar()
        if expect_admin:
            return expect_admin
        return None

    async def create_admin(self, email: str, password: str) -> AdminModel:
        admin = await self.get_by_email(email)
        if not admin:
            async with self.app.database.async_session as session:
                admin = AdminModel(
                    email=email,
                    password=sha256(password.encode('utf-8')).hexdigest(),
                                    )
                session.add(admin)
                await session.commit()

        else:
            if admin.password != sha256(password.encode('utf-8')).hexdigest():
                raise HTTPForbidden
        return admin

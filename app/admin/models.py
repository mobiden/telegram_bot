import datetime
import uuid
from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import now

from app.store.database.sa_db import Sa_db

AGE_DAYS = 1


class AdminModel(Sa_db):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=True)

    def __repr__(self):
        return f'Admin - {self.email}'

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["AdminModel"]:
        return cls(
            id=session["admin"]["id"],
            email=session["admin"]["email"],
            password=session["admin"]["password"],
        )


class Admin_Session(Sa_db):
    __tablename__ = "admin_sessions"

    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)
    created = Column(DateTime(timezone=True), nullable=False)
    adm_sess_token = Column(String(32), primary_key=True)

    @classmethod
    async def generate(cls, admin_id):
        return await cls.create(
            admin_id=admin_id,
            adm_sess_token= str(uuid.uuid4().hex),
            created=now(),
            expires=now() + datetime.timedelta(days=cls.AGE_DAYS),
        )

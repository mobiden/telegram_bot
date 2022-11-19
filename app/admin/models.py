from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy import Column, Integer, String

from app.store.database.sa_db import sa_db as db, Sa_db


class AdminModel(Sa_db):
    __tablename__ = "admins"

    id = Column(Integer(), primary_key=True, autoincrement=True)
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

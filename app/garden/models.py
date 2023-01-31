from sqlalchemy import UniqueConstraint, Column, String, Integer, ForeignKey, Text

from app.store.database.sa_db import sa_db, Sa_db


from sqlalchemy import Enum

months = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "null")


class TypeModel(Sa_db):
    __tablename__ = "flora_types"
    type = Column(String(30), primary_key=True)


class FloraModel(Sa_db):
    __tablename__ = "floras"

    flora_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    type = Column(String(30), ForeignKey("flora_types.type"))
    planting_time = Column(Enum(*months, name="pl_months"), nullable=True)
    harvest_time = Column(Enum(*months, name="har_months"), nullable=True)
    __mapper_args__ = {"eager_defaults": True}


class GardenOperationModel(Sa_db):
    __tablename__ = "garden_operations"

    operation_id = Column(Integer, primary_key=True, autoincrement=True)
    operation_time = Column(Enum(*months, name="op_months"), nullable=True)
    flora = Column(String(100), ForeignKey("floras.name"), nullable=False)
    description = Column(Text, nullable=False)
    UniqueConstraint("operation_time", "flora", name="uniq_1")
    __mapper_args__ = {"eager_defaults": True}


class UserModel(Sa_db):
    __tablename__ = "users"

    id = Column(Integer(), nullable=False, autoincrement=True, primary_key=True)
    # email = db.Column(db.Unicode(), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)

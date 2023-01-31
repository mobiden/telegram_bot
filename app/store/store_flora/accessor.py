from typing import Optional, Callable

from sqlalchemy.future import select as f_select

from app.base.base_accessor import BaseAccessor
from app.garden.models import FloraModel, TypeModel, GardenOperationModel

from typing import List


# floras name
class FloraAccessor(BaseAccessor):
    async def create_flora(
        self,
        name: str,
        type: str,
        planting_time: Callable[[int], None],
        harvest_time: Callable[[int], None],
    ) -> FloraModel:
        async with self.app.database.db_async_session() as session:
            flora = FloraModel(
                name=name,
                type=type,
                planting_time=planting_time,
                harvest_time=harvest_time,
            )
            session.add(flora)
            await session.commit()
        return flora

    async def get_flora_by_name(self, name: str) -> Optional[FloraModel]:
        async with self.app.database.db_async_session() as session:
            return await session.execute(
                f_select(FloraModel).where(FloraModel.name == name).scalar()
            )

    async def flora_names_list(self, type: Optional[str] = None) -> List:
        async with self.app.database.db_async_session() as session:
            flora_list = await session.execute(f_select(FloraModel))
        filtred_flora_name_list = []
        if not type:
            for flora in flora_list.scalars():
                filtred_flora_name_list.append(flora.name.lower())
        else:
            for flora in flora_list.scalars():
                if (flora.type).lower() == type.lower():
                    filtred_flora_name_list.append(flora.name.lower())
        return filtred_flora_name_list

        # type

    async def get_flora_type(self, type: str) -> Optional[FloraModel]:
        async with self.app.database.db_async_session() as session:
            return await session.get(TypeModel, type)
            # return await session.execute(ilf_select(TypeModel).where(TypeModel.type == type).scalar())

    async def create_flora_type(self, type: str) -> TypeModel:
        async with self.app.database.db_async_session() as session:
            type = TypeModel(type=type)
            session.add(type)
            await session.commit()
            return type

    async def list_types(self) -> List:  # [TypeModel]:
        async with self.app.database.db_async_session() as session:
            types = await session.execute(f_select(TypeModel))
            list_types = []
            for type in types.scalars():
                list_types.append((type.type).lower())
            return list_types

            # operation

    async def create_operation(
        self, operation_time: str, flora: str, description: str
    ) -> GardenOperationModel:
        async with self.app.database.db_async_session() as session:
            operation = GardenOperationModel(
                operation_time=operation_time,
                flora=flora,
                description=description,
            )
            session.add(operation)
            await session.commit()
            return operation

    async def list_operations(self, flora: Optional[str]) -> List[GardenOperationModel]:
        async with self.app.database.db_async_session() as session:
            if flora:
                operations = await session.execute(
                    f_select(GardenOperationModel).where(
                        GardenOperationModel.flora.contains(flora)
                    )
                )
            else:
                operations = await session.execute(f_select(GardenOperationModel))
            list_of_oper = []
            for o in operations.scalars():
                list_of_oper.append(o)

            return list_of_oper

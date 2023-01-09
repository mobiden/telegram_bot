
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeMeta, sessionmaker


from app.admin.models import *
from app.garden.models import *
from sqlalchemy.engine.url import URL




class Database:
    db: Sa_db

    def __init__(self, app: "Application"):
        self.app = app
        self.db: Optional[Sa_db] = None
        self.db_async_session: Optional[AsyncSession] = None


    async def connect(self, *_, **kw):

        if self.app.config.database.db_name in 'postgresql+asyncpg':
            self._engine = create_async_engine(
            URL(
                drivername="postgresql+asyncpg",
                host=self.app.config.database.host,
                database=self.app.config.database.database,
                username=self.app.config.database.user,
                password=self.app.config.database.password,
                port=self.app.config.database.port,
            ),
                 echo=False,
                    )
        else:
            self._engine = create_async_engine(
                URL(
                    drivername="mysql+aiomysql", #TODO: fix with config
                    host=self.app.config.database.host,
                    database=self.app.config.database.database,
                    username=self.app.config.database.user,
                    password=self.app.config.database.password,
                    port=self.app.config.database.port,
                ),
                   echo=False,
            )

        self.db = sa_db
        self.db.bind = self._engine

        async with self._engine.begin() as conn:
    #        await conn.run_sync(self.db.metadata.drop_all)
            await conn.run_sync(self.db.metadata.create_all)

        self.db_async_session = sessionmaker(bind=self._engine, expire_on_commit=False,
                                             class_=AsyncSession)

    async def disconnect(self, *_, **kw):
        self.app = None
        await sa_db.pop_bind().close()


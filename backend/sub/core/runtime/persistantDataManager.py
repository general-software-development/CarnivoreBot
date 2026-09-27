from sub.core.starttime.assetManager import AssetManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import TYPE_CHECKING

target_path = AssetManager.paths.rootPath / ".data" / "latest.sqlite3.db"
target_path.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{target_path}")
async_engine = create_async_engine(f"sqlite+aiosqlite:///{target_path}")

from typing import Any
type GodKnowsWhat = Any

class PersistentDataManager:
    if TYPE_CHECKING:
        execute = Session.execute
        add = Session.add
        add_all = Session.add_all
        delete = Session.delete
        flush = Session.flush
        scalar = Session.scalar
        scalars = Session.scalars

    def __init__(self, expire_on_commit: bool = False):
        self._conn = engine.connect()
        self._session = Session(bind=self._conn, expire_on_commit=expire_on_commit)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.close()

    @property
    def session(self):
        return self._session

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    def close(self, commit: bool = False):
        if commit:
            self.commit()
        self._session.close()
        self._conn.close()

    def __getattr__(self, name: str) -> GodKnowsWhat:
        try:
            return getattr(self.session, name)
        except AttributeError:
            return getattr(self._conn, name)

class APersistentDataManager:
    if TYPE_CHECKING:
        execute = Session.execute
        add = Session.add
        add_all = Session.add_all
        delete = Session.delete
        flush = Session.flush
        scalar = Session.scalar
        scalars = Session.scalars

    def __init__(self, expire_on_commit: bool = False):
        self._conn = async_engine.connect()
        self._session = None
        self.configs_expire_on_commit = expire_on_commit

    async def start(self):
        await self._conn.start()
        self._session = AsyncSession(bind=self._conn, expire_on_commit=self.configs_expire_on_commit)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    @property
    def session(self):
        return self._session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self, commit: bool = False):
        if commit:
            await self.commit()
        await self._session.close()
        await self._conn.close()

    def __getattr__(self, name: str) -> GodKnowsWhat:
        try:
            return getattr(self.session, name)
        except AttributeError:
            return getattr(self._conn, name)

from sub.core.starttime.assetManager import AssetManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

target_path = AssetManager.paths.rootPath / ".data" / "latest.sqlite3.db"
target_path.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{target_path}")

class PersistentDataManager:
    def __init__(self):
        self._conn = engine.connect()
        self._session = Session(bind=self._conn)

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

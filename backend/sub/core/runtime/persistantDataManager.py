from typing import Literal
from sub.core.starttime.assetManager import AssetManager
from pathlib import Path
import sqlite3

class PersistentDataManager:
    def __init__(self, subsystem: str):
        target_path = AssetManager.paths.rootPath / ".data" / (subsystem + ".sql3.db")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(target_path, isolation_level=None)
        self._cursor = self._conn.cursor()

    def begin(self, mode: Literal["DEFERRED", "IMMEDIATE", "EXCLUSIVE"] = 'IMMEDIATE') -> sqlite3.Cursor:
        self._cursor.execute(f"BEGIN {mode};")
        return self._cursor

    def commit(self):
        self._conn.commit()

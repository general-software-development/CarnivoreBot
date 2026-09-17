from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import orm
import sqlalchemy as sqla
import uuid

class SQLServerConfigBase(DeclarativeBase):
    pass

class ServerConfig(SQLServerConfigBase):
    __tablename__ = "feat:serverConfig"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(sqla.Uuid(), primary_key=True, default=uuid.uuid7)
    server_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer(), nullable=False)
    key_name: orm.Mapped[str] = orm.mapped_column(sqla.String(50), nullable=False)
    value: orm.Mapped[str] = orm.mapped_column(sqla.String(500), nullable=True)

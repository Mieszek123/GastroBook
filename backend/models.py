from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from .database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Automatycznie przez fastapiusers, nie zmieniaj nic"""

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from fastapi_users_db_sqlalchemy.generics import GUID

from .database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    phone_number = Column(String, nullable=False, unique=True)

class Tables(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False, default=1)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    user_id = Column(GUID, ForeignKey("user.id"),nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="pending")
from datetime import datetime
from typing import Optional
import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    phone_number: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    phone_number: str


class UserUpdate(schemas.BaseUserUpdate):
    phone_number: Optional[str] = None

# ----------

class TableResponse(BaseModel):
    id: int
    number: int
    size: int
    available: int

# ----------

class ReservationCreate(BaseModel):
    table_id: int
    start_at: datetime
    end_at: datetime

class ReservationResponse(BaseModel):
    id: int
    table_id: int
    user_id: uuid.UUID
    start_at: datetime
    end_at: datetime
    status: str


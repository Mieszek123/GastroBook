from datetime import datetime
from typing import Optional
import uuid

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    phone_number: Optional[str] = None
    verification_code: Optional[int] = None
    verification_code_expires: Optional[datetime] = None


class UserCreate(schemas.BaseUserCreate):
    phone_number: str
    verification_code: Optional[int] = None
    verification_code_expires: Optional[datetime] = None


class UserUpdate(schemas.BaseUserUpdate):
    phone_number: Optional[str] = None
    verification_code: Optional[int] = None
    verification_code_expires: Optional[datetime] = None


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: int
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


from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from .users import UserManager, get_user_manager

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/verify_code")
async def verify_code(email: EmailStr, code: int, user_manager: UserManager = Depends(get_user_manager)):
    pass
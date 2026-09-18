from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr

from .users import UserManager, get_user_manager

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/verify_code")
async def verify_code(
    email: EmailStr,
    code: int,
    user_manager: UserManager = Depends(get_user_manager),
):
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    user = await user_manager.get_by_email(email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    saved_code = getattr(user, "verification_code", None)
    expires_at = getattr(user, "verification_code_expires", None)

    if saved_code is None:
        raise HTTPException(status_code=400, detail="No verification code for this user")

    if expires_at is not None and expires_at < now_utc:  
        raise HTTPException(status_code=400, detail="Verification code expired")

    if saved_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await user_manager.user_db.update(
        user,
        {
            "verification_code": None,
            "verification_code_expires": None,
            "is_verified": True,
        },
    )

    return {"valid": True, "message": "Verification code is valid"}

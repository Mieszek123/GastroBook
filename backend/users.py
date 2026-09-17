import os
import uuid
import resend
import random
from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from .database import get_user_db
from .models import User

JWT_SECRET = os.getenv("JWT_SECRET")
resend.api_key = os.getenv("RESEND_API_KEY")

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = JWT_SECRET
    verification_token_secret = JWT_SECRET

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        code = f"{random.randint(0, 999999):06d}"
        code = int(code)

        await self.user_db.update(user, {
        "verification_code": code,
        "verification_code_expires": datetime.now(timezone.utc) + timedelta(minutes=15)
    })
        resend.Emails.send({
            "from": "GastroBook <noreply@mieszek.dev>",
            "to": user.email,
            "template": {
                "id": "welcome-gastrobook",
                "variables": {
                    "first_name": user.email,
                    "verification_code": code
                }
            }
        })


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=60 * 60 * 24)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)



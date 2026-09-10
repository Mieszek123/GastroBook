from fastapi import APIRouter, Depends

from .users import current_active_user

router = APIRouter(prefix="/api")


@router.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Checks whether the API is running."""
    return {"status": "ok"}


@router.get("/restaurants/", tags=["restaurants"])
async def list_restaurants() -> list[dict[str, str]]:
    """Temporary endpoint; later it will return restaurants from the database."""
    return []


@router.get("/reservations/", tags=["reservations"])
async def list_reservations(
    user=Depends(current_active_user),
) -> list[dict[str, str]]:
    """Temporary protected endpoint; it requires a logged-in user."""
    return []

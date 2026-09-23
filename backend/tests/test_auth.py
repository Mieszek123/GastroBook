# tests/test_auth.py
import pytest
from sqlalchemy import select
from backend.models import User

def test_register(client):
    response = client.post("/auth/register", json={
        "email": "testowy@mieszek.dev",
        "password": "123455678890",
        "phone_number": "123456789",
    })
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201


def test_login(client):
    # najpierw rejestrujemy usera WEWNĄTRZ tego testu,
    # bo baza jest pusta i nie może polegać na innym teście
    client.post("/auth/register", json={
        "email": "testowy@mieszek.dev",
        "password": "haslo123",
        "phone_number": "111222333",
    })

    response = client.post("/auth/jwt/login", data={
        "username": "testowy@mieszek.dev",
        "password": "haslo123"
    })
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_verify_code(client, db_session):
    client.post("/auth/register", json={
        "email": "testownik@mieszek.dev",
        "password": "haslo123",
        "phone_number": "987654321",
    })

    result = await db_session.execute(
        select(User).where(User.email == "testownik@mieszek.dev")
    )
    user = result.scalar_one()
    ver_code = user.verification_code

    print(f"Kod z bazy: {ver_code}")

    response = client.post("/auth/verify_code", json={
        "email": "testownik@mieszek.dev",
        "code": ver_code
    })

    db_session.expire_all()

    result = await db_session.execute(
        select(User).where(User.email == "testownik@mieszek.dev")
    )
    updated_user = result.scalar_one()

    assert updated_user.is_verified is True

    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
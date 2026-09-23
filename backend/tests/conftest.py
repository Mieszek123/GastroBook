import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.main import app
from backend.database import Base, get_async_session
from backend import models  # WAŻNE: importujemy modele, żeby Base "wiedziała" o tabelach

# osobna baza tylko do testów
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session


# podmieniamy prawdziwą bazę na testową dla całej aplikacji
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    # tworzy świeże tabele przed każdym testem
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # i czyści wszystko po teście
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client():
    return TestClient(app)

import resend

@pytest.fixture(autouse=True)
def mock_resend_email(monkeypatch):
    def fake_send(params):
        print(f"MOCK: mail 'wysłany' do {params.get('to')} (nic realnie nie poleciało)")
        return {"id": "fake-email-id"}
    
    monkeypatch.setattr(resend.Emails, "send", fake_send)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
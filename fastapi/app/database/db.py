from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgresql@db:5432/usersdb"
)


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


"""
    init_db() → run once at app startup (create tables in dev, maybe seed data).
    get_session() → per-request dependency that yields an AsyncSession. Use Depends(get_session) in route functions.
    Put init_db() in the app lifespan / startup (not inside request dependencies).
    For production migrations use Alembic — init_db() is fine only for local/dev convenience.
    
    Why init_db() is not a session dependency
    init_db() typically runs await engine.begin(); await conn.run_sync(SQLModel.metadata.create_all). It creates schema, not a live AsyncSession.
    If you wired init_db() as a dependency (e.g. session = Depends(init_db)), it would:
    Run schema-creation on every request (terrible performance, incorrect semantics).
    Not yield an AsyncSession object for queries — so your code that expects a session would break.
    Session lifecycle must be per-request (open/close per request) to avoid connection leaks. init_db() is a one-time startup action.
"""


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """
    Create database tables from SQLModel metadata.
    Run this at startup for dev, or run migrations with Alembic in production.
    Call this once to create tables when running locally (not for alembic migrations)
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgresql")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv(
    "POSTGRES_DB", "usersdb"
)  # ِnew database that we want to be creatd


async def create_database():
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database="postgres",
        port=POSTGRES_PORT,
    )

    db_exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname=$1", POSTGRES_DB
    )

    if not db_exists:
        await conn.execute(f'CREATE DATABASE "{POSTGRES_DB}"')
        print(f"Database '{POSTGRES_DB}' created successfully!")
    else:
        print(f"Database '{POSTGRES_DB}' already exists.")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(create_database())

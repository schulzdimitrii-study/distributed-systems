import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


async def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    return await asyncpg.connect(database_url)

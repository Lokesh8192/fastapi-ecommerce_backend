from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("ALTER TYPE orderstatus ADD VALUE IF NOT EXISTS 'RETURNED'"))
    print('orderstatus enum updated')

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from src.config import settings

engine = create_async_engine(
    settings.DB_URL,
    echo=True,
    # pool_pre_ping=True,
    # pool_recycle=600,
    # connect_args={
    #     "keepalives": 1,
    #     "keepalives_idle": 30,
    #     "keepalives_interval": 10,
    #     "keepalives_count": 5,
    # }
)
engine_np = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_np = async_sessionmaker(bind=engine_np, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

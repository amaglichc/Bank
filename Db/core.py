from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from Config import db_config

Base = declarative_base()
engine = create_async_engine(url=db_config.url, echo=True)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False)

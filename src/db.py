import os
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, create_engine,
    LargeBinary, DateTime, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import ConfigParametersDatabase

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    generate_token = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)

    users = relationship("User", back_populates="profile")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    token_exp_minutes = Column(Integer, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), index=True, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    profile = relationship("Profile", back_populates="users", lazy="joined")  # otimizado para acesso conjunto
    tokens = relationship("UserToken", back_populates="user", cascade="all, delete-orphan")

class UserToken(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    token = Column(String, nullable=False)
    generated_at = Column(DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")), nullable=False)

    user = relationship("User", back_populates="tokens")

    __table_args__ = (
        Index("idx_user_token", "user_id", "token"),  # índice composto para performance
    )

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    http_status = Column(Integer, nullable=False)
    requested_at = Column(DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")), nullable=False)

os.makedirs(ConfigParametersDatabase.LOCAL_DB, exist_ok=True)

engine = create_engine(
    ConfigParametersDatabase.URI_CONNECTION,
    pool_size=ConfigParametersDatabase.POOL_SIZE,
    max_overflow=ConfigParametersDatabase.MAX_OVERFLOW,
    pool_timeout=ConfigParametersDatabase.POOL_TIMEOUT,
    pool_recycle=ConfigParametersDatabase.POOL_RECYCLE
)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

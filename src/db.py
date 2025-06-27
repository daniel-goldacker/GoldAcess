import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import ConfigParametersDatabase

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    generate_token = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="profile")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(LargeBinary)
    token_exp_minutes = Column(Integer)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    is_visible = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="users")

# Configuração e criação das tabelas
os.makedirs(ConfigParametersDatabase.LOCAL_DB, exist_ok=True)
engine = create_engine(ConfigParametersDatabase.URI_CONNECTION)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

from sqlalchemy import Column, Integer, String, create_engine, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import ConfigParametersApplication, ConfigParametersDatabase
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(LargeBinary)
    token_exp_minutes = Column(Integer)
    profile = Column(String, default="user")  # Novo campo perfil com valor padrão "user"

engine = create_engine(ConfigParametersDatabase.DATABASE)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

def create_admin_user():
    session = SessionLocal()
    admin = session.query(User).filter_by(username=ConfigParametersApplication.NAME_ADMIN).first()
    if not admin:
        hashed_pw = bcrypt.hashpw(ConfigParametersApplication.PASSWORD_ADMIN.encode(), bcrypt.gensalt())
        admin_user = User(
            username=ConfigParametersApplication.NAME_ADMIN,
            password=hashed_pw,
            token_exp_minutes=ConfigParametersApplication.TOKEN_EXP_MINUTES_ADMIN,
            profile=ConfigParametersApplication.PROFILE_ADMIN
        )
        session.add(admin_user)
        session.commit()
    else:
        session.close()

# Executa a criação do admin na inicialização do módulo
create_admin_user()

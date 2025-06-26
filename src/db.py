from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import ConfigParametersAdmin, ConfigParametersDatabase
import bcrypt

Base = declarative_base()

# Tabela de perfis
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    generate_token = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="profile")

# Tabela de usuários
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
engine = create_engine(ConfigParametersDatabase.DATABASE)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

# Criar perfis
def create_profiles():
    session = SessionLocal()
    is_admin_profile = session.query(Profile).filter_by(name=ConfigParametersAdmin.PROFILE_ADMIN).first()
    if not is_admin_profile:
        is_admin_profile = Profile(
            name=ConfigParametersAdmin.PROFILE_ADMIN,
            generate_token=False,
            is_admin=True,
            is_visible=False
        )
        session.add(is_admin_profile)
        session.commit()
    session.close()
    

# Criar usuário admin
def create_admin_user():
    session = SessionLocal()
    create_profiles()
    is_admin_profile = session.query(Profile).filter_by(name=ConfigParametersAdmin.PROFILE_ADMIN).first()

    is_admin = session.query(User).filter_by(username=ConfigParametersAdmin.NAME_ADMIN).first()
    if not is_admin:
        hashed_pw = bcrypt.hashpw(ConfigParametersAdmin.PASSWORD_ADMIN.encode(), bcrypt.gensalt())
        is_admin_user = User(
            username=ConfigParametersAdmin.NAME_ADMIN,
            password=hashed_pw,
            token_exp_minutes=ConfigParametersAdmin.TOKEN_EXP_MINUTES_ADMIN,
            profile_id=is_admin_profile.id,
            is_visible=False,
            is_active = True
        )
        session.add(is_admin_user)
        session.commit()
    session.close()

# Executa na inicialização
create_admin_user()

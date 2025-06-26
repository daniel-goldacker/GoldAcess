import bcrypt
from db import SessionLocal, User
from sqlalchemy.orm import joinedload
from typing import Optional
from config import ConfigParametersApplication

def add_user(username: str, password: str, token_exp_minutes: int, profile_id: int, is_visible: bool, is_active: bool):
    session = SessionLocal()
    try: 
        existing = session.query(User).filter_by(username=username).first()
        if existing:
           raise ValueError("Usuário já existente!")
    
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        user = User(
            username=username,
            password=hashed_pw,
            token_exp_minutes=token_exp_minutes,
            profile_id=profile_id,
            is_visible=is_visible,
            is_active=is_active
        )
        
        session.add(user)
        session.commit()
        return True, "Usuário criado com sucesso."
    finally:
        session.close()


def update_user(user_id: int, new_password: Optional[str] = None,
                new_token_exp_minutes: Optional[int] = None,
                new_profile_id: Optional[int] = None,
                new_is_visible: Optional[bool] = None,
                new_is_active: Optional[bool] = None,):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("Usuário não encontrado.")

        if new_password:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            user.password = hashed_pw

        if new_token_exp_minutes is not None:
            user.token_exp_minutes = new_token_exp_minutes

        if new_profile_id is not None:
            user.profile_id = new_profile_id

        if new_is_visible is not None:
            user.is_visible = new_is_visible

        if new_is_active is not None:
            user.is_active = new_is_active

        session.commit()
        return True, "Usuário atualizado com sucesso."
    finally:
        session.close()

def delete_user(user_id: int):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Usuário não encontrado.")
        
        session.delete(user)
        session.commit()
        return True, "Usuário excluído com sucesso."
    finally:
        session.close()

def get_all_users(profile_logged: str):
    session = SessionLocal()
    try:
        if profile_logged == ConfigParametersApplication.PROFILE_SISTEMA: 
            users = session.query(User).options(joinedload(User.profile)).all()
        else:    
            users = session.query(User).options(joinedload(User.profile)).filter(User.is_visible == True).all()

        return users
    finally:
        session.close()

def authenticate(username: str, password: str):
    session = SessionLocal()
    try: 
        user = session.query(User).filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode(), user.password):
            return user
        else:
            return False
    finally:
        session.close()

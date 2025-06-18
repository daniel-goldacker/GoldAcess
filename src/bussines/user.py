import bcrypt
from db import SessionLocal, User
from sqlalchemy.orm import joinedload
from typing import Optional

def add_user(username: str, password: str, token_exp_minutes: int, profile_id: int, visible: bool):
    session = SessionLocal()
    try: 
        existing = session.query(User).filter_by(username=username).first()
        if existing:
            return False, "Perfil já existe!"
    
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        user = User(
            username=username,
            password=hashed_pw,
            token_exp_minutes=token_exp_minutes,
            profile_id=profile_id,
            visible=visible
        )
        
        session.add(user)
        session.commit()
        return True, "Usuário criado com sucesso."
    finally:
        session.close()


def update_user(user_id: int, new_password: Optional[str] = None,
                     new_token_exp_minutes: Optional[int] = None,
                     new_profile_id: Optional[int] = None,
                     new_visible: Optional[bool] = None):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return False, "Usuário não encontrado."

        if new_password:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            user.password = hashed_pw

        if new_token_exp_minutes is not None:
            user.token_exp_minutes = new_token_exp_minutes

        if new_profile_id is not None:
            user.profile_id = new_profile_id
        if new_visible is not None:
            user.visible = new_visible

        session.commit()
        return True, "Usuário atualizado com sucesso."
    finally:
        session.close()

def delete_user(user_id: int):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "Usuário não encontrado."
        
        session.delete(user)
        session.commit()
        return True, "Usuário excluído com sucesso."
    finally:
        session.close()

def get_all_users():
    session = SessionLocal()
    try:
        users = session.query(User).options(joinedload(User.profile)).all()
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

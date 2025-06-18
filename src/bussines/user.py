import bcrypt
from db import SessionLocal, User
from sqlalchemy.orm import joinedload
from typing import Optional

def create_user(username: str, password: str, token_exp_minutes: int, profile_id: int):
    db = SessionLocal()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    user = User(
        username=username,
        password=hashed_pw,
        token_exp_minutes=token_exp_minutes,
        profile_id=profile_id  # <- Usar profile_id diretamente
    )
    
    db.add(user)
    db.commit()
    db.close()


def update_user(username: str, new_password: Optional[str] = None,
                     new_token_exp_minutes: Optional[int] = None,
                     new_profile_id: Optional[int] = None):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False

        if new_password:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            user.password = hashed_pw

        if new_token_exp_minutes is not None:
            user.token_exp_minutes = new_token_exp_minutes

        if new_profile_id is not None:
            user.profile_id = new_profile_id

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_user(username: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()

def get_all_users():
    session = SessionLocal()
    users = session.query(User).options(joinedload(User.profile)).all()
    session.close()
    
    return users

def authenticate(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and bcrypt.checkpw(password.encode(), user.password):
        return user
    return None
import bcrypt
import jwt
from datetime import datetime, timedelta
from db import SessionLocal, User
from config import ConfigParametersSecurity
from sqlalchemy.orm import joinedload



def authenticate(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and bcrypt.checkpw(password.encode(), user.password):  # <-- aqui está a correção
        return user
    return None

def generate_token(user: User):
    exp = datetime.utcnow() + timedelta(minutes=user.token_exp_minutes)
    payload = {
        "sub": user.username,
        "exp": exp,
    }
    return jwt.encode(payload, ConfigParametersSecurity.SECRET_KEY, algorithm=ConfigParametersSecurity.ALGORITHMS_CRYPTOGRAPHY)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, ConfigParametersSecurity.SECRET_KEY, algorithms=[ConfigParametersSecurity.ALGORITHMS_CRYPTOGRAPHY])
        return {"valid": True, "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "reason": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"valid": False, "reason": "Token inválido"}

def update_password(username, new_password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    if user:
        user.password = hashed_pw
        session.commit()
    session.close()

def update_token(username, new_token_exp_minutes):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if user:
        user.token_exp_minutes = new_token_exp_minutes
        session.commit()
    session.close()

def update_profile(username, new_profile_id):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if user:
        user.profile_id = new_profile_id
        session.commit()
    session.close()

def delete_user(username):
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

    return users

def authenticate(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and bcrypt.checkpw(password.encode(), user.password):
        return user
    return None
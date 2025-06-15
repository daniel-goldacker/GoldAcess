import bcrypt
import jwt
from datetime import datetime, timedelta
from db import SessionLocal, User

SECRET_KEY = "segredo_super_secreto"

def create_user(username, password, token_exp_minutes, profile):
    db = SessionLocal()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(username=username, password=hashed_pw, profile=profile, token_exp_minutes=token_exp_minutes)
    db.add(user)
    db.commit()
    db.close()

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
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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

def update_profile(username, new_profile):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if user:
        user.profile = new_profile
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
    users = session.query(User).all()
    session.close()

    return users

def authenticate(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and bcrypt.checkpw(password.encode(), user.password):
        if user.profile in ("Sistema", "Administrador"):
            return True
    return False
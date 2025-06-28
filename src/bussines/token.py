
import jwt
import pandas as pd
from datetime import datetime, timedelta
from db import SessionLocal, User, UserToken
from config import ConfigParametersSecurity
from sqlalchemy.orm import joinedload


def generate_token(user: User):
    exp = datetime.utcnow() + timedelta(minutes=user.token_exp_minutes)
    payload = {
        "sub": user.username,
        "exp": exp,
    }

    tokeJWT = jwt.encode(payload, ConfigParametersSecurity.SECRET_KEY, algorithm=ConfigParametersSecurity.ALGORITHMS_CRYPTOGRAPHY)
    store_token(user, tokeJWT)
    
    return tokeJWT

def get_all_tokens():
    session = SessionLocal()
    try: 
        tokens = session.query(UserToken).options(joinedload(UserToken.user)).all()
        data = [
            {"Usuário": token.user.username, "Data": token.created_at.date()}
            for token in tokens if token.created_at
        ]        
        return pd.DataFrame(data)
    finally:
        session.close()
    

def verify_token(token: str):
    try:
        payload = jwt.decode(token, ConfigParametersSecurity.SECRET_KEY, algorithms=[ConfigParametersSecurity.ALGORITHMS_CRYPTOGRAPHY])
        return {"valid": True, "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "reason": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"valid": False, "reason": "Token inválido"}


def store_token(user, token):
    session = SessionLocal()
    try: 
        user_token = UserToken(user_id=user.id, token=token)
        session.add(user_token)
        session.commit()
        return True, "Usuário criado com sucesso."
    finally:
        session.close()






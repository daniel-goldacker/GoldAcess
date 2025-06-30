
import jwt
import pandas as pd
from datetime import datetime, timedelta
from db import SessionLocal, User, UserToken, RequestLog
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
            {"Usuário": token.user.username, "Data": token.generated_at.date()}
            for token in tokens if token.generated_at
        ]        
        return pd.DataFrame(data)
    finally:
        session.close()
    

def get_all_request_logs():
    session = SessionLocal()
    try:
        logs = session.query(RequestLog).all()
        data = [
            {"Data": log.requested_at.date(), "Status HTTP": log.http_status}
            for log in logs
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
    finally:
        session.close()

def store_request_logs(http_status):
    session = SessionLocal()
    try: 
        request_logs = RequestLog(http_status=http_status)
        session.add(request_logs)
        session.commit()
    finally:
        session.close()







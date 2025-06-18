
import jwt
from datetime import datetime, timedelta
from db import  User
from config import ConfigParametersSecurity


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

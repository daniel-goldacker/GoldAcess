import bcrypt
from db import SessionLocal, User

def create_user(username, password, token_exp_minutes, profile_id):
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

from sqlalchemy.orm import Session
from db import SessionLocal, Profile

def get_profiles(profile_id:int):
    session = SessionLocal()
    try:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            return False, "Perfil não encontrado."
        return profile
    finally:
        session.close()

def add_profile(name: str, generate_token: bool, admin: bool, visible: bool):
    session = SessionLocal()
    try:
        existing = session.query(Profile).filter_by(name=name).first()
        if existing:
            return False, "Perfil já existe!"
        profile = Profile(name=name, generate_token=generate_token, admin=admin, visible=visible)
        session.add(profile)
        session.commit()
        return True, "Perfil criado com sucesso."
    finally:
        session.close()

def update_profile(profile_id: int, generate_token: bool, admin: bool, visible: bool):
    session = SessionLocal()
    try:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            return False, "Perfil não encontrado."
        profile.generate_token = generate_token
        profile.admin = admin
        profile.visible = visible
        session.commit()
        return True, "Perfil atualizado com sucesso."
    finally:
        session.close()

def delete_profile(profile_id: int):
    session = SessionLocal()
    try:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            return False, "Perfil não encontrado."
        session.delete(profile)
        session.commit()
        return True, "Perfil excluído com sucesso."
    finally:
        session.close()

def get_all_profiles():
    session = SessionLocal()
    try:
        profiles = session.query(Profile).all()
        return profiles
    finally:
        session.close()

 
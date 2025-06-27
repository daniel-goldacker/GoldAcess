from db import SessionLocal, Profile
from config import ConfigParametersApplication
from bussines.user import user_has_profile

def get_profiles(profile_id:int):
    session = SessionLocal()
    try:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            raise ValueError("Perfil não encontrado.")
        return profile
    finally:
        session.close()

def add_profile(name: str, generate_token: bool, is_admin: bool, is_visible: bool):
    session = SessionLocal()
    try:
        existing = session.query(Profile).filter_by(name=name).first()
        if existing:
            raise ValueError("Perfil já existe!")
        profile = Profile(name=name, generate_token=generate_token, is_admin=is_admin, is_visible=is_visible)
        session.add(profile)
        session.commit()
        return True, "Perfil criado com sucesso."
    finally:
        session.close()

def update_profile(profile_id: int, generate_token: bool, is_admin: bool, is_visible: bool):
    session = SessionLocal()
    try:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            raise ValueError("Perfil não encontrado.")

        profile.generate_token = generate_token
        profile.is_admin = is_admin
        profile.is_visible = is_visible
        session.commit()
        return True, "Perfil atualizado com sucesso."
    finally:
        session.close()

def delete_profile(profile_id: int):
    session = SessionLocal()
    try:
        profile = session.query(Profile).filter_by(id=profile_id).first()
        if not profile:
            raise ValueError("Perfil não encontrado.")
        
        if user_has_profile(profile_id):
            raise ValueError("Perfil está sendo utilizado por um usuário.")
        
        session.delete(profile)
        session.commit()
        return True, "Perfil excluído com sucesso."
    finally:
        session.close()

def get_all_profiles(profile_logged: str):
    session = SessionLocal()
    try:
        if profile_logged == ConfigParametersApplication.PROFILE_SISTEMA: 
            profiles = session.query(Profile).all()  
        else:     
            profiles = session.query(Profile).filter(Profile.is_visible == True).all()    
        
        return profiles
    finally:
        session.close()

def get_default_profile():
    session = SessionLocal()
    try:
        is_default_profile = session.query(Profile).filter_by(name=ConfigParametersApplication.PROFILE_PADRAO).first()

        return is_default_profile.id   
    finally:
        session.close()
 
def create_default_profiles():
    session = SessionLocal()
    is_admin_profile = session.query(Profile).filter_by(name=ConfigParametersApplication.PROFILE_SISTEMA).first()
    if not is_admin_profile:
        is_admin_profile = Profile(
            name=ConfigParametersApplication.PROFILE_SISTEMA,
            generate_token=False,
            is_admin=True,
            is_visible=False
        )
        session.add(is_admin_profile)

        is_default_profile = Profile(
            name=ConfigParametersApplication.PROFILE_PADRAO,
            generate_token=False,
            is_admin=False,
            is_visible=False
        )
        session.add(is_default_profile)

        session.commit()
    session.close()
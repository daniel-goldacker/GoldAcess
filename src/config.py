from dotenv import load_dotenv
import os

load_dotenv()

class ConfigParametersAdmin():
    NAME_ADMIN = os.getenv('NAME_ADMIN')
    PASSWORD_ADMIN = os.getenv('PASSWORD_ADMIN')
    PROFILE_ADMIN = os.getenv('PROFILE_ADMIN')
    TOKEN_EXP_MINUTES_ADMIN = os.getenv('TOKEN_EXP_MINUTES_ADMIN')

class ConfigParametersApplication():
    DEFAULT_EXP_MINUTES = 60
    DEFAULT_PROFILE = "APIs"
   
class ConfigParametersDatabase():    
    DATABASE = 'sqlite:///database/database.db'

class ConfigParametersSecurity():
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHMS_CRYPTOGRAPHY = os.getenv('ALGORITHMS_CRYPTOGRAPHY')
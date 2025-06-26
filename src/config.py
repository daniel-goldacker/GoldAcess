from dotenv import load_dotenv
import os

load_dotenv()

class ConfigParametersAdmin():
    NAME_ADMIN = os.getenv('NAME_ADMIN')
    PASSWORD_ADMIN = os.getenv('PASSWORD_ADMIN')
    TOKEN_EXP_MINUTES_ADMIN = os.getenv('TOKEN_EXP_MINUTES_ADMIN')    
    
class ConfigParametersApplication():
    PROFILE_PADRAO = os.getenv('PROFILE_PADRAO')
    PROFILE_SISTEMA = os.getenv('PROFILE_SISTEMA')
    TOKEN_EXP_MINUTES_AUTOMATIC_USER_CREATION = os.getenv('TOKEN_EXP_MINUTES_AUTOMATIC_USER_CREATION')
    TOKEN_EXP_MINUTES_NEW_USER = 60
    DEFAULT_TIME_SLEEP = 2
   
class ConfigParametersDatabase():    
    DATABASE = 'sqlite:///database/database.db'

class ConfigParametersSecurity():
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHMS_CRYPTOGRAPHY = os.getenv('ALGORITHMS_CRYPTOGRAPHY')
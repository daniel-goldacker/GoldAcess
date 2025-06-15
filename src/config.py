from dotenv import load_dotenv
import os

load_dotenv()

class ConfigParametersApplication():
    NAME_ADMIN = os.getenv('NAME_ADMIN')
    PASSWORD_ADMIN = os.getenv('PASSWORD_ADMIN')
    PROFILE_ADMIN = os.getenv('PROFILE_ADMIN')
    TOKEN_EXP_MINUTES_ADMIN = os.getenv('TOKEN_EXP_MINUTES_ADMIN')
    
class ConfigParametersDatabase():    
    DATABASE = 'sqlite:///database/database.db'
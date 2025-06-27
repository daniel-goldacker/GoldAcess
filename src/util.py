import time
import base64
from config import ConfigParametersApplication

def time_sleep():
    time.sleep(ConfigParametersApplication.DEFAULT_TIME_SLEEP)

def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
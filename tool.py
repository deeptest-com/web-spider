import os
from dotenv import load_dotenv, find_dotenv

def get_nancal_cloud_url():
    _ = load_dotenv(find_dotenv())

    key = 'NANCAL_CLOUD_URL'

    return os.environ[key]


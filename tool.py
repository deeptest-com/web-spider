import os
from dotenv import load_dotenv, find_dotenv

def get_wiki_url():
    _ = load_dotenv(find_dotenv())

    return os.environ["WIKI_URL"]


import os
from dotenv import load_dotenv, find_dotenv

def get_wiki_url():
    _ = load_dotenv(find_dotenv())

    return os.environ["WIKI_URL"]

def write_doc(docsDir, id, content):
    docPath = os.path.join(docsDir, id + ".html")
    file = open(docPath, 'w')

    file.write(content)
    file.close()
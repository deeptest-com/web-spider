import os
from dotenv import load_dotenv, find_dotenv

def get_wiki_url():
    _ = load_dotenv(find_dotenv())

    return os.environ["WIKI_URL"]

def write_doc(docsDir, id, title, content):
    name = id + "-" + title.replace(os.sep, "_")
    print(name)

    docPath = os.path.join(docsDir, name + ".html")
    file = open(docPath, 'w')

    file.write(content)
    file.close()
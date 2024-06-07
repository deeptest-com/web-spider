import os
import time
import re

from langchain_community.document_loaders import AsyncHtmlLoader, JSONLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import urllib.request, json

from tool import get_wiki_url, write_doc

wiki_url = get_wiki_url()
url = "{}/rest/api/content?type=page&start=0&limit=99999".format(wiki_url)

batch_size = 5

docsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs")
if not os.path.exists(docsDir):
    os.makedirs(docsDir)

with urllib.request.urlopen(url) as url:
    data = json.load(url)
    results = data['results']

count = 0
index = 0
batch_urls_arr = []
batch_urls = []
for result in results:
    id = result["id"]

    if count > 9:
        batch_urls_arr.append(batch_urls)

        batch_urls = []
        count = 0

    else:
        pageUrl = "{}/pages/viewpage.action?pageId={id}".format(wiki_url, id=id)
        batch_urls.append(pageUrl)
        count += 1


for batch_urls in batch_urls_arr:
    loader = AsyncHtmlLoader(batch_urls)
    docs = loader.load()

    bs_transformer = BeautifulSoupTransformer()
    docs_transformer = (
        bs_transformer.transform_documents(
            docs,
            tags_to_extract=["p", "li", "div", "a", "span", "h1", "h2", "h3", "h4", "h5", "h6"],
            remove_comments=True))

    for doc_transformer in docs_transformer:
        source = doc_transformer.metadata["source"]
        ids = re.findall(r"pageId=(\d+?)$", source)

        id = 0
        if ids.__len__() > 0:
            id = ids[0]

        title = doc_transformer.metadata["title"]
        content = doc_transformer.page_content

        write_doc(docsDir, id, title, content)

    time.sleep(1)
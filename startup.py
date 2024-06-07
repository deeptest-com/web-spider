from tool import get_wiki_url

wiki_url = get_wiki_url()

url = "{}/rest/api/content?type=page&start=0&limit=99999".format(wiki_url)

from langchain_community.document_loaders import AsyncHtmlLoader, JSONLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

import urllib.request, json

with urllib.request.urlopen(url) as url:
    data = json.load(url)
    results = data['results']

for result in results:
    pageUrl = "{}/pages/viewpage.action?pageId={id}".format(wiki_url, id=result["id"])
    print(pageUrl)

    loader = AsyncHtmlLoader([pageUrl])
    docs = loader.load()

    # print(docs[0].page_content)

    bs_transformer = BeautifulSoupTransformer()
    docs_transformer = (
        bs_transformer.transform_documents(docs,
                                           tags_to_extract=["p", "li", "div", "a", "span", "h1", "h2", "h3", "h4", "h5", "h6"],
                                           remove_comments=True))

    content = docs_transformer[0].page_content

    print("==================\n")
    print(content)

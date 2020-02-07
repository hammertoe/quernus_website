import argparse
import requests
import json
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Fetch content from a coil post")
parser.add_argument("url", help="URL to fetch from Coil")
args = parser.parse_args()

url_parts = urlparse(args.url)
path = url_parts[2]
path_parts = path.split('/')

assert(path_parts[1] == 'p')
username = path_parts[2]
post_id = path_parts[-1]

gq_api_url = "https://coil.com/graphql"

query = """query GetPost($author: String, $postId: String, $postPermanentId: String) {""" \
        """    getPost(author: $author, postId: $postId, permanentId: $postPermanentId) { content publishedAt title}""" \
        """}"""

data =  {"operationName":"GetPost",
         "variables":{"author":username,
                      "postPermanentId":post_id},
         "query": query}
data = json.dumps(data)
headers = {"content-type": "application/json"}

req = requests.post(gq_api_url,
                    headers=headers,
                    data=data)

res = req.json()
content = res['data']['getPost']['content']
date = res['data']['getPost']['publishedAt']
title = res['data']['getPost']['title']

# format title to slug
slug = title.lower()
slug = re.sub(r"\W+", "-", slug)
date = date.split("T")[0]
slug = f"{date}-{slug}"

# Find all image links, download the images and rewrite the local image links:
soup = BeautifulSoup(content, features="html.parser")

for img in soup.findAll('img'):
    src = img['src']
    r = requests.get(src, allow_redirects=True)
    path = urlparse(src).path
    filename = path.split("/")[-1]
    filename = f"/coil_images/{filename}"
    img['src'] = filename
    with open(f"content{filename}", "wb") as f:
        f.write(r.content)

html = soup.prettify()
#print(content)
#print(slug)

filename = f"content/{slug}.md"

header = f"""---
layout: post
title: {title}
comments: True
tags: 
summary: 
---

<p class="message">
This post was originally written on my Coil site, which is currently my main blogging platform. 
On there you will also see bonus content if you are a Coil subscriber.<br />
<a href="{args.url}">{args.url}</a>
</p>


"""

with open(filename, "x") as f:
    f.write(header)
    f.write(html)

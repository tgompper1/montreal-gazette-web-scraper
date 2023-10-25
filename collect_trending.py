# Tess Gompper #260947251
import requests
from pathlib import Path
import bs4
import argparse
import json

PYTHONENCODING = "utf-8"

headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

def get_trending_stories_html():
    
    fpath = Path("homepage.html")

    if not fpath.exists():
        data = requests.get("https://montrealgazette.com/category/news/", headers=headers)
        with open(fpath, "w") as f:
            f.write(data.text)
    with open(fpath) as f:
        homepage_html_data= f.read()
        
    data = []

    soup = bs4.BeautifulSoup(homepage_html_data, "html.parser")
    trending_div = soup.find("div", class_="list-widget-trending") #gets first
    trending_ol = trending_div.find("ol")
    i=0
    for li in trending_ol.find_all("li"):
        a_href=li.find("a").get("href")
        data.append(get_article_info(a_href))
    return data



def get_article_info(article_path):
    title = article_path.rsplit('/', 1)[-1]

    fpath = Path(f"{title}.html")
    if not fpath.exists():
        data = requests.get(f"https://montrealgazette.com{article_path}", headers=headers)
        with open(fpath, "w",  encoding=PYTHONENCODING) as f:
            f.write(data.text)
    with open(fpath, encoding=PYTHONENCODING) as f:
        article_html_data = f.read()
    article_json = {}
    soup = bs4.BeautifulSoup(article_html_data, "html.parser")
    
    title = soup.find("h1", id="articleTitle").text.strip()

    date = soup.find("span", class_="published-date__since").text.strip()
 
    author = soup.find("span", class_="published-by__author").find("a").text.strip()
    
    blurb  = soup.find("p", class_="article-subtitle").text.strip()

    article_json["title"]=title
    article_json["publication_date"] = date
    article_json["author"] = author
    article_json["blurb"] = blurb

    return article_json


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-o", dest="json_file", help="output json file", metavar="<json_file>", required=True)
    args = parser.parse_args()
    fpath=args.json_file
    with open(fpath, "w") as f:
        json.dump(get_trending_stories_html(), f, indent = 4) 

if __name__ == "__main__":
    main()
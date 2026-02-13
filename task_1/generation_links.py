import requests
from bs4 import BeautifulSoup
import os

def get_links_from_page( *urls ):
    links = set()
    for url in urls:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith("/ru/articles/") and "/page" not in href: 
                    if href.endswith("comments/"):
                        href = href.removesuffix("comments/")
                    links.add("https://habr.com" + href)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении ссылок с {url}: {e}")
            return []
    return list(links)

urls_to_scan = [
    "https://habr.com/ru/articles/",
    "https://habr.com/ru/articles/page2/",
    "https://habr.com/ru/articles/page3/",
    "https://habr.com/ru/articles/page4/",
    "https://habr.com/ru/articles/page5/",
    "https://habr.com/ru/articles/page6/",
    "https://habr.com/ru/articles/page7/",
    "https://habr.com/ru/articles/page8/",
    "https://habr.com/ru/articles/page9/",
    "https://habr.com/ru/articles/page10/"
]
links = get_links_from_page(*urls_to_scan)

for i in range(len(links)):
    print(f"\'{links[i]}\',")
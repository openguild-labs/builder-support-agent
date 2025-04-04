import os 
import json 

#Web Scraping
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )

#--------------------------------------------Scraping Polkadot blog from URL-------------------------------------------------
LINKS_FILE = os.path.join(BASE_DIR, "urls", "blog_links.json")

def load_links():
    try:
        with open(LINKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict) or "urls" not in data:
                print("⚠️ Error: Invalid links.json format")
                return []
            return data["urls"]
    except json.JSONDecodeError:
        print("⚠️ Error: Invalid JSON format in links.json")
        return []
    except FileNotFoundError:
        print("⚠️ Error: links.json not found")
        return []

def get_new_posts():
    try:
        urls = load_links()
        if not urls:
            print("⚠️ No URLs found in links.json")
            return []

        latest_posts = []
        seen_titles = set()

        for url in urls:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.find_all("div", class_="col-span-full")

            for post in posts:
                title_tag = post.find("h2")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find("a")["href"] if title_tag.find("a") else None
                    if link:
                        link = f"https://polkadot.network{link}"

                    if title not in seen_titles:
                        seen_titles.add(title)
                        latest_posts.append({"title": title, "link": link})

        return latest_posts[:3]

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching the blog page: {e}")
        return []
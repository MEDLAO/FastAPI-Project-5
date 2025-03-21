from fastapi import FastAPI
import os
import requests
from bs4 import BeautifulSoup
from typing import List


app = FastAPI()


RAPIDAPI_SECRET = os.getenv("RAPIDAPI_SECRET")


@app.get("/")
def read_root():
    welcome_message = (
        "Welcome!"
        "¡Bienvenido!"
        "欢迎!"
        "नमस्ते!"
        "مرحبًا!"
        "Olá!"
        "Здравствуйте!"
        "Bonjour!"
        "বাংলা!"
        "こんにちは!"
    )
    return {"message": welcome_message}


def scrape_ebay_search(query: str) -> List[dict]:
    query = query.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select(".s-item")
    items = []

    for item in results:
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        url_tag = item.select_one(".s-item__link")
        image = item.select_one(".s-item__image-img")
        condition = item.select_one(".SECONDARY_INFO")
        shipping = item.select_one(".s-item__shipping, .s-item__freeXDays")

        if not (title and price and url_tag):
            continue

        items.append({
            "title": title.get_text(strip=True),
            "price": price.get_text(strip=True),
            "condition": condition.get_text(strip=True) if condition else None,
            "shipping": shipping.get_text(strip=True) if shipping else None,
            "url": url_tag['href'],
            "image": image['src'] if image else None
        })

    return items



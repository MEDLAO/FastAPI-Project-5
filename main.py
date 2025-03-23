import requests
from bs4 import BeautifulSoup


def test_ebay_scraper(query="iphone 13"):
    query = query.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".s-item")

    if not items:
        print("No items found. The layout may have changed.")
        return

    print(f"Found {len(items)} items. Showing first 5:\n")

    for item in items[:5]:
        title_elem = item.select_one(".s-item__title")
        price_elem = item.select_one(".s-item__price")
        url_elem = item.select_one(".s-item__link")

        if title_elem and price_elem and url_elem:
            print("Title:", title_elem.text.strip())
            print("Price:", price_elem.text.strip())
            print("URL:", url_elem['href'])
            print("-" * 40)


def scrape_ebay_categories() -> List[Dict]:
    url = "https://www.ebay.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch eBay homepage: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # eBay homepage categories are under <li class="hl-cat-nav__js-tab">
    category_elements = soup.select("li.hl-cat-nav__js-tab > a")

    categories = []
    for cat in category_elements:
        name = cat.get_text(strip=True)
        link = cat["href"] if cat.has_attr("href") else None
        if name and link:
            categories.append({
                "name": name,
                "url": link
            })

    return categories


if __name__ == "__main__":
    test_ebay_scraper()

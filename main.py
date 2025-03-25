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


def scrape_ebay_deals() -> List[Dict]:
    url = "https://www.ebay.com/deals"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch eBay deals page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    deal_elements = soup.select(".ebayui-dne-item-featured-card")  # main container for each deal

    deals = []
    for deal in deal_elements:
        title_elem = deal.select_one(".dne-itemtile-title")
        price_elem = deal.select_one(".dne-itemtile-price .first")
        original_price_elem = deal.select_one(".itemtile-price-strikethrough")
        url_elem = deal.select_one("a.dne-itemtile-detail")
        image_elem = deal.select_one("img")

        title = title_elem.get_text(strip=True) if title_elem else None
        price = price_elem.get_text(strip=True) if price_elem else None
        original_price = original_price_elem.get_text(strip=True) if original_price_elem else None
        url = url_elem["href"] if url_elem and url_elem.has_attr("href") else None
        image = image_elem["src"] if image_elem and image_elem.has_attr("src") else None

        if title and price and url:
            deals.append({
                "title": title,
                "price": price,
                "original_price": original_price,
                "url": url,
                "image": image
            })

    return deals


def scrape_ebay_product(item_url: str) -> Dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(item_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch product page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    title_elem = soup.select_one("#itemTitle")
    price_elem = soup.select_one("#prcIsum, #prcIsum_bidPrice, #mm-saleDscPrc")
    specs_table = soup.select("div.itemAttr td.attrLabels, div.itemAttr td")

    title = title_elem.get_text(strip=True).replace("Details about  ", "") if title_elem else None
    price = price_elem.get_text(strip=True) if price_elem else None

    # Extract key-value specs
    specs = {}
    for i in range(0, len(specs_table) - 1, 2):
        label = specs_table[i].get_text(strip=True)
        value = specs_table[i + 1].get_text(strip=True)
        specs[label] = value

    return {
        "title": title,
        "price": price,
        "specs": specs,
        "url": item_url
    }



if __name__ == "__main__":
    test_ebay_scraper()

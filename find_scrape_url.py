import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlunparse
import logging
import json
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GoogleAdvancedSearch:
    def __init__(self):
        self.params = {
            "as_q": "",  # All these words
            "as_epq": "",  # This exact word or phrase
            "as_oq": "",  # Any of these words
            "as_eq": "",  # None of these words
            "as_nlo": "",  # Numbers ranging from (low)
            "as_nhi": "",  # Numbers ranging to (high)
            "lr": "",  # Language
            "cr": "",  # Region
            "as_qdr": "all",  # Last update (d - day, w - week, m - month, y - year, all - anytime)
            "as_sitesearch": "",  # Site or domain
            "as_occt": "any",  # Terms appearing (any, title, url, links)
            "as_filetype": "",  # File type
            "tbs": "",  # Tools and filters
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }

    def set_all_words(self, words):
        self.params["as_q"] = words

    def set_exact_phrase(self, phrase):
        self.params["as_epq"] = phrase

    def set_any_words(self, words):
        self.params["as_oq"] = words

    def set_none_words(self, words):
        self.params["as_eq"] = words

    def set_number_range(self, low, high):
        self.params["as_nlo"] = low
        self.params["as_nhi"] = high

    def set_language(self, language_code):
        self.params["lr"] = f"lang_{language_code}"

    def set_region(self, country_code):
        self.params["cr"] = f"country{country_code}"

    def set_last_update(self, period):
        self.params["as_qdr"] = period

    def set_site_or_domain(self, site):
        self.params["as_sitesearch"] = site

    def set_terms_appearing(self, location):
        self.params["as_occt"] = location

    def set_file_type(self, file_type):
        self.params["as_filetype"] = file_type

    def set_usage_rights(self, rights):
        self.params["tbs"] = rights

    def get_search_url(self):
        query_string = urlencode(self.params)
        return urlunparse(("https", "www.google.com", "/search", "", query_string, ""))

    def fetch_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching the URL: {e}")
            return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("div", {"class": "g"})

    def extract_data(self, all_data):
        data = []
        position = 0
        for item in all_data:
            link = item.find("a").get("href")
            if link and link.startswith("https") and "aclk" not in link:
                position += 1
                entry = {
                    "link": link,
                    "title": item.find("h3").text if item.find("h3") else None,
                    "description": (
                        item.find("div", {"class": "VwiC3b"}).text
                        if item.find("div", {"class": "VwiC3b"})
                        else None
                    ),
                    "position": position,
                }
                data.append(entry)
        return data

    def save_data(self, data, filename="data.json"):
        if not os.path.exists("data"):
            os.makedirs("data")

        filepath = os.path.join("data", filename)

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info(f"Data saved to {filepath}")

    def save_links(self, data, filename="links.json"):
        if not os.path.exists("data"):
            os.makedirs("data")

        filepath = os.path.join("data", filename)

        links = [item["link"] for item in data]

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(links, file, indent=4)

        logging.info(f"Links saved to {filepath}")

    def scrape(self, save_data=False, save_links=True):
        search_url = self.get_search_url()
        logging.info(f"Using URL: {search_url}")
        html = self.fetch_html(search_url)
        if html:
            all_data = self.parse_html(html)
            data = self.extract_data(all_data)

            if save_data:
                self.save_data(data)
            if save_links:
                self.save_links(data)

            logging.info("Scraping completed successfully")

        return data


if __name__ == "__main__":
    search = GoogleAdvancedSearch()

    # Customize the search parameters
    search.set_all_words("")
    search.set_exact_phrase("albert stankowski")
    search.set_any_words("")
    search.set_none_words("")
    search.set_number_range("", "")
    search.set_language("en")
    search.set_region("")
    # d - day, w - week, m - month, y - year, all - anytime
    search.set_last_update("w")
    search.set_site_or_domain("")
    search.set_terms_appearing("")
    search.set_file_type("")
    search.set_usage_rights("")

    # Perform the scraping
    data = search.scrape(save_data=False, save_links=True)

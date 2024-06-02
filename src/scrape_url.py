import json
import requests
from bs4 import BeautifulSoup
import re
import os
import time


def sanitize_filename(url):
    """Sanitize the URL to create a valid filename."""
    return re.sub(r'[\\/*?:"<>|]', "_", url)


def preprocess_content(content):
    """Preprocess the content by replacing consecutive spaces with newline characters."""
    content = content.replace("\n", "")
    return re.sub(r"\s{2,}", "\n", content)


def scrape_and_save(url):
    """Scrape content from the given URL and save it to a JSON file."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.get_text()

        preprocessed_content = preprocess_content(content)

        data = {"url": url, "content": preprocessed_content}

        os.makedirs("data/scrape", exist_ok=True)

        filename = os.path.join("data/scrape", sanitize_filename(url) + ".json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Content saved to {filename}")
    else:
        print(f"Failed to retrieve {url}")


def scrape_url(wait_time=5):
    # Load URLs from the JSON file
    with open("./data/links.json", "r") as file:
        urls = json.load(file)

    # Ensure the loaded data is a list
    if not isinstance(urls, list):
        raise ValueError("JSON file must contain a list of URLs")

    # Scrape each URL and save the content
    for url in urls:
        scrape_and_save(url)
        time.sleep(wait_time)


# if __name__ == "__main__":
#     scrape_url()

import json
import requests
from bs4 import BeautifulSoup
import re
import os

def sanitize_filename(url):
    """Sanitize the URL to create a valid filename."""
    return re.sub(r'[\\/*?:"<>|]', "_", url)

def scrape_and_save(url):
    """Scrape content from the given URL and save it to a JSON file."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text()
        data = {
            "url": url,
            "content": content
        }
        filename = sanitize_filename(url) + '.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Content saved to {filename}")
    else:
        print(f"Failed to retrieve {url}")

def main():
    # Load URLs from the JSON file
    with open('links.json', 'r') as file:
        urls = json.load(file)

    # Ensure the loaded data is a list
    if not isinstance(urls, list):
        raise ValueError("JSON file must contain a list of URLs")

    # Scrape each URL and save the content
    for url in urls:
        scrape_and_save(url)

if __name__ == '__main__':
    main()
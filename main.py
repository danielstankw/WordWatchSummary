from src.find_scrape_url import GoogleAdvancedSearch
from src.scrape_url import scrape_url
from llm.ollama_main import summarize_articles
from src.smtp import send_mail
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def configure_search(search):
    """Customize the GoogleAdvancedSearch parameters."""
    search.set_all_words("")
    search.set_exact_phrase("Museum of War")
    search.set_any_words("")
    search.set_none_words("")
    search.set_number_range("", "")
    search.set_language("en")
    search.set_region("")
    # d - day, w - week, m - month, y - year, all - anytime
    search.set_last_update("d")
    search.set_site_or_domain("")
    search.set_terms_appearing("")
    search.set_file_type("")
    search.set_usage_rights("")

def main():
    """Main function to perform search and scrape URLs."""
    # Initialize the GoogleAdvancedSearch class
    search = GoogleAdvancedSearch()
    
    # Configure search parameters
    configure_search(search)

    # Perform the search and scrape URLs
    try:
        search.find_url()
        scrape_url(wait_time=5)
    except Exception as e:
        # Log the error
        logging.error(f"An error occurred: {e}")

    summarize_articles()

    send_mail()

if __name__ == "__main__":
    main()

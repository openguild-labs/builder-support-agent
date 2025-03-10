import requests
import json
import os
import time
import logging
from bs4 import BeautifulSoup

# 🛠 Logging Setup
LOG_FILE = "crawler.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🚀 Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAQ_LINKS_FILE = os.path.join(BASE_DIR, "src", "urls", "faq_links.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "src", "urls", "polkadot_faq.json")
MAX_RETRIES = 3  # Retry attempts for failed requests
TIMEOUT = 10  # Timeout for HTTP requests

# 📂 Load FAQ URLs
def load_faq_urls():
    """Loads FAQ URLs from `faq_links.json`."""
    if not os.path.exists(FAQ_LINKS_FILE):
        logging.error(f"❌ FAQ links file not found: {FAQ_LINKS_FILE}")
        return []
    
    try:
        with open(FAQ_LINKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("urls", [])
    except json.JSONDecodeError:
        logging.error(f"❌ Error parsing JSON: {FAQ_LINKS_FILE}")
        return []

# 🛠 Crawl FAQ Data
def crawl_polkadot_faq(url):
    logging.info(f"🔍 Crawling FAQ from: {url}")

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code != 200:
                logging.warning(f"⚠️ Attempt {attempt+1}: Failed to fetch {url} (Status: {response.status_code})")
                time.sleep(2)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            faq_data = []
            questions = soup.find_all(["h2", "h3"])

            for question in questions:
                answer = []
                next_elem = question.find_next_sibling()

                while next_elem and next_elem.name not in ["h2", "h3"]:
                    if next_elem.name in ["p", "div", "ul", "ol"]:
                        text = next_elem.get_text(strip=True).replace("\n", " ")
                        answer.append(text)
                    next_elem = next_elem.find_next_sibling()

                if answer:
                    faq_data.append({
                        "question": question.get_text(strip=True).replace("\n", " "),
                        "answer": " ".join(answer)
                    })

            logging.info(f"✅ Successfully crawled {len(faq_data)} FAQs from {url}")
            return faq_data
        
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Error during crawling {url}: {e}")
            time.sleep(3)  # Wait before retrying

    logging.error(f"❌ Failed to fetch {url} after {MAX_RETRIES} attempts")
    return []

# 📂 Save FAQ Data
def save_faq_data(faq_data):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(faq_data, f, indent=4, ensure_ascii=False)

    logging.info(f"📂 Saved {len(faq_data)} FAQs to {OUTPUT_FILE}")

# 🚀 Main Function
def main():
    logging.info("🚀 Starting FAQ crawling process...")

    faq_urls = load_faq_urls()
    if not faq_urls:
        logging.error("❌ No FAQ URLs found, exiting.")
        return

    all_faqs = []
    for url in faq_urls:
        all_faqs.extend(crawl_polkadot_faq(url))

    if all_faqs:
        save_faq_data(all_faqs)
        logging.info("✅ FAQ crawling completed successfully!")
    else:
        logging.warning("⚠️ No FAQ data was collected!")

if __name__ == "__main__":
    main()

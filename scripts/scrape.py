# scripts/scrape.py
import os
import requests
from bs4 import BeautifulSoup
import time

# --- Configuration ---
URLS_TO_SCRAPE = [
    "https://nmcg.nic.in/NamamiGange.aspx",
    "https://nmcg.nic.in/activities.aspx",
    "https://nmcg.nic.in/abou-us.aspx",
    "https://jalshakti-dowr.gov.in/schemes-projects/namami-gange-programme/",
    "https://nmcg.nic.in/about_nmcg.aspx",
    "https://nmcg.nic.in/newsletter.aspx",
    "https://www.jalshakti-dowr.gov.in/offerings/schemes-and-services/details/namami-gange",
    "https://www.pib.gov.in/",
    "https://www.pmindia.gov.in/en/government_tr_rec/namami-gange/",
    "https://ddnews.gov.in/en/namami-gange-programme-over-300-projects-completed-rs-40000-crore-invested-in-rejuvenating-river-ganga/",
    "https://thewaterdigest.com/tag/namami-gange/",
    "https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2125277",
    "https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2121047",
    "https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2109118",
    "https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2095341",
    "https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2093936",
    "https://www.pib.gov.in/FeaturesDeatils.aspx?NoteId=153670&ModuleId=2",
    "https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2065766",
    "https://en.wikipedia.org/wiki/Namami_Gange_Programme",
    "https://www.aninews.in/news/world/asia/ganga-connect-concludes-in-london-after-high-level-of-engagement-tangible-outcomes20211129192955/",
    # Add more relevant news articles or official pages here
]
OUTPUT_DIR = "./data/raw_text"

# --- Helper Function ---
def scrape_and_save(url: str, output_dir: str):
    """Scrapes a URL, extracts main text content, and saves it to a file."""
    try:
        print(f"Scraping {url}...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # This is a generic selector. You might need to inspect each site
        # to find the main content container (e.g., <main>, <article>, <div class="content">)
        # For nmcg.nic.in, 'form-group' contains a lot of the main text.
        content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
        
        if not content_tags:
            # Fallback to just getting all text if specific tags fail
            text = soup.get_text(separator='\n', strip=True)
        else:
            text = '\n'.join(tag.get_text(strip=True) for tag in content_tags)

        if not text.strip():
            print(f"Warning: No text content found for {url}")
            return

        # Create a simple filename from the URL
        filename = url.split("://")[1].replace("/", "_").replace(".", "_") + ".txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Successfully saved content to {filepath}")

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for url in URLS_TO_SCRAPE:
        scrape_and_save(url, OUTPUT_DIR)
        time.sleep(1) # Be respectful to the server, wait a second between requests
import os
import time
import csv
from DrissionPage import ChromiumPage
from DrissionPage.errors import NoRectError

# Constants
OPAY_BLOG_URL = "https://blog.opayweb.com/"
SITE_NAME = "opay"
TYPE = "blog"
OUTPUT_FILE = "datasets/opay_blog_posts.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Initialize ChromiumPage
page = ChromiumPage()

# Define number of pages to scrape
PAGES = 9

# CSV header
fields = ["site", "text", "type"]

# Open CSV file for writing
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    # Navigate to the Opay blog
    page.get(OPAY_BLOG_URL)
    page.wait(20)
    page.wait.doc_loaded()

    links = []

    # Extract links from all pages
    for n in range(2, PAGES + 1):
        try:
            blog_posts = page.eles("@class=css-ondjfz")
            blog_posts_links = [blog.link for blog in blog_posts]
            links.extend(blog_posts_links)

            next_button = page.ele(f'@text()={n}')
            if next_button:
                next_button.click()
                time.sleep(5)
            else:
                print(f"Next button for page {n} not found.")
                break

        except Exception as e:
            print(f"Error navigating to page {n}: {e}")

    # Scrape each blog post
    for link in links:
        try:
            page.get(link)
            page.wait.doc_loaded()

            article = page.eles("@class=css-1e3i1a4")
            if article and len(article) > 1:
                text = article[1].text.replace('"', "'").replace('“', "'").replace('”', "'")

                # Write to CSV
                writer.writerow({"site": SITE_NAME, "text": text, "type": TYPE})
            else:
                print(f"Article content not found for link: {link}")

        except Exception as e:
            print(f"Error while scraping {link}: {e}")

print(f"Scraping completed. Data saved to {OUTPUT_FILE}.")

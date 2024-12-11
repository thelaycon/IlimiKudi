import os
import time
import csv
from DrissionPage import ChromiumPage

# Constants
PAYSTACK_BLOG_URL = "https://paystack.com/blog/page/{n}?q=/"
SITE_NAME = "paystack"
TYPE = "blog"
OUTPUT_FILE = "datasets/paystack_blog_posts.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Initialize ChromiumPage
page = ChromiumPage()

# Define number of pages to scrape
PAGES = 25

# CSV header
fields = ["site", "text", "type"]

# Open CSV file for writing
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    # Loop through the pages
    for n in range(1, PAGES + 1):
        print(f"Scraping page {n}...")
        page.get(PAYSTACK_BLOG_URL.format(n=n))
        page.wait.doc_loaded()

        # Allow page to load
        time.sleep(10)

        # Extract post links
        posts = page.eles("@class=post__title")
        links = [post.link for post in posts]

        for link in links:
            try:
                print(f"Scraping article: {link}")
                page.get(link)
                page.wait.doc_loaded()
                
                # Allow article to load
                time.sleep(5)

                # Extract article content
                article = page.ele('xpath:/html/body/article')
                if article:
                    text = article.text.replace('"', "'")
                    
                    # Write to CSV
                    writer.writerow({"site": SITE_NAME, "text": text, "type": TYPE})
                else:
                    print("No article content found.")

                time.sleep(5)

            except Exception as e:
                print(f"Error while scraping {link}: {e}")

print(f"Scraping completed. Data saved to {OUTPUT_FILE}.")
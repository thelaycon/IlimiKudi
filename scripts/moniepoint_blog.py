import os
import time
import csv
from DrissionPage import ChromiumPage
from DrissionPage.errors import ElementNotFoundError

# Constants
MONIEPOINT_BLOG_URL = "https://moniepoint.com/blog"
SITE_NAME = "moniepoint"
TYPE = "blog"
OUTPUT_FILE = "datasets/moniepoint_blog_posts.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Initialize ChromiumPage
page = ChromiumPage()

# CSV header
fields = ["site", "text", "type"]

# Open CSV file for writing
with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    # Navigate to Moniepoint blog
    page.get(MONIEPOINT_BLOG_URL)
    time.sleep(10)

    # Load all blog posts
    while True:
        try:
            page.ele("@text()=Load more").click()
            time.sleep(5)
        except ElementNotFoundError:
            print("All posts loaded.")
            break

    # Extract links to individual blog posts
    blog_eles = page.eles("@class=blog_blog-item__H40aR")
    links = [link.link for link in blog_eles]

    # Scrape each blog post
    for link in links:
        try:
            page.get(link)
            time.sleep(5)

            # Extract article content
            article = page.ele("@class=article_article-container__eqcVl")
            if article:
                text = article.text.replace('"', "'").replace('“', "'").replace('”', "'")

                # Write to CSV
                writer.writerow({"site": SITE_NAME, "text": text, "type": TYPE})
                print(f"Scraped: {link}")
            else:
                print(f"No content found for link: {link}")

        except Exception as e:
            print(f"Error scraping {link}: {e}")

print(f"Scraping completed. Data saved to {OUTPUT_FILE}.")

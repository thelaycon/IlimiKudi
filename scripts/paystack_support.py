import time
import csv
import os
from DrissionPage import ChromiumPage

# Constants
PAYSTACK_SUPPORT_URL = "https://support.paystack.com/"
SITE_NAME = "paystack"
TYPE = "support"
OUTPUT_FILE = "datasets/paystack_support_posts.csv"

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

    # Navigate to main support page
    page.get(PAYSTACK_SUPPORT_URL)
    page.wait.doc_loaded()

    time.sleep(10)

    # Extract category links
    categories = page.eles("@@class=kb-category-card")
    categories_links = [category.link for category in categories]

    for categories_link in categories_links:
        page.get(categories_link)
        page.wait.doc_loaded()

        time.sleep(5)

        # Extract sub-category links
        sub_categories = page.eles("@class=kb-category-card")
        sub_categories_links = [sub_category.link for sub_category in sub_categories]

        for sub_categories_link in sub_categories_links:
            page.get(sub_categories_link)
            page.wait.doc_loaded()

            time.sleep(5)

            # Extract article links
            articles = page.eles("@class=article-card")
            articles_links = [article.link for article in articles]

            for article_link in articles_links:
                try:
                    page.get(article_link)
                    page.wait.doc_loaded()
                    
                    time.sleep(5)

                    # Extract article content
                    article = page.ele("xpath:/html/body/div[1]/div[3]/div[2]/div[2]")
                    if article:
                        text = article.text.replace('"', "'").replace('“', "'").replace('”', "'")

                        # Write to CSV
                        writer.writerow({"site": SITE_NAME, "text": text, "type": TYPE})
                    else:
                        print("No article content found.")

                except Exception as e:
                    print(f"Error while scraping {article_link}: {e}")

print(f"Scraping completed. Data saved to {OUTPUT_FILE}.")

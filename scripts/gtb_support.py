import time
import csv
import os
from DrissionPage import ChromiumPage

# Constants
GTB_SUPPORT_URL = "https://www.gtbank.com/help-centre"
SITE_NAME = "gtb"
TYPE = "support"
OUTPUT_FILE = "datasets/gtb_support_posts.csv"

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

    # Navigate to the GTB support URL
    page.get(GTB_SUPPORT_URL)
    time.sleep(10)

    # Extract support information
    try:
        support_info_element = page.ele('xpath://*[@id="nav-account-services"]/div[2]')
        if support_info_element:
            support_info_text = support_info_element.text.replace('"', "'").replace('“', "'").replace('”', "'").replace('“', "'").replace('”', "'").replace('“', "'").replace('”', "'").replace('“', "'").replace('”', "'")

            # Write to CSV
            writer.writerow({"site": SITE_NAME, "text": support_info_text, "type": TYPE})
            print(f"Support information scraped and saved to {OUTPUT_FILE}.")
        else:
            print("Support information not found.")
    except Exception as e:
        print(f"Error while scraping support information: {e}")

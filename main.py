# main.py

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.extracts.category_scraper import get_categories
from utils.extracts.product_scraper import get_products_from_category

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("scraper_log.txt", mode='w'),
            logging.StreamHandler()
        ]
    )

def run_scraper():
    setup_logger()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    logging.info("Memulai scraping kategori...")

    try:
        categories = get_categories(limit=3)  # 3 kategori untuk percobaan

        for cat in categories:
            logging.info(f"\n📂 Memproses kategori: {cat['name']} ({cat['url']})")
            products = get_products_from_category(driver, cat['url'], max_products=10)

            logging.info(f"📦 Jumlah produk ditemukan: {len(products)}")
            for i, prod in enumerate(products, 1):
                logging.info(f"[{i}] {prod['brand']} - {prod['name']} | ⭐ {prod['rating']} ({prod['total_reviews']} reviews)")
    finally:
        driver.quit()
        logging.info("Scraping selesai dan browser ditutup.")

if __name__ == "__main__":
    run_scraper()
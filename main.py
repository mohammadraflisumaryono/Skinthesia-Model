# main.py

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.extracts.category_scraper import get_categories
from utils.extracts.product_scraper import get_products_from_category
import pandas as pd
import os

def setup_logger():
    # buat folder logs jika belum ada
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # setup logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/scraper_log.txt", mode='w'),
            logging.StreamHandler()
        ]
    )

def run_scraper():
    setup_logger()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    logging.info("Memulai scraping kategori...")
    all_products = []

    try:
        categories = get_categories(limit=3)  # 3 kategori untuk percobaan

        for cat in categories:
            logging.info(f"\n Memproses kategori: {cat['name']} ({cat['url']})")
            products = get_products_from_category(driver, cat['url'], max_products=100)

            logging.info(f" Jumlah produk ditemukan: {len(products)}")
            for i, prod in enumerate(products, 1):
                logging.info(f"[{i}] {prod['brand']} - {prod['name']} |  {prod['rating']} ({prod['total_reviews']} reviews)")
            all_products.extend(products)
    finally:
        driver.quit()
        logging.info("Scraping selesai dan browser ditutup.")
         # Simpan ke CSV
    if all_products:
        df = pd.DataFrame(all_products)
        if not os.path.exists("data"):
            os.makedirs("data")
        df.to_csv("data/raw.csv", index=False, encoding='utf-8-sig')
        logging.info(f"Data berhasil disimpan ke data/raw.csv ({len(df)} baris)")
    else:
        logging.warning("Tidak ada data produk yang berhasil dikumpulkan.")

if __name__ == "__main__":
    run_scraper()
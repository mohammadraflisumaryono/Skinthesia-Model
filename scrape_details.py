import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.extracts.detail_scraper import get_product_details
import os


def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/scrape_details_log.txt", mode='w'),
            logging.StreamHandler()
        ]
    )


def run_detail_scraper():
    setup_logger()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    all_details = []
    all_reviews = []

    try:
        product_list_path = "data/products_list.csv"
        if not os.path.exists(product_list_path):
            logging.error("❌ File data/products_list.csv tidak ditemukan. Jalankan scrape_products.py dulu.")
            return

        df = pd.read_csv(product_list_path)
        for i, row in df.iterrows():
            try:
                detail = get_product_details(driver, row["url"])
                if detail:
                    all_details.append({k: v for k, v in detail.items() if k != "reviews"})
                    for rev in detail["reviews"]:
                        rev["product_name"] = detail["name"]
                        rev["product_url"] = detail["url"]
                        all_reviews.append(rev)
                    logging.info(f"📌 Detail & review diambil: {detail['name']}")
            except Exception as e:
                logging.warning(f"❌ Gagal ambil detail: {row['name']} - {e}")

    finally:
        driver.quit()
        logging.info("Browser ditutup.")

    if all_details:
        pd.DataFrame(all_details).to_csv("data/products_detail.csv", index=False, encoding="utf-8-sig")
        logging.info(f"📝 Detail produk disimpan ke data/products_detail.csv ({len(all_details)} baris)")
    if all_reviews:
        pd.DataFrame(all_reviews).to_csv("data/reviews.csv", index=False, encoding="utf-8-sig")
        logging.info(f"📝 Review disimpan ke data/reviews.csv ({len(all_reviews)} baris)")


if __name__ == "__main__":
    run_detail_scraper()

# skincare_scraper/extract/detail_scraper.py

from selenium.webdriver.common.by import By
import time

def get_product_details(driver, product_url):
    """
    Scrap detail dari halaman produk individual.
    """
    driver.get(product_url)
    time.sleep(2)

    try:
        name = driver.find_element(By.CLASS_NAME, "product-profile__name").text.strip()
        brand = driver.find_element(By.CLASS_NAME, "product-profile__brand").text.strip()
        rating = driver.find_element(By.CLASS_NAME, "product-profile__rating-value").text.strip()
        reviews = driver.find_element(By.CLASS_NAME, "product-profile__rating-count").text.strip()
        desc = driver.find_element(By.CLASS_NAME, "product-detail__description").text.strip()
    except Exception:
        return None

    return {
        "name": name,
        "brand": brand,
        "rating": rating,
        "total_reviews": reviews,
        "description": desc,
        "url": product_url
    }

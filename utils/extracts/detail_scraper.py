# skincare_scraper/extract/category_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_categories(driver, limit=10):
    """
    Scrap daftar kategori skincare dan link-nya dari halaman kategori utama.
    """
    url = "https://femaledaily.com/category/skincare"
    driver.get(url)
    time.sleep(3)

    categories = []
    root = driver.find_element(By.CLASS_NAME, 'category-landing-list')
    columns = root.find_elements(By.CLASS_NAME, 'category-landing-column')

    for col in columns:
        links = col.find_elements(By.TAG_NAME, "a")
        for link in links:
            categories.append({
                "name": link.text.strip(),
                "url": link.get_attribute("href")
            })
            if len(categories) >= limit:
                return categories
    return categories

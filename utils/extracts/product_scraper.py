# utils/extracts/product_scraper.py

from selenium.webdriver.common.by import By
import time

def get_products_from_category(driver, category_url, max_products=100):
    """
    Scrap daftar produk dari suatu kategori di Female Daily.
    """
    driver.get(category_url)
    time.sleep(3)

    products = []
    scroll_pause = 2

    while len(products) < max_products:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        product_cards = driver.find_elements(By.CSS_SELECTOR, 'a.product-card')

        for card in product_cards:
            try:
                name_el = card.find_elements(By.CLASS_NAME, 'fd-body-md-regular')
                name = name_el[1].text.strip() if len(name_el) > 1 else ""
                brand = card.find_element(By.CLASS_NAME, 'fd-body-md-bold').text.strip()
                img = card.find_element(By.TAG_NAME, 'img').get_attribute("src")
                url = card.get_attribute("href")
                rating = card.find_element(By.CSS_SELECTOR, '.rating span.fd-body-sm-regular').text.strip()
                total_reviews = card.find_element(By.CSS_SELECTOR, '.rating span.grey').text.strip()
                total_reviews = total_reviews.strip("()")  # remove parentheses

                products.append({
                    "name": name,
                    "brand": brand,
                    "image": img,
                    "url": url,
                    "rating": rating,
                    "total_reviews": total_reviews
                })

            except Exception as e:
                print(f"[!] Error scraping product card: {e}")
                continue

            if len(products) >= max_products:
                break

    return products
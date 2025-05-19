# utils/extracts/review_scraper.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_reviews(driver, max_pages=5):
    reviews = []
    page = 1

    while page <= max_pages:
        time.sleep(2)

        try:
            # Klik tombol read-more jika ada untuk memperluas komentar
            read_more_buttons = driver.find_elements(By.CSS_SELECTOR, "span.read-more")
            for btn in read_more_buttons:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                except:
                    continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_blocks = soup.find_all('div', class_='review-detail d-flex')

            for block in review_blocks:
                try:
                    # Username (optional)
                    try:
                        username = block.find('p', class_='username').text.strip()
                    except:
                        username = None

                    # Skin info: oiltype, shade, tone, age
                    skin_info = block.find('p', class_='skin').text.strip().split(',')
                    skin_type = skin_info[0].strip() if len(skin_info) > 0 else None
                    age = skin_info[3].strip() if len(skin_info) > 3 else None

                    # Rating
                    stars = block.find_all('i', class_='icon-ic_big_star_full')
                    rating = len(stars)

                    # Recommended
                    rec_tag = block.find('p', class_='recommend')
                    if rec_tag:
                        rec_text = rec_tag.find('b').text.lower()
                        recommended = "doesn't" not in rec_text
                    else:
                        recommended = None

                    # Review text
                    try:
                        review_text = block.find('p', class_='text-content').text.strip()
                    except:
                        review_text = None

                    # Review date
                    try:
                        review_date = block.find('p', class_='date review-date').text.strip()
                    except:
                        review_date = None

                    # Usage period
                    try:
                        info_wrap = block.find('div', class_='information-wrapper')
                        usage_period = info_wrap.find_all('b')[0].text.strip()
                    except:
                        usage_period = None

                    reviews.append({
                        "username": username,
                        "skin_type": skin_type,
                        "age": age,
                        "rating_star": rating,
                        "recommended": recommended,
                        "review": review_text,
                        "review_date": review_date,
                        "usage_period": usage_period
                    })
                except Exception as e:
                    print(f"[!] Gagal ambil satu review: {e}")
                    continue

            # Klik tombol next
            try:
                next_button = driver.find_element(By.ID, "id_next_page")
                driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "review-detail"))
                )
                page += 1
            except:
                break

        except Exception as e:
            print(f"[!] Gagal ambil review halaman {page}: {e}")
            break

    return reviews

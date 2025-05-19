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
            # Tunggu sampai review muncul
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "review-card"))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_blocks = soup.select("div.review-card")

            print(f"[✓] Halaman {page} berhasil ambil {len(review_blocks)} review")

            if not review_blocks:
                print(f"[!] Halaman {page} tidak ada review.")
                break

            for block in review_blocks:
                try:
                    # Username
                    try:
                        username = block.select_one("p.profile-username").text.strip()
                    except:
                        username = None

                    # Age
                    try:
                        age = block.select_one("p.profile-age").text.strip()
                    except:
                        age = None

                    # Skin Type (ambil dari deskripsi, biasanya format: "Oily, Medium, Neutral")
                    try:
                        skin_desc = block.select_one("p.profile-description").text.strip()
                        skin_type = skin_desc.split(",")[0].strip() if skin_desc else None
                    except:
                        skin_type = None

                    # Rating
                    stars = block.select("span.cardrv-starlist i.icon-ic_big_star_full")
                    rating = len(stars)

                    # Recommended?
                    try:
                        recommend_text = block.select_one("p.recommend b").text.lower()
                        recommended = "doesn't" not in recommend_text
                    except:
                        recommended = None

                    # Review text
                    try:
                        review_text = block.select_one("p.text-content").text.strip()
                    except:
                        review_text = None

                    # Review date
                    try:
                        review_date = block.select_one("p.review-date").text.strip()
                    except:
                        review_date = None

                    # Usage period
                    try:
                        usage_period = block.select_one("div.information-wrapper b").text.strip()
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
                    print(f"[!] Gagal parsing satu review: {e}")
                    continue

            # Klik next halaman
            try:
                next_button = driver.find_element(By.ID, "id_next_page")
                driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "review-card"))
                )
                page += 1
            except:
                break
        except Exception as e:
            print(f"[!] Gagal proses halaman {page}: {e}")
            break

    return reviews

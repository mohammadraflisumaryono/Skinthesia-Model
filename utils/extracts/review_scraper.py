from selenium.webdriver.common.by import By
import time

def scrape_reviews(driver, max_pages=5):
    """
    Scrape review pengguna dari halaman produk Female Daily.
    Mengambil data: usia, tipe kulit, rating, direkomendasikan/tidak, periode penggunaan, tanggal review, isi review.
    """
    reviews = []
    page = 1

    while page <= max_pages:
        time.sleep(2)
        try:
            review_blocks = driver.find_elements(By.CLASS_NAME, "review-detail")

            for block in review_blocks:
                try:
                    # Ambil informasi pengguna (usia, skin type, dsb)
                    skin_info = block.find_element(By.CLASS_NAME, "skin").text.strip().split(",")
                    age = skin_info[3].strip() if len(skin_info) > 3 else None
                    skin_type = skin_info[0].strip() if len(skin_info) > 0 else None

                    # Rating (jumlah bintang full)
                    stars = block.find_elements(By.CLASS_NAME, "icon-ic_big_star_full")
                    rating = len(stars)

                    # Apakah direkomendasikan
                    try:
                        recommend_text = block.find_element(By.CLASS_NAME, "recommend").text.lower()
                        recommended = "recommend" in recommend_text and "doesn't" not in recommend_text
                    except:
                        recommended = None

                    # Isi review
                    try:
                        review_content = block.find_element(By.CLASS_NAME, "text-content").text.strip()
                    except:
                        review_content = None

                    # Tanggal
                    try:
                        review_date = block.find_element(By.CLASS_NAME, "review-date").text.strip()
                    except:
                        review_date = None

                    # Usage period
                    try:
                        usage_info = block.find_element(By.CLASS_NAME, "information-wrapper").find_elements(By.TAG_NAME, "b")
                        usage_period = usage_info[0].text.strip() if len(usage_info) > 0 else None
                    except:
                        usage_period = None

                    reviews.append({
                        "age": age,
                        "skin_type": skin_type,
                        "rating_star": rating,
                        "recommended": recommended,
                        "review": review_content,
                        "review_date": review_date,
                        "usage_period": usage_period
                    })
                except Exception as e:
                    print(f"[!] Gagal ambil 1 review: {e}")
                    continue

            # Klik tombol next halaman review jika ada
            try:
                next_btn = driver.find_element(By.ID, "id_next_page")
                driver.execute_script("arguments[0].click();", next_btn)
                page += 1
            except:
                break  # tidak ada tombol next

        except Exception as e:
            print(f"[!] Gagal ambil review di halaman {page}: {e}")
            break

    return reviews
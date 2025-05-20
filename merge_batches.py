# merge_batches.py

import pandas as pd
import os

# Gabung dan simpan ulang hasil detail
if os.path.exists("data/tmp_details.csv"):
    df_details = pd.read_csv("data/tmp_details.csv").drop_duplicates()
    df_details.to_csv("data/products_detail.csv", index=False, encoding="utf-8-sig")
    print(f"✅ Detail produk digabung dan disimpan: {len(df_details)} baris")
else:
    print("⚠️ Tidak ditemukan tmp_details.csv")

# Gabung dan simpan ulang hasil review
if os.path.exists("data/tmp_reviews.csv"):
    df_reviews = pd.read_csv("data/tmp_reviews.csv").drop_duplicates()
    df_reviews.to_csv("data/reviews.csv", index=False, encoding="utf-8-sig")
    print(f"✅ Review digabung dan disimpan: {len(df_reviews)} baris")
else:
    print("⚠️ Tidak ditemukan tmp_reviews.csv")

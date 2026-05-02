import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

np.random.seed(42)
random.seed(42)

NUM_RECORDS = 1200

categories = {
    "Electronics":    {"products": ["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch"], "price_range": (5000, 80000)},
    "Clothing":       {"products": ["T-Shirt", "Jeans", "Jacket", "Saree", "Kurta"],               "price_range": (299,  5000)},
    "Home & Kitchen": {"products": ["Mixer", "Pressure Cooker", "Bedsheet", "Curtains", "Lamp"],   "price_range": (499,  8000)},
    "Books":          {"products": ["Fiction Novel", "Self Help", "Textbook", "Comics", "Magazine"],"price_range": (99,   1500)},
    "Sports":         {"products": ["Cricket Bat", "Football", "Yoga Mat", "Dumbbells", "Racket"], "price_range": (299,  6000)},
    "Beauty":         {"products": ["Moisturizer", "Lipstick", "Perfume", "Shampoo", "Serum"],     "price_range": (199,  3000)},
}

start_date = datetime(2023, 1, 1)
end_date   = datetime(2024, 12, 31)

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

records = []
for i in range(1, NUM_RECORDS + 1):
    category = random.choices(
        list(categories.keys()),
        weights=[30, 20, 15, 10, 15, 10],
        k=1
    )[0]

    cat_data   = categories[category]
    product    = random.choice(cat_data["products"])
    unit_price = round(random.uniform(*cat_data["price_range"]), 2)
    quantity   = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 12, 8, 5], k=1)[0]
    total_price = round(unit_price * quantity, 2)

    order_date = random_date(start_date, end_date)

    records.append({
        "order_id":         f"ORD{i:05d}",
        "customer_id":      f"CUST{random.randint(1, 400):04d}",
        "product_id":       f"PROD{random.randint(1, 100):03d}",
        "order_date":       order_date.strftime("%Y-%m-%d"),
        "product_category": category,
        "product_name":     product,
        "quantity":         quantity,
        "unit_price":       unit_price,
        "total_price":      total_price,
        "city":             random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad",
                                           "Pune", "Kolkata", "Jaipur", "Ahmedabad", "Lucknow"]),
        "payment_method":   random.choice(["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"]),
    })

df = pd.DataFrame(records)

# Simulate ~3% missing values for realism
missing_idx = np.random.choice(df.index, size=int(0.03 * NUM_RECORDS), replace=False)
df.loc[missing_idx[:15], "city"]           = np.nan
df.loc[missing_idx[15:25], "payment_method"] = np.nan

os.makedirs("data", exist_ok=True)
df.to_csv("data/ecommerce_transactions.csv", index=False)
print(f"Dataset generated: {len(df)} records")
print(f"Columns: {list(df.columns)}")
print(f"\nSample:\n{df.head()}")
print(f"\nMissing values:\n{df.isnull().sum()}")

from flask import Flask, jsonify, request, render_template, send_file
import pandas as pd
import numpy as np
import os
import io
from datetime import datetime
from report_generator import generate_pdf_report

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Load & preprocess data once at startup
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "ecommerce_transactions.csv")

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year"]    = df["order_date"].dt.year
    df["month"]   = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter
    df["city"].fillna("Unknown", inplace=True)
    df["payment_method"].fillna("Unknown", inplace=True)
    return df

df = load_data()

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def filter_by_date(dataframe, start_date, end_date):
    mask = (dataframe["order_date"] >= start_date) & (dataframe["order_date"] <= end_date)
    return dataframe[mask]

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/kpis")
def api_kpis():
    start = request.args.get("start_date")
    end   = request.args.get("end_date")
    data  = filter_by_date(df, start, end) if start and end else df

    total_sales     = round(float(data["total_price"].sum()), 2)
    total_orders    = int(data["order_id"].nunique())
    avg_order_value = round(total_sales / total_orders, 2) if total_orders else 0
    total_customers = int(data["customer_id"].nunique())
    total_units     = int(data["quantity"].sum())

    return jsonify({
        "total_sales":     total_sales,
        "total_orders":    total_orders,
        "avg_order_value": avg_order_value,
        "total_customers": total_customers,
        "total_units_sold": total_units,
    })

@app.route("/api/sales_by_month")
def api_sales_by_month():
    start = request.args.get("start_date")
    end   = request.args.get("end_date")
    data  = filter_by_date(df, start, end) if start and end else df

    monthly = (
        data.groupby(["year", "month"])["total_price"]
        .sum()
        .reset_index()
        .sort_values(["year", "month"])
    )
    monthly["label"] = monthly.apply(
        lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1
    )
    return jsonify({
        "labels": monthly["label"].tolist(),
        "values": monthly["total_price"].round(2).tolist(),
    })

@app.route("/api/sales_by_quarter")
def api_sales_by_quarter():
    quarterly = (
        df.groupby(["year", "quarter"])["total_price"]
        .sum()
        .reset_index()
        .sort_values(["year", "quarter"])
    )
    quarterly["label"] = quarterly.apply(
        lambda r: f"Q{int(r['quarter'])} {int(r['year'])}", axis=1
    )
    return jsonify({
        "labels": quarterly["label"].tolist(),
        "values": quarterly["total_price"].round(2).tolist(),
    })

@app.route("/api/top_products")
def api_top_products():
    n = int(request.args.get("n", 10))
    top = (
        df.groupby("product_name")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    return jsonify({
        "labels": top["product_name"].tolist(),
        "values": top["total_price"].round(2).tolist(),
    })

@app.route("/api/sales_by_category")
def api_sales_by_category():
    cat = (
        df.groupby("product_category")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return jsonify({
        "labels": cat["product_category"].tolist(),
        "values": cat["total_price"].round(2).tolist(),
    })

@app.route("/api/payment_methods")
def api_payment_methods():
    pay = df["payment_method"].value_counts().reset_index()
    pay.columns = ["method", "count"]
    return jsonify({
        "labels": pay["method"].tolist(),
        "values": pay["count"].tolist(),
    })

@app.route("/api/top_cities")
def api_top_cities():
    cities = (
        df[df["city"] != "Unknown"]
        .groupby("city")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    return jsonify({
        "labels": cities["city"].tolist(),
        "values": cities["total_price"].round(2).tolist(),
    })

# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------
@app.route("/api/generate_report")
def api_generate_report():
    start_date = request.args.get("start_date", "2023-01-01")
    end_date   = request.args.get("end_date",   "2024-12-31")
    fmt        = request.args.get("format", "pdf").lower()

    filtered = filter_by_date(df, start_date, end_date)

    if fmt == "csv":
        csv_buffer = io.StringIO()
        filtered.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"sales_report_{start_date}_to_{end_date}.csv",
        )
    else:
        pdf_path = generate_pdf_report(filtered, start_date, end_date)
        return send_file(pdf_path, as_attachment=True,
                         download_name=f"sales_report_{start_date}_to_{end_date}.pdf")

if __name__ == "__main__":
    print("Starting E-Commerce Insights Server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)

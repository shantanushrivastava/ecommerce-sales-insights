# 🛒 E-Commerce Sales Insights Dashboard

> **TCS Industry Project** | Data Analytics & Business Intelligence

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=for-the-badge&logo=chartdotjs)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🌐 Live Demo
👉 [Click here to view Dashboard](https://ecommerce-sales-insights.onrender.com)

---

## 📌 Overview

A full-stack **Business Intelligence Dashboard** built for analyzing e-commerce transaction data. This project provides real-time sales insights through interactive visualizations, KPI tracking, and automated report generation — designed to support data-driven business decisions.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📊 Interactive Dashboard | 6 dynamic charts powered by Chart.js |
| 💰 KPI Cards | Total Revenue, Orders, Avg Order Value, Customers |
| 📅 Date Filter | Filter all insights by custom date range |
| 📈 Sales Trends | Monthly & Quarterly revenue analysis |
| 🏆 Top Products | Best performing products by revenue |
| 🗺️ City Analysis | Top 10 cities by sales volume |
| 💳 Payment Insights | Payment method distribution |
| 📄 PDF Reports | Auto-generated professional PDF reports |
| 📤 CSV Export | Export filtered data as CSV |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** — Core language
- **Flask** — REST API & web server
- **Pandas / NumPy** — Data processing & analysis
- **FPDF2** — PDF report generation

### Frontend
- **HTML5 / CSS3 / JavaScript**
- **Chart.js** — Interactive data visualizations

### Data & Analysis
- **Jupyter Notebook** — Exploratory Data Analysis (EDA)
- **Matplotlib / Seaborn** — Statistical visualizations

---

## 📁 Project Structure

```
project_final/
├── data/
│   └── ecommerce_transactions.csv   # 1200 transaction records
├── notebooks/
│   └── eda_analysis.ipynb           # Exploratory Data Analysis
├── templates/
│   └── index.html                   # Dashboard frontend
├── static/
│   ├── css/style.css
│   └── js/main.js
├── reports/                         # Auto-generated reports
├── app.py                           # Flask backend & API routes
├── report_generator.py              # PDF generation logic
├── generate_dataset.py              # Synthetic dataset generator
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.10+
- pip

### Step 1 — Clone the Repository

```bash
git clone https://github.com/shantanushrivastava/ecommerce-sales-insights.git
cd ecommerce-sales-insights
```

### Step 2 — Install Dependencies

```bash
pip install flask pandas numpy matplotlib seaborn fpdf2 jupyter
```

### Step 3 — Generate Dataset

```bash
python generate_dataset.py
```
> Creates `data/ecommerce_transactions.csv` with 1200 synthetic records.

### Step 4 — (Optional) Run EDA Notebook

```bash
jupyter notebook notebooks/eda_analysis.ipynb
```
> Run all cells to generate charts saved in `/reports/`.

### Step 5 — Start the Flask Server

```bash
python app.py
```

### Step 6 — Open Dashboard

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/kpis` | GET | KPI summary (revenue, orders, customers) |
| `/api/sales_by_month` | GET | Monthly sales trend |
| `/api/sales_by_quarter` | GET | Quarterly sales trend |
| `/api/top_products` | GET | Top N products by revenue |
| `/api/sales_by_category` | GET | Sales by product category |
| `/api/payment_methods` | GET | Payment method distribution |
| `/api/top_cities` | GET | Top 10 cities by revenue |
| `/api/generate_report` | GET | Download PDF or CSV report |

---

## 📊 Dataset Information

The dataset is synthetically generated with realistic e-commerce patterns:

- **Records:** 1,200 transactions
- **Date Range:** 2023 – 2024
- **Fields:** `order_id`, `customer_id`, `product_name`, `product_category`, `quantity`, `unit_price`, `total_price`, `order_date`, `city`, `payment_method`

---

> ⭐ If you found this project helpful, please give it a star on GitHub!

# E-Commerce Sales Insights
### TCS Industry Project | Data Analytics & Business Intelligence

---

## Project Structure
```
ecommerce_project/
├── data/                          # Auto-generated dataset
├── notebooks/
│   └── eda_analysis.ipynb         # Jupyter EDA notebook
├── templates/
│   └── index.html                 # Dashboard frontend
├── reports/                       # Generated PDFs/PNGs
├── generate_dataset.py            # Step 1: Create dataset
├── app.py                         # Flask backend
├── report_generator.py            # PDF generation logic
└── README.md
```

---

## Setup & Run (Step by Step)

### Step 1 - Generate Dataset
```bash
python generate_dataset.py
```
Creates `data/ecommerce_transactions.csv` with 1200 records.

### Step 2 - Run Jupyter Notebook (EDA)
```bash
jupyter notebook notebooks/eda_analysis.ipynb
```
Run all cells. Charts will be saved in `/reports/`.

### Step 3 - Start Flask Server
```bash
python app.py
```

### Step 4 - Open Dashboard
Open browser: **http://127.0.0.1:5000**

---

## Features
- Interactive dashboard with 6 charts (Chart.js)
- KPI cards: Total Revenue, Orders, Avg Order Value, Customers
- Sales trend by month, category, product, city, payment method
- PDF report generation with FPDF2
- CSV export with date range filter

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Data Analysis | Python, Pandas, Matplotlib, Seaborn |
| Backend | Flask, FPDF2 |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Notebook | Jupyter |

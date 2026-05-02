import os
from fpdf import FPDF
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

class SalesReport(FPDF):
    def header(self):
        self.set_fill_color(41, 128, 185)
        self.rect(0, 0, 210, 22, "F")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 14, "E-Commerce Sales Insights Report", align="C", ln=True)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 8, f"Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}", align="C", ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()} | E-Commerce Sales Insights | Confidential", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(236, 240, 241)
        self.set_text_color(44, 62, 80)
        self.cell(0, 9, f"  {title}", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def kpi_box(self, label, value, x, y, w=45, h=22):
        self.set_fill_color(41, 128, 185)
        self.rect(x, y, w, h, "F")
        self.set_xy(x, y + 2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(255, 255, 255)
        self.cell(w, 8, value, align="C", ln=False)
        self.set_xy(x, y + 11)
        self.set_font("Helvetica", "", 7)
        self.cell(w, 8, label, align="C")
        self.set_text_color(0, 0, 0)

    def data_table(self, headers, rows, col_widths):
        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        for h, w in zip(headers, col_widths):
            self.cell(w, 8, str(h), border=0, fill=True, align="C")
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 8)
        self.set_text_color(0, 0, 0)
        for i, row in enumerate(rows):
            fill_color = (245, 245, 245) if i % 2 == 0 else (255, 255, 255)
            self.set_fill_color(*fill_color)
            for val, w in zip(row, col_widths):
                self.cell(w, 7, str(val), border=0, fill=True, align="C")
            self.ln()
        self.ln(3)


def generate_pdf_report(df, start_date, end_date):
    pdf = SalesReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- Report Period ---
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Report Period:  {start_date}  to  {end_date}    |    Total Records: {len(df):,}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # --- KPI Section ---
    pdf.section_title("Key Performance Indicators")

    total_sales     = df["total_price"].sum()
    total_orders    = df["order_id"].nunique()
    avg_order_value = total_sales / total_orders if total_orders else 0
    total_customers = df["customer_id"].nunique()

    kpis = [
        ("Total Revenue",    f"Rs {total_sales:,.0f}"),
        ("Total Orders",     f"{total_orders:,}"),
        ("Avg Order Value",  f"Rs {avg_order_value:,.0f}"),
        ("Unique Customers", f"{total_customers:,}"),
    ]

    start_x = 15
    for i, (label, value) in enumerate(kpis):
        pdf.kpi_box(label, value, x=start_x + i * 48, y=pdf.get_y(), w=44, h=20)
    pdf.ln(28)

    # --- Monthly Sales Table ---
    pdf.section_title("Monthly Sales Summary")
    df["month_label"] = df["order_date"].dt.strftime("%b %Y")
    monthly = df.groupby("month_label").agg(
        Orders=("order_id", "count"),
        Revenue=("total_price", "sum"),
        Avg_Value=("total_price", "mean"),
    ).reset_index()
    monthly["Revenue"]   = monthly["Revenue"].apply(lambda x: f"Rs {x:,.2f}")
    monthly["Avg_Value"] = monthly["Avg_Value"].apply(lambda x: f"Rs {x:,.2f}")
    monthly.columns = ["Month", "Orders", "Revenue", "Avg Order Value"]

    pdf.data_table(
        headers   = monthly.columns.tolist(),
        rows      = monthly.values.tolist(),
        col_widths= [40, 30, 60, 60],
    )

    # --- Category Breakdown ---
    pdf.section_title("Sales by Product Category")
    cat = df.groupby("product_category").agg(
        Orders=("order_id", "count"),
        Revenue=("total_price", "sum"),
    ).sort_values("Revenue", ascending=False).reset_index()
    cat["Revenue"] = cat["Revenue"].apply(lambda x: f"Rs {x:,.2f}")
    cat.columns = ["Category", "Orders", "Revenue"]

    pdf.data_table(
        headers   = cat.columns.tolist(),
        rows      = cat.values.tolist(),
        col_widths= [60, 40, 60],
    )

    # --- Top Products ---
    pdf.section_title("Top 10 Products by Revenue")
    top_prod = df.groupby("product_name")["total_price"].sum().sort_values(ascending=False).head(10).reset_index()
    top_prod["Rank"]        = range(1, 11)
    top_prod["total_price"] = top_prod["total_price"].apply(lambda x: f"Rs {x:,.2f}")
    top_prod = top_prod[["Rank", "product_name", "total_price"]]
    top_prod.columns = ["Rank", "Product", "Revenue"]

    pdf.data_table(
        headers   = top_prod.columns.tolist(),
        rows      = top_prod.values.tolist(),
        col_widths= [15, 85, 60],
    )

    # --- Payment Methods ---
    pdf.section_title("Payment Method Distribution")
    pay = df["payment_method"].value_counts().reset_index()
    pay.columns = ["Payment Method", "Orders"]
    pay["% Share"] = (pay["Orders"] / pay["Orders"].sum() * 100).round(1).astype(str) + "%"

    pdf.data_table(
        headers   = pay.columns.tolist(),
        rows      = pay.values.tolist(),
        col_widths= [60, 40, 40],
    )

    # --- Save ---
    output_path = os.path.join(REPORTS_DIR, "sales_report.pdf")
    pdf.output(output_path)
    print(f"PDF saved to {output_path}")
    return output_path

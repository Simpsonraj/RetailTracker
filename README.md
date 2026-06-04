# RetailTracker
Retail demand intelligence system - SQL, Python, Power BI, 5000+ records validated, KPI dashboard replacing manual reporting

#  RetailTracker — Retail Demand Intelligence System

**Author:** Simpson Gundlapally  
**Tools:** SQL · Python (Pandas), Excel, Power BI  
**Dataset:** 5000+ retail transaction records, 2025  
**Domain:** Retail Analytics, Demand Forecasting, Business Intelligence

---

## Context & Objectives

A multi-city retail chain operating across 5 store locations lacked centralized visibility into its sales data. The raw transactional data was siloed, uncleaned, and prone to schema mismatches, preventing leadership from understanding core revenue drivers, underperforming stores, or seasonal demand patterns.

My goal for this project was to clean the transactional layer and build an analytics pipeline to uncover:
* **Revenue Drivers:** Which product categories and regions anchor the business.
* **Leakage & Risks:** Monthly sales seasonality, return rate anomalies, and margin erosion from heavy discounting.
---

##  Project Structure

```
RetailTracker/
│
├── retail_raw_data.csv          ← Original dataset (5000+ records, with dirty data)
├── retail_cleaned_data.csv      ← Cleaned dataset (4,940 records)
├── category_summary.csv         ← Category-level aggregated analysis
├── monthly_trend.csv            ← Month-by-month revenue trend
│
├── retail_analysis.sql          ← All SQL queries (exploration → KPIs)
├── retail_analysis.py           ← Full Python analysis (Pandas + Matplotlib)
├── RetailTracker_Complete.xlsx  ← Excel workbook (7 sheets: raw, clean, KPIs, guide)
│
├── RetailTracker_Dashboard.png  ← Dashboard visualization output
└── README.md                    ← This file
```

---

##  Core KPIs

| KPI | Value |
|---|---|
| Total Transactions | 4,940 |
| Total Net Revenue | ₹8.47 Crores |
| Total Discount Given | ₹87.6 Lakhs |
| Average Order Value | ₹17,140 |
| Total Units Sold | 22,123 |
| Overall Return Rate | 7.3% |
| Data Accuracy (after cleaning) | 95.0% |

---

##  Data Cleaning Summary

| Issue Found | Records |
|---|---|
| Missing date values | 260 |
| Missing quantity | 94 |
| Invalid discount values (< 0 or > 100) | 184 |
| Missing net sales | 260 |
| **Total dirty records removed** | **260** |
| **Clean records retained** | **4,940** |

---

##  Key Insights

1. **Heavy Revenue Concentration:** Electronics completely dominates the business, driving 71.97% of total revenue. In fact, the top 3 categories (Electronics, Home Appliances, Clothing) capture 98.1% of all sales.
2. **Regional Leader:** Hyderabad emerged as the top-performing city across all tracked store locations.
3. **Product Quality Red Flags:** The Grocery category has a standout return rate of 7.97%, heavily hinting at potential freshness or supplier quality issues.
4. **Payment Preferences:** Digital adoption is high; UPI and Credit Cards are the primary transactional drivers.
5. **Discount Elasticity:** The 20% discount tier appears to be the sweet spot, driving the highest average basket size without completely destroying margins.
   
---

##  Strategic Recommendations

- **Inventory Optimization:** Allocate higher capital and shelf space to Electronics during Q3–Q4 to capture peak seasonal demand.
- **Supply Chain Audit:** Review grocery suppliers to trace the root cause of the 7.97% return rate.
- **Loyalty Program Expansion:** Incentivize the high-AOV (Average Order Value) customer segments with tiered rewards to boost retention.
- **Discount Guardrails:** Re-evaluate the ROI on the ₹87.6 Lakhs given away in discounts to ensure it's actually driving incremental volume rather than cannibalizing full-price sales.
  
---

##  Setup & Execution

```bash
# 1. Generate raw dataset
python3 generate_data.py

# 2. Run full analysis
python3 retail_analysis.py

# 3. Open SQL queries in any SQL editor (MySQL / PostgreSQL / SQLite)
# Load retail_raw_data.csv as table: retail_sales
# Run retail_analysis.sql step by step

# 4. Open RetailTracker_Complete.xlsx in Excel
# See "Power BI Guide" sheet for dashboard instructions
```

---

##  Power BI Dashboard Pages

**Page 1 — Executive Summary**
- KPI Cards: Revenue, Transactions, Avg Order, Return Rate
- Monthly Revenue Trend Line

**Page 2 — Category Intelligence**
- Revenue by Category (Bar Chart)
- Revenue Share Donut Chart
- Return Rate by Category

**Page 3 — Store & City Performance**
- City Revenue Map
- Payment Method Distribution
- Customer Segment Analysis

---

##  Tags
`Data Analytics` `SQL` `Python` `Pandas` `Power BI` `Excel` `Retail Analytics` `EDA` `Dashboard` `KPI`

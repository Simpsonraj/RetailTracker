# ============================================================
# RETAILTRACKER: Retail Demand Intelligence System
# Author: Simpson Gundlapally
# Tools: Python (Pandas, Matplotlib, Seaborn)
# Dataset: retail_raw_data.csv (5,200 records)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Plot style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
COLORS = ['#1F3864','#2E75B6','#4BACC6','#70AD47','#FFC000','#FF6B6B']

# ============================================================
# STEP 1: LOAD & EXPLORE
# ============================================================
df = pd.read_csv('retail_raw_data.csv')

print("=" * 55)
print("  STEP 1: RAW DATA OVERVIEW")
print("=" * 55)
print(f"Shape          : {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Columns        : {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ============================================================
# STEP 2: DATA CLEANING
# ============================================================
print("\n" + "=" * 55)
print("  STEP 2: DATA QUALITY CHECK")
print("=" * 55)

print(f"\nMissing values per column:\n{df.isnull().sum()}")

# Count dirty records
missing_date = df['Date'].isna() | (df['Date'] == '')
missing_qty  = df['Quantity'].isna()
bad_discount = df['Discount_Percent'].apply(
    lambda x: pd.notna(x) and (x < 0 or x > 100))
missing_sales = df['Net_Sales'].isna()

total_dirty = (missing_date | missing_qty | bad_discount | missing_sales).sum()
print(f"\nDirty record breakdown:")
print(f"  Missing dates       : {missing_date.sum()}")
print(f"  Missing quantity    : {missing_qty.sum()}")
print(f"  Invalid discounts   : {bad_discount.sum()}")
print(f"  Missing net sales   : {missing_sales.sum()}")
print(f"  TOTAL dirty records : {total_dirty}")

# Clean the data
df_clean = df[~(missing_date | missing_qty | bad_discount | missing_sales)].copy()
df_clean['Date'] = pd.to_datetime(df_clean['Date'])
df_clean['Month'] = df_clean['Date'].dt.to_period('M').astype(str)
df_clean['Month_Num'] = df_clean['Date'].dt.month
df_clean['Quarter'] = 'Q' + df_clean['Date'].dt.quarter.astype(str)

print(f"\nAfter cleaning: {len(df_clean)} records retained")
print(f"Data accuracy rate: {round(len(df_clean)/len(df)*100,1)}%")

# ============================================================
# STEP 3: KPI CALCULATIONS
# ============================================================
print("\n" + "=" * 55)
print("  STEP 3: KEY PERFORMANCE INDICATORS")
print("=" * 55)

total_revenue   = df_clean['Net_Sales'].sum()
total_gross     = df_clean['Gross_Sales'].sum()
total_discount  = df_clean['Discount_Amount'].sum()
avg_order_val   = df_clean['Net_Sales'].mean()
total_units     = df_clean['Quantity'].sum()
return_rate     = (df_clean['Return_Flag']=='Yes').mean() * 100
total_txns      = len(df_clean)

print(f"  Total Transactions  : {total_txns:,}")
print(f"  Total Net Revenue   : ₹{total_revenue:,.0f}")
print(f"  Total Discount Given: ₹{total_discount:,.0f}")
print(f"  Avg Order Value     : ₹{avg_order_val:,.0f}")
print(f"  Total Units Sold    : {total_units:,.0f}")
print(f"  Overall Return Rate : {return_rate:.1f}%")

# ============================================================
# STEP 4: CATEGORY ANALYSIS
# ============================================================
cat_summary = df_clean.groupby('Category').agg(
    Transactions=('Transaction_ID','count'),
    Units_Sold=('Quantity','sum'),
    Net_Revenue=('Net_Sales','sum'),
    Avg_Order_Value=('Net_Sales','mean'),
    Return_Count=('Return_Flag', lambda x: (x=='Yes').sum())
).reset_index()
cat_summary['Revenue_Share_Pct'] = (cat_summary['Net_Revenue'] /
                                     cat_summary['Net_Revenue'].sum() * 100).round(2)
cat_summary['Return_Rate_Pct']   = (cat_summary['Return_Count'] /
                                     cat_summary['Transactions'] * 100).round(2)
cat_summary = cat_summary.sort_values('Net_Revenue', ascending=False)

print("\n" + "=" * 55)
print("  STEP 4: REVENUE BY CATEGORY")
print("=" * 55)
print(cat_summary[['Category','Transactions','Net_Revenue',
                    'Revenue_Share_Pct','Return_Rate_Pct']].to_string(index=False))

# ============================================================
# STEP 5: MONTHLY TREND
# ============================================================
monthly = df_clean.groupby('Month').agg(
    Transactions=('Transaction_ID','count'),
    Net_Revenue=('Net_Sales','sum'),
    Units_Sold=('Quantity','sum')
).reset_index().sort_values('Month')

# ============================================================
# STEP 6: CITY PERFORMANCE
# ============================================================
city_perf = df_clean.groupby('City').agg(
    Transactions=('Transaction_ID','count'),
    Net_Revenue=('Net_Sales','sum'),
    Avg_Order=('Net_Sales','mean')
).reset_index().sort_values('Net_Revenue', ascending=False)

# ============================================================
# STEP 7: TOP PRODUCTS
# ============================================================
top_products = df_clean.groupby(['Product_Name','Category']).agg(
    Units_Sold=('Quantity','sum'),
    Revenue=('Net_Sales','sum')
).reset_index().sort_values('Revenue', ascending=False).head(10)

# ============================================================
# STEP 8: DISCOUNT IMPACT
# ============================================================
discount_impact = df_clean.groupby('Discount_Percent').agg(
    Transactions=('Transaction_ID','count'),
    Avg_Units=('Quantity','mean'),
    Net_Revenue=('Net_Sales','sum')
).reset_index()

# ============================================================
# STEP 9: VISUALIZATIONS (Dashboard-quality plots)
# ============================================================
fig = plt.figure(figsize=(20, 24))
fig.suptitle('RetailTracker — Retail Demand Intelligence Dashboard\nSimpson Gundlapally | 2024',
             fontsize=18, fontweight='bold', color='#1F3864', y=0.98)

# --- Plot 1: Revenue by Category (Horizontal Bar) ---
ax1 = fig.add_subplot(4, 2, 1)
bars = ax1.barh(cat_summary['Category'], cat_summary['Net_Revenue']/1e6,
                color=COLORS[:len(cat_summary)], edgecolor='white', height=0.6)
ax1.set_title('Net Revenue by Category (₹ Millions)', fontweight='bold', color='#1F3864')
ax1.set_xlabel('Revenue (₹ Millions)')
for bar, val in zip(bars, cat_summary['Net_Revenue']/1e6):
    ax1.text(bar.get_width()+0.02, bar.get_y()+bar.get_height()/2,
             f'₹{val:.1f}M', va='center', fontsize=9)
ax1.invert_yaxis()

# --- Plot 2: Revenue Share Pie ---
ax2 = fig.add_subplot(4, 2, 2)
wedges, texts, autotexts = ax2.pie(
    cat_summary['Revenue_Share_Pct'],
    labels=cat_summary['Category'],
    autopct='%1.1f%%', colors=COLORS,
    startangle=90, pctdistance=0.8)
ax2.set_title('Revenue Share by Category', fontweight='bold', color='#1F3864')

# --- Plot 3: Monthly Revenue Trend ---
ax3 = fig.add_subplot(4, 2, (3,4))
ax3.plot(monthly['Month'], monthly['Net_Revenue']/1e6,
         marker='o', color='#1F3864', linewidth=2.5, markersize=7)
ax3.fill_between(range(len(monthly)), monthly['Net_Revenue']/1e6,
                 alpha=0.1, color='#2E75B6')
ax3.set_xticks(range(len(monthly)))
ax3.set_xticklabels(monthly['Month'], rotation=45, ha='right', fontsize=8)
ax3.set_title('Monthly Net Revenue Trend (₹ Millions)', fontweight='bold', color='#1F3864')
ax3.set_ylabel('Revenue (₹ Millions)')
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter('₹%.1fM'))

# --- Plot 4: City Performance ---
ax4 = fig.add_subplot(4, 2, 5)
city_colors = COLORS[:len(city_perf)]
bars4 = ax4.bar(city_perf['City'], city_perf['Net_Revenue']/1e6,
                color=city_colors, edgecolor='white')
ax4.set_title('Revenue by City', fontweight='bold', color='#1F3864')
ax4.set_ylabel('Revenue (₹ Millions)')
ax4.tick_params(axis='x', rotation=15)
for bar in bars4:
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
             f'₹{bar.get_height():.1f}M', ha='center', fontsize=8)

# --- Plot 5: Payment Method ---
ax5 = fig.add_subplot(4, 2, 6)
pay_data = df_clean['Payment_Method'].value_counts()
ax5.bar(pay_data.index, pay_data.values, color=COLORS, edgecolor='white')
ax5.set_title('Transactions by Payment Method', fontweight='bold', color='#1F3864')
ax5.set_ylabel('Number of Transactions')
ax5.tick_params(axis='x', rotation=20)

# --- Plot 6: Top 10 Products ---
ax6 = fig.add_subplot(4, 2, (7, 8))
top10 = top_products.head(10)
bars6 = ax6.barh(top10['Product_Name'], top10['Revenue']/1e6,
                 color='#2E75B6', edgecolor='white', height=0.6)
ax6.set_title('Top 10 Products by Revenue (₹ Millions)', fontweight='bold', color='#1F3864')
ax6.set_xlabel('Revenue (₹ Millions)')
ax6.invert_yaxis()
for bar in bars6:
    ax6.text(bar.get_width()+0.01, bar.get_y()+bar.get_height()/2,
             f'₹{bar.get_width():.2f}M', va='center', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/home/claude/RetailTracker/RetailTracker_Dashboard.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("\n✅ Dashboard visualization saved.")

# ============================================================
# STEP 10: BUSINESS INSIGHTS
# ============================================================
top_cat = cat_summary.iloc[0]
print("\n" + "=" * 55)
print("  STEP 10: KEY BUSINESS INSIGHTS")
print("=" * 55)
print(f"\n1. Top revenue category  : {top_cat['Category']} "
      f"({top_cat['Revenue_Share_Pct']}% of total revenue)")
print(f"2. Highest return rate   : "
      f"{cat_summary.sort_values('Return_Rate_Pct',ascending=False).iloc[0]['Category']}")
print(f"3. Best performing city  : {city_perf.iloc[0]['City']}")
print(f"4. Avg order value       : ₹{avg_order_val:,.0f}")
print(f"5. Overall return rate   : {return_rate:.1f}%")
print(f"6. Top 3 categories drive: "
      f"{cat_summary.head(3)['Revenue_Share_Pct'].sum():.1f}% of revenue")
print("\n✅ Analysis complete. Export files ready for Power BI.")

# Save cleaned data for Excel/Power BI
df_clean.to_csv('/home/claude/RetailTracker/retail_cleaned_data.csv', index=False)
cat_summary.to_csv('/home/claude/RetailTracker/category_summary.csv', index=False)
monthly.to_csv('/home/claude/RetailTracker/monthly_trend.csv', index=False)
print("✅ Cleaned CSVs exported.")

#!/usr/bin/env python
# coding: utf-8

# In[1]:


# New Project - US Equities Performance & Risk Analytics


# In[2]:


import requests
import pandas as pd
import time
from bs4 import BeautifulSoup


# In[3]:


# Tickers - Companies: Apple, Microsoft, Google, Amazon and JP Morgan

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM"]

headers = {"User-Agent": "Mozilla/5.0"}

columns = [
    "Date", "Open", "High", "Low",
    "Close", "Adj_Close", "Volume", "Ticker"
]

raw_records = []


# In[4]:


for ticker in tickers:
    url = f"https://finance.yahoo.com/quote/{ticker}/history/"

    response = requests.get(
        url, headers=headers, timeout=30
    )
    response.raise_for_status()


# In[5]:


soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table")


# In[6]:


for ticker in tickers:
   #  code to request and parse the webpage goes here
   table = soup.find("table")

   if table is None:
       print(f"No HTML table found for {ticker}")
       continue
       ticker_count = 0


# In[7]:


for ticker in tickers:
    ticker_count = 0

    # Your existing webpage request and table extraction code

    for row in table.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) != 7:
            continue

        values = [
            cell.get_text(" ", strip=True)
            for cell in cells
        ]
 # Keep genuine daily price records only
        try:
            pd.to_datetime(values[0], format="%b %d, %Y")
        except (ValueError, TypeError):
            continue

        raw_records.append(values + [ticker])
        ticker_count += 1

    print(f"{ticker}: {ticker_count} rows scraped")
    time.sleep(2)


# In[8]:


# Create raw DataFrame without calculated columns
raw_df = pd.DataFrame(raw_records, columns=columns)


# In[9]:


raw_df.to_csv(r"C:\Users\Samson\Downloads\Stock_Raw_Data.csv", index=False)


# In[10]:


print("\nRaw dataset shape:", raw_df.shape)
print(raw_df.head())
print("\nSaved: Stock_Raw_Data.csv")


# In[11]:


import pandas as pd

# Load raw scraped data
clean_df = pd.read_csv(r"C:\Users\Samson\Downloads\Stock_Raw_Data.csv")

print("Original shape:", clean_df.shape)


# In[12]:


# Remove whitespace from text fields
clean_df["Date"] = clean_df["Date"].astype(str).str.strip()
clean_df["Ticker"] = clean_df["Ticker"].astype(str).str.strip()


# In[13]:


# Convert dates
clean_df["Date"] = pd.to_datetime(
    clean_df["Date"], format="%b %d, %Y", errors="coerce"
)


# In[14]:


# Convert numeric columns
numeric_cols = [
    "Open", "High", "Low", "Close",
    "Adj_Close", "Volume"
]

for col in numeric_cols:
    clean_df[col] = pd.to_numeric(
        clean_df[col].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )


# In[15]:


# Check missing values before removing invalid records
print("\nMissing values before cleaning:")
print(clean_df.isnull().sum())


# In[16]:


# Remove rows missing essential fields
clean_df = clean_df.dropna(
    subset=["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
)

# Remove duplicate company-date observations
clean_df = clean_df.drop_duplicates(
    subset=["Ticker", "Date"], keep="first"
)


# In[17]:


# Check basic price consistency
invalid_prices = (
    (clean_df["Open"] <= 0) |
    (clean_df["High"] <= 0) |
    (clean_df["Low"] <= 0) |
    (clean_df["Close"] <= 0) |
    (clean_df["High"] < clean_df["Low"]) |
    (clean_df["High"] < clean_df["Open"]) |
    (clean_df["High"] < clean_df["Close"]) |
    (clean_df["Low"] > clean_df["Open"]) |
    (clean_df["Low"] > clean_df["Close"]) |
    (clean_df["Volume"] < 0)
)

print("\nInvalid price rows:", invalid_prices.sum())


# In[18]:


# Review invalid rows before deciding whether to exclude them
print(clean_df.loc[invalid_prices].head())


# In[19]:


# Sort chronologically within each ticker
clean_df = clean_df.sort_values(
    ["Ticker", "Date"]
).reset_index(drop=True)


# In[20]:


print("\nCleaned shape:", clean_df.shape)
print("\nMissing values after cleaning:")
print(clean_df.isnull().sum())


# In[21]:


print("\nRows per ticker:")
print(clean_df.groupby("Ticker").size())


# In[22]:


# Work on a separate DataFrame with calculated columns
analysis_df = clean_df.copy()


# In[23]:


# Price change from previous trading observation for each ticker
analysis_df["Price_Change"] = (
    analysis_df.groupby("Ticker")["Close"].diff()
)


# In[24]:


# Daily percentage return
analysis_df["Daily_Return_Pct"] = (
    analysis_df.groupby("Ticker")["Close"].pct_change() * 100
)


# In[25]:


# Daily high-low trading range
analysis_df["Daily_Range"] = (
    analysis_df["High"] - analysis_df["Low"]
)


# In[26]:


# Trading range as a percentage of closing price
analysis_df["Range_Pct"] = (
    analysis_df["Daily_Range"] /
    analysis_df["Close"] * 100
)


# In[27]:


# Rolling standard deviation of daily returns over 20 observations
analysis_df["20_Day_Volatility_Pct"] = (
    analysis_df.groupby("Ticker")["Daily_Return_Pct"]
    .transform(lambda x: x.rolling(window=20, min_periods=20).std())
)


# In[28]:


print("Calculated dataset shape:", analysis_df.shape)
print(analysis_df.head(10))


# In[29]:


# Save cleaned original data
clean_df.to_csv(r"C:\Users\Samson\Downloads\Stock_Cleaned_Data.csv", index=False)


# In[30]:


# Save data with calculated financial indicators
analysis_df.to_csv(r"C:\Users\Samson\Downloads\Stock_Financial_Analysis.csv", index=False)


# In[31]:


print("Raw data shape:", raw_df.shape)
print("Cleaned data shape:", clean_df.shape)
print("Financial analysis shape:", analysis_df.shape)


# In[32]:


print("\nFiles saved successfully:")
print("1. Stock_Raw_Data.csv")
print("2. Stock_Cleaned_Data.csv")
print("3. Stock_Financial_Analysis.csv")


# In[33]:


import os

# Create a folder for all visualisations
visuals_folder = "Stock_Financial_Analysis_Virtuals"

os.makedirs(visuals_folder, exist_ok=True)

print("Folder created at:", os.path.abspath(visuals_folder))


# In[34]:


# Visualization
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Visual 1. Bar chart: average closing price by ticker
plt.figure(figsize=(10, 6))

analysis_df.groupby("Ticker")["Close"].mean().plot(
    kind="bar",
    title="Average Closing Price by Stock"
)

plt.xlabel("Stock Ticker")
plt.ylabel("Average Closing Price (USD)")
plt.tight_layout()

plt.savefig(
    os.path.join(visuals_folder, "01_Average_Closing_Price.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# In[35]:


# Visual 2. Pie chart: share of total trading volume
plt.figure(figsize=(8, 8))

analysis_df.groupby("Ticker")["Volume"].sum().plot(
    kind="pie",
    autopct="%1.1f%%",
    title="Trading Volume Share by Stock"
)

plt.ylabel("")

plt.savefig(
    os.path.join(visuals_folder, "02_Trading_Volume_Share.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# In[36]:


# Visual 3. Column chart: monthly average closing price
monthly_plot = analysis_df.copy()
monthly_plot["Month"] = monthly_plot["Date"].dt.to_period("M").astype(str)

monthly_close = monthly_plot.groupby(
    ["Month", "Ticker"]
)["Close"].mean().unstack()

ax = monthly_close.plot(
    figsize=(12, 6),
    title="Monthly Average Closing Price by Stock"
)

ax.set_xlabel("Month")
ax.set_ylabel("Average Closing Price (USD)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(visuals_folder, "03_Monthly_Closing_Price.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# In[37]:


# Visual 4. Scatter plot: trading volume versus daily return
plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=analysis_df,
    x="Volume",
    y="Daily_Return_Pct",
    hue="Ticker"
)

plt.title("Trading Volume vs Daily Return")
plt.xlabel("Trading Volume")
plt.ylabel("Daily Return (%)")
plt.tight_layout()

plt.savefig(
    os.path.join(visuals_folder, "04_Volume_vs_Daily_Return.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# In[38]:


# Visual 5. Correlation heatmap
corr_cols = [
    "Open", "High", "Low", "Close", "Adj_Close",
    "Volume", "Price_Change", "Daily_Return_Pct",
    "Daily_Range", "Range_Pct", "20_Day_Volatility_Pct"
]

correlation_matrix = analysis_df[corr_cols].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    linewidths=0.5
)
plt.title("Correlation Heatmap of Financial Variables")
plt.tight_layout()

plt.savefig(
    os.path.join(visuals_folder, "05_Correlation_Heatmap.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# In[39]:


# Visual 6: Box plot of daily returns by company
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=analysis_df,
    x="Ticker",
    y="Daily_Return_Pct"
)

plt.title("Daily Return Distribution by Stock")
plt.xlabel("Stock Ticker")
plt.ylabel("Daily Return (%)")
plt.tight_layout()

plt.savefig(
    os.path.join(visuals_folder, "06_Daily_Return_Boxplot.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# In[40]:


# Visual 7: Cumulative growth index by company

plot_df = analysis_df.sort_values(
    ["Ticker", "Date"]
).copy()

# Calculate daily returns from closing prices
plot_df["Return"] = (
    plot_df.groupby("Ticker")["Close"].pct_change()
)

# Set each stock's index to 100 at the beginning
plot_df["Growth_Index"] = (
    plot_df.groupby("Ticker")["Return"]
    .transform(lambda x: (1 + x.fillna(0)).cumprod() * 100)
)

plt.figure(figsize=(12, 6))

for ticker, group in plot_df.groupby("Ticker"):
    plt.plot(
        group["Date"],
        group["Growth_Index"],
        label=ticker
    )

plt.axhline(100, linestyle="--")
plt.title("Cumulative Price Growth Index (Base = 100)")
plt.xlabel("Date")
plt.ylabel("Growth Index (Starting Value = 100)")
plt.legend(title="Ticker")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(visuals_folder, "07_Cumulative_Growth_Index.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# In[41]:


print("Saved visualisations:")

for file in sorted(os.listdir(visuals_folder)):
    print(file)

print("\nTotal files:", len(os.listdir(visuals_folder)))
print("Folder location:", os.path.abspath(visuals_folder))


# In[42]:


import pandas as pd
import numpy as np

numeric_cols = [
    "Open", "High", "Low", "Close", "Adj_Close",
    "Volume", "Price_Change", "Daily_Return_Pct",
    "Daily_Range", "Range_Pct", "20_Day_Volatility_Pct"
]


# In[43]:


# Descriptive statistics
summary_stats = analysis_df[numeric_cols].describe().T

summary_stats["Median"] = analysis_df[numeric_cols].median()
summary_stats["Mode"] = analysis_df[numeric_cols].mode().iloc[0]
summary_stats["Variance"] = analysis_df[numeric_cols].var()
summary_stats["Skewness"] = analysis_df[numeric_cols].skew()

print("KEY SUMMARY STATISTICS")
print(summary_stats.round(3))


# In[44]:


# Save results to CSV
summary_file = os.path.join(
    visuals_folder,
    "Summary_Statistics.csv"
)

summary_stats.round(3).to_csv(summary_file)

print("\nSummary statistics saved to:")
print(os.path.abspath(summary_file))


# In[45]:


# Correlations between numerical columns

correlation_matrix = analysis_df[numeric_cols].corr(
    method="pearson"
)

print("CORRELATION MATRIX")
print(correlation_matrix.round(3))

# Extract unique pairs, excluding self-correlations
upper_triangle = correlation_matrix.where(
    np.triu(
        np.ones(correlation_matrix.shape), k=1
    ).astype(bool)
)

correlation_pairs = (
    upper_triangle.stack()
    .rename("Correlation")
    .reset_index()
)

correlation_pairs.columns = [
    "Variable_1", "Variable_2", "Correlation"
]

correlation_pairs["Absolute_Correlation"] = (
    correlation_pairs["Correlation"].abs()
)

correlation_pairs = correlation_pairs.sort_values(
    "Absolute_Correlation", ascending=False
)

print("\nTOP 15 CORRELATION PAIRS")
print(correlation_pairs.head(15).round(3))


# In[46]:


# Save both results to the folder

matrix_file = os.path.join(
    visuals_folder, "Correlation_Matrix.csv"
)

pairs_file = os.path.join(
    visuals_folder, "Correlation_Pairs.csv"
)

correlation_matrix.round(3).to_csv(matrix_file)
correlation_pairs.round(3).to_csv(
    pairs_file, index=False
)

print("\nFiles saved successfully:")
print(os.path.abspath(matrix_file))
print(os.path.abspath(pairs_file))


# In[47]:


# Look for any outliers or anomalies in the data

def detect_outliers(df, column):
    values = df[column].dropna() 

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ].copy()

    return outliers, lower_bound, upper_bound

for column in [
    "Daily_Return_Pct", "Volume", "Daily_Range"
]:
    outliers, lower, upper = detect_outliers(
        analysis_df, column
    )

    print(f"\nOutlier analysis: {column}")
    print(f"Lower bound: {lower:.3f}")
    print(f"Upper bound: {upper:.3f}")
    print(f"Number of outliers: {len(outliers)}")

    print(
        outliers[["Date", "Ticker", column]]
        .sort_values(column)
        .head(10)
    )


# In[48]:


# Folder for Outliers analysis outputs

visuals_folder = "Stock_Financial_Analysis_Virtuals"
os.makedirs(visuals_folder, exist_ok=True)


# In[49]:


# Columns to check for outliers
outlier_columns = [
    "Daily_Return_Pct",
    "Volume",
    "Daily_Range"
]

all_outliers = []
outlier_summary = []

for column in outlier_columns:

    outliers, lower, upper = detect_outliers(
        analysis_df, column
    )


# In[50]:


print(f"\nOutlier analysis: {column}")
print(f"Lower bound: {lower:.3f}")
print(f"Upper bound: {upper:.3f}")
print(f"Number of outliers: {len(outliers)}")

print(
    outliers[["Date", "Ticker", column]]
    .sort_values(column)
    .head(10)
)


# In[51]:


# Store all detected outliers
if not outliers.empty:
        outlier_details = outliers[
            ["Date", "Ticker", column]
        ].copy()

        outlier_details["Variable"] = column
        outlier_details["Lower_Bound"] = lower
        outlier_details["Upper_Bound"] = upper

        outlier_details = outlier_details.rename(
            columns={column: "Observed_Value"}
        )

        all_outliers.append(outlier_details)


# In[52]:


# Store summary for each variable
outlier_summary.append({
        "Variable": column,
        "Lower_Bound": lower,
        "Upper_Bound": upper,
        "Number_of_Outliers": len(outliers)
    })


# In[53]:


# Combine and save all outlier records
if all_outliers:
    outlier_results = pd.concat(
        all_outliers, ignore_index=True
    )
else:
    outlier_results = pd.DataFrame(
        columns=[
            "Date", "Ticker", "Observed_Value",
            "Variable", "Lower_Bound", "Upper_Bound"
        ]
    )

outlier_results.to_csv(
    os.path.join(
        visuals_folder,
        "Outlier_Details.csv"
    ),
    index=False
)


# In[54]:


# Save the summary
outlier_summary_df = pd.DataFrame(outlier_summary)

outlier_summary_df.to_csv(
    os.path.join(
        visuals_folder,
        "Outlier_Summary.csv"
    ),
    index=False
)

print("\nOutlier results saved successfully.")
print("Folder:", os.path.abspath(visuals_folder))


# In[55]:


# Companies analysis

company_analysis = analysis_df.groupby("Ticker").agg(
    Average_Close=("Close", "mean"),
    Median_Close=("Close", "median"),
    Average_Daily_Return=("Daily_Return_Pct", "mean"),
    Return_Std_Dev=("Daily_Return_Pct", "std"),
    Average_Volume=("Volume", "mean"),
    Total_Volume=("Volume", "sum"),
    Average_Daily_Range=("Daily_Range", "mean")
).round(3)

print("PERFORMANCE BY COMPANY")
print(company_analysis)


# In[56]:


# Save the results to CSV
company_file = os.path.join(
    visuals_folder,
    "Company_Performance_Summary.csv"
)

company_analysis.to_csv(company_file, index=True)

print("\nCompany performance results saved to:")
print(os.path.abspath(company_file))


# In[57]:


# Monthly Analysis

monthly_analysis = analysis_df.copy()

monthly_analysis["Month"] = (
    monthly_analysis["Date"].dt.to_period("M")
)

monthly_summary = monthly_analysis.groupby(
    ["Month", "Ticker"]
).agg(
    Average_Close=("Close", "mean"),
    Average_Daily_Return=("Daily_Return_Pct", "mean"),
    Average_Volume=("Volume", "mean"),
    Trading_Days=("Date", "count")
).reset_index()

print("MONTHLY TRENDS")
print(monthly_summary.head(20).round(3))


# In[58]:


# Save the first 20 monthly trend records to CSV
monthly_file = os.path.join(
    visuals_folder,
    "Monthly_Trends_Summary.csv"
)

monthly_summary.head(20).round(3).to_csv(monthly_file, index=True)

# Confirm the saved file location
print("\nMonthly trends saved successfully to:")
print(os.path.abspath(monthly_file))


# In[59]:


#Trading Days analysis

daily_direction = analysis_df.dropna(
    subset=["Daily_Return_Pct"]
).groupby("Ticker").agg(
    Positive_Days=(
        "Daily_Return_Pct", lambda x: (x > 0).sum()
    ),
    Negative_Days=(
        "Daily_Return_Pct", lambda x: (x < 0).sum()
    ),
    Zero_Return_Days=(
        "Daily_Return_Pct", lambda x: (x == 0).sum()
    )
)

daily_direction["Positive_Day_Percentage"] = (
    daily_direction["Positive_Days"] /
    (
        daily_direction["Positive_Days"] +
        daily_direction["Negative_Days"] +
        daily_direction["Zero_Return_Days"]
    ) * 100
)

print("TRADING-DAY DIRECTION BY COMPANY")
print(daily_direction.round(2))


# In[60]:


# Save results to CSV
output_file = os.path.join(
    visuals_folder,
    "Trading_Day_Direction_By_Company.csv"
)

daily_direction.round(2).to_csv(output_file)

print("\nResults saved successfully to:")
print(os.path.abspath(output_file))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





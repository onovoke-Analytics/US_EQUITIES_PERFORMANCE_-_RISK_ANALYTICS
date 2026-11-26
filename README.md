# US_EQUITIES_PERFORMANCE_-_RISK_ANALYTICS
The project analyses the performance, trading patterns and short-term risk of five major US-listed companies: Apple, Amazon, Alphabet, JPMorgan Chase and Microsoft. It uses web-scraped data, cleaning and exploratory analysis, presented through interactive Power BI dashboards.

Introduction

Equity-market analysis requires more than observing share prices. Price levels show nominal valuation, while returns measure changes relative to a reference value; trading volume provides an indication of market activity and liquidity; and volatility measures the dispersion of price movements. This project brings these measures together to assess performance and risk across Apple (AAPL), Amazon (AMZN), Alphabet (GOOGL), JPMorgan Chase (JPM) and Microsoft (MSFT) - US-listed equities.

The objective was to convert historical market data obtained from Yahoo Finance into a cleaned, validated analytical dataset, conduct exploratory analysis and develop an interactive Power BI reporting suite for descriptive monitoring and stakeholder review.

Chart / Dashboard

The interactive dashboard combines equity performance analysis, trading activity, volatility assessment and variable relationships. It presents key performance indicators, including 1,255 trading records, approximately 11 billion shares traded, an average closing price of $320.05, average daily return of +0.05%, average intraday price range of $6.42 and average 20-day volatility of 1.40%.

The dashboard incorporates a closing-price distribution chart, highlighting a major concentration corridor around $300–$370; a donut chart showing the approximately 20% trading-volume share of each ticker; a cumulative price-growth line chart; and a volume-versus-daily-return scatter plot for examining price movements and trading activity. It also features a high-low spread column chart for comparing intraday price ranges, a 20-day rolling-volatility area chart for identifying periods of elevated risk, and a monthly average closing-price trend, which records a low of $289.92 in March and a high of $358.01 in August. A risk/performance summary and correlation-matrix tooltip further support the assessment of individual stock performance and relationships among key variables.

Interactive controls, including stock-ticker, date-range, trading-volume and volatility-tier slicers, enable users to filter and investigate selected equities and trading periods. Cross-filtering and report-page tooltips provide a connected analytical experience, allowing users to explore equity performance, market activity, price fluctuations and short-term investment risk within a single dashboard.

Story of the Data
The analysis follows the journey from raw historical trading records to decision-support visuals. Daily observations for five equities were collected from Yahoo Finance, cleaned and combined into one dataset. The resulting analysis explores how closing prices move, how trading volume is distributed, how daily returns behave and whether short-term volatility persists over time.

The overall picture is one of a slightly positive average daily return (+0.05%) alongside measurable downside asymmetry and periods of persistent elevated volatility. Trading-volume surges are associated with wider return dispersion and tend to coincide with price pullbacks in the reported analysis. The dashboards make these patterns easier to compare and investigate.


Methodology

1.	Data acquisition: Python Requests retrieved Yahoo Finance historical-data pages; BeautifulSoup parsed the HTML tables for the five selected ticker symbols.
2.	Data preparation: pandas was used to standardise column names, parse dates, remove currency symbols and thousands separators, convert price and volume fields to numeric types, and combine ticker-level records.
3.	Data cleaning and validation: Non-trading dividend/split event rows, invalid dates, missing closing prices and duplicate ticker-date records were removed. The report records zero null values in Date and Close and zero duplicate ticker-date records after cleaning.
4.	Derived Metrics Calculation: Key analytical measures were calculated, including daily price change, daily return percentage, daily trading range, range percentage and rolling 20-day volatility.
5.	Exploratory analysis and visualization: Descriptive statistics, return distributions, volume relationships, time-series trends and Pearson correlations were examined, then presented in Power BI using KPI cards, charts, a summary matrix and interactive slicers.

Data Breakdown

Dataset size: 1,255 daily trading records.
Assets covered: AAPL, AMZN, GOOGL, JPM and MSFT.
Core source fields: Date, Open, High, Low, Close, Adjusted Close and Volume.
Portfolio trading volume: Approximately 11.0 billion shares.
Average closing price: $320.05.
Average daily return: +0.05%.
Average intraday range: $6.42.
Average 20-day volatility: 1.40%.

The report describes four technology-focused mega-cap equities (AAPL, AMZN, GOOGL and MSFT) and one financial-sector equity (JPM), providing a cross-sector basis for descriptive comparison.

Pre-Analysis – What to be Explored

1.	How did closing prices vary across the selected equities and over the observation period?
2.	How was total trading volume distributed among the five tickers?
3.	What was the typical range of daily percentage returns, and were unusually large gains or losses present?
4.	Did high-volume sessions coincide with changes in returns or greater dispersion?
5.	How did 20-day rolling volatility change over time, and did elevated-risk periods persist?
6.	How strongly were price variables, volume, daily returns and volatility related?
7.	Whether percentage-based returns provide a more reliable basis for comparing the performance of equities with different share prices.
8.	Whether monthly closing-price movements reveal seasonal patterns and potential opportunities for portfolio rebalancing.
9.	How correlations among stock prices, trading volume, daily returns and volatility could influence portfolio diversification and risk assessment.

Potential Insights

1.	Percentage-based returns could provide a more reliable basis for comparing the performance of equities with different share prices.
2.	Trading-volume patterns could help identify periods of increased market activity and potential liquidity stress.
3.	Monitoring daily price movements could reveal unusual gains, losses and market fluctuations.
4.	 Rolling 20-day volatility analysis could help identify persistent periods of elevated investment risk.
5.	Correlation analysis could improve understanding of relationships among stock prices, trading volume and daily returns.
6.	Comparative stock-performance analysis could support better portfolio diversification and asset-allocation decisions.
7.	High trading-volume periods may reveal increased return dispersion and potential downside market pressure.
8.	Monthly price trends could reveal seasonal patterns and potential opportunities for portfolio rebalancing.
9.	Interactive Power BI dashboards could improve investment monitoring, risk assessment and data-driven decision-making.

In-Analysis Observations

1.	Return concentration: more than 85% of observations were reported within the -2.0% to +2.0% daily-return corridor when session volume was below 100 million shares.
2.	Downside asymmetry: the largest reported daily dollar gain was +$3.95, compared with a largest loss of -$4.66, indicating a more pronounced negative tail in the observed dollar movements.
3.	Volume and price: the report identifies a moderate negative relationship between volume and closing price (Pearson r ≈ -0.30). Volume surges above 100 million shares were associated with wider return dispersion, reaching approximately -4% to +4%.
4.	Volatility clustering: average 20-day volatility was about 1.40%; periods above 1.50% were reported to persist for approximately 15–30 trading days.
5.	Price-variable correlation: Open, High, Low and Close showed very strong positive inter-correlation (approximately r ≥ +0.98). Daily return percentage had only a weak relationship with closing price (approximately r = +0.10).
6.	Monthly pattern: average closing price rose from the reported March seasonal low of $289.92 to an August high of $358.01, a reported increase of approximately 23.5%.
7.	Cumulative movement: the report records a move from $110.15 at Day 15 to $121.32 at Day 18, described as a +10.15% three-day momentum swing.
8.	Trading-volume distribution: this was relatively balanced, with each of the five stocks (AAPL, AMZN, GOOGL, JPM and MSFT) accounting for approximately 20% of the total 11.0 billion shares traded.
9.	The average intraday price range: was approximately $6.42 across the five stocks, indicating a similar average daily high-to-low price spread in the reported analysis.

Interpretation: these findings describe the selected dataset and period. Correlation does not establish causation, and the dashboard should be used as a monitoring and analytical aid rather than a stand-alone portfolio-optimisation model.

Recommendations

1.	Volatility controls: use the 1.50% 20-day-volatility level as a review trigger for risk exposure and hedging; monitor elevated conditions over subsequent trading            sessions rather than reacting to a single observation.
2.	Liquidity-aware execution: review execution methods and potential slippage when daily volume exceeds 100 million shares, particularly where large price movements occur.
3.	Downside protection: assess risk controls that account for the larger observed maximum loss (-$4.66) relative to the maximum gain (+$3.95).
4.	Portfolio balance: monitor exposure across the four technology equities and JPM, and assess concentration and sector risk before rebalancing.
5.	Return-based comparison: use percentage returns and volatility, rather than nominal share prices alone, when comparing assets with different price levels.
6.	Data governance: maintain documented extraction dates, repeatable cleaning rules, ticker-date uniqueness checks and validation of missing values.
7.	Dashboard governance: use the Power BI report for periodic performance and risk reviews, with consistent date filters, clearly defined metrics and documented thresholds.
8.	Performance Monitoring: Establish regular monitoring of daily returns and closing-price movements to identify unusual market trends and support timely investment            decisions.
9.	Portfolio Diversification: Review asset allocation across technology and financial stocks to manage sector concentration and improve portfolio risk distribution.
10.	Analytical Reporting: Conduct periodic reviews of monthly stock performance, trading-volume trends and correlation patterns to strengthen investment planning and            management oversight.

References

1.	Yahoo Finance. Historical market data for Apple (AAPL), Amazon (AMZN), Alphabet (GOOGL), JPMorgan Chase (JPM) and Microsoft (MSFT). https://finance.yahoo.com/ 
2.	Project Report – Samson Ovokeraye Onoshaghware. US Equities Performance & Risk Analytics: Comprehensive Web Scraping, Data Cleaning, EDA & Power BI Dashboard Governance     Report. Data Analytics - 2026
3.	Python Requests documentation. https://requests.readthedocs.io/ 
4.	Beautiful Soup documentation. https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
5.	pandas documentation. https://pandas.pydata.org/docs/
6.	Microsoft Power BI documentation. https://learn.microsoft.com/power-bi/

Tools of Analysis: Python / Pandas and Microsoft Power BI














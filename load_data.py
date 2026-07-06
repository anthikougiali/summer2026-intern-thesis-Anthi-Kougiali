import yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pd.set_option("display.max_columns", None)

tickers = ["XBI", "IHI", "PPH", "IHF", "XLV", "^VIX"]

data = yf.download(tickers, start="2010-01-01", end="2025-07-01")

close = data["Close"]

close = close.dropna()

returns = close.pct_change()

returns = returns.dropna()

print(returns.head())

vix_level = close["^VIX"]

vix_median = vix_level.median()

regime = vix_level > vix_median

regime = regime.loc[returns.index]

average_by_regime = returns.groupby(regime).mean()

print(vix_median)
print(regime.head())
print(average_by_regime)

average_by_regime = average_by_regime.drop(columns=["^VIX"])

average_by_regime.T.plot(kind="bar")

plt.title("avg daily return: calm vs stressful days")
plt.ylabel("avg daily return")
plt.xlabel("etf")

plt.savefig("regime_chart.png")

event_dates = ["2022-08-16", "2023-08-29", "2024-08-15", "2025-01-17"]

event_dates = pd.to_datetime(event_dates)

pricing_window = pd.Series(False, index=returns.index)

for event in event_dates:
    start = event - pd.Timedelta(days=5)
    end = event + pd.Timedelta(days=20)
    pricing_window[(returns.index >= start) & (returns.index <= end)] = True

print(pricing_window.sum())

average_by_pricing = returns.groupby(pricing_window).mean()

print(average_by_pricing)

pricing_chart_data = average_by_pricing.drop(columns=["^VIX"])

pricing_chart_data.T.plot(kind="bar")

plt.title("avg daily return : normal vs drug-pricing news")
plt.ylabel("avg daily return")
plt.xlabel("etf")

plt.savefig("pricing_chart.png")

innovation_dates = ["2023-12-08", "2024-01-08", "2024-03-08", "2025-01-13"]

innovation_dates = pd.to_datetime(innovation_dates)

innovation_window = pd.Series(False, index=returns.index)

for event in innovation_dates:
    start = event - pd.Timedelta(days=5)
    end = event + pd.Timedelta(days=20)
    innovation_window[(returns.index >= start) & (returns.index <= end)] = True

print(innovation_window.sum())

average_by_innovation = returns.groupby(innovation_window).mean()

print(average_by_innovation)

innovation_chart_data = average_by_innovation.drop(columns=["^VIX"])

innovation_chart_data.T.plot(kind="bar")

plt.title("avg daily return: normal time vs innovation news")
plt.ylabel("avg daily return")
plt.xlabel("etf")

plt.savefig("innovation_chart.png")

print("--- PRICING WINDOWS ---")

xbi_in = returns["XBI"][pricing_window]
xbi_out = returns["XBI"][~pricing_window]
t_stat, p_value = stats.ttest_ind(xbi_in, xbi_out)
print("XBI p-value:", p_value)

ihi_in = returns["IHI"][pricing_window]
ihi_out = returns["IHI"][~pricing_window]
t_stat, p_value = stats.ttest_ind(ihi_in, ihi_out)
print("IHI p-value:", p_value)
import yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["XBI", "IHI", "PPH", "IHF", "XLV", "^VIX"]

data = yf.download(tickers, start="2010-01-01", end="2025-01-01")

close = data["Close"]

close = close.dropna()

returns = close.pct_change()

returns = returns.dropna()

print(returns.head())

vix_level = close["^VIX"]

vix_median = vix_level.median()

regime = vix_level > vix_median

print(vix_median)
print(regime.head())

regime = regime.loc[returns.index]

average_by_regime = returns.groupby(regime).mean()

print(average_by_regime)

average_by_regime = average_by_regime.drop(columns=["^VIX"])

average_by_regime.T.plot(kind="bar")

plt.title("avg daily return: calm vs stressful days")
plt.ylabel("avg daily return")
plt.xlabel("etf")

plt.savefig("regime_chart.png")
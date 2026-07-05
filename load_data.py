import yfinance as yf 
import pandas as pd

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
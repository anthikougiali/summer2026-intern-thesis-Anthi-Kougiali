import yfinance as yf 
import pandas as pd

data = yf.download("XBI", start="2010-01-01", end="2025-01-01")

print(data.head())

tickers = ["XBI", "IHI", "PPH", "IHF", "XLV", "^VIX"]

data = yf.download(tickers, start="2010-01-01", end="2025-01-01")

close = data["Close"]

print(close.head())
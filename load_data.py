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

pph_in = returns["PPH"][pricing_window]
pph_out = returns["PPH"][~pricing_window]
t_stat, p_value = stats.ttest_ind(pph_in, pph_out)
print("PPH p-value:", p_value)

ihf_in = returns["IHF"][pricing_window]
ihf_out = returns["IHF"][~pricing_window]
t_stat, p_value = stats.ttest_ind(ihf_in, ihf_out)
print("IHF p-value:", p_value)

xlv_in = returns["XLV"][pricing_window]
xlv_out = returns["XLV"][~pricing_window]
t_stat, p_value = stats.ttest_ind(xlv_in, xlv_out)
print("XLV p-value:", p_value)

print("--- INNOVATION WINDOWS ---")

xbi_in = returns["XBI"][innovation_window]
xbi_out = returns["XBI"][~innovation_window]
t_stat, p_value = stats.ttest_ind(xbi_in, xbi_out)
print("XBI p-value:", p_value)

ihi_in = returns["IHI"][innovation_window]
ihi_out = returns["IHI"][~innovation_window]
t_stat, p_value = stats.ttest_ind(ihi_in, ihi_out)
print("IHI p-value:", p_value)

pph_in = returns["PPH"][innovation_window]
pph_out = returns["PPH"][~innovation_window]
t_stat, p_value = stats.ttest_ind(pph_in, pph_out)
print("PPH p-value:", p_value)

ihf_in = returns["IHF"][innovation_window]
ihf_out = returns["IHF"][~innovation_window]
t_stat, p_value = stats.ttest_ind(ihf_in, ihf_out)
print("IHF p-value:", p_value)

xlv_in = returns["XLV"][innovation_window]
xlv_out = returns["XLV"][~innovation_window]
t_stat, p_value = stats.ttest_ind(xlv_in, xlv_out)
print("XLV p-value:", p_value)

# new approach 

innovation_basket = returns[["XBI", "IHI"]].mean(axis=1)

pricing_basket = returns[["PPH", "IHF"]].mean(axis=1)

wins = 0 
total = 0 

for event in innovation_dates: 
    start = event - pd.Timedelta(days=5)
    end = event + pd.Timedelta(days=20)

    window_mask = (returns.index>= start) & (returns.index <= end)

    innovation_return = innovation_basket[window_mask].mean()
    pricing_return = pricing_basket[window_mask].mean()

    total = total + 1 
    if innovation_return > pricing_return:
        wins = wins + 1 

    print(event.date(), "innovation:", round(innovation_return, 5), "pricing:", round(pricing_return, 5))

hit_rate = wins / total * 100

print("innovation beat pricing in", wins, "of", total, "events")
print("hit rate:", hit_rate)

#try individual companies instead of etfs

stocks = yf.download(["VRTX", "CRSP", "RXRX"], start="2010-01-01", end="2025-07-01")

stock_close = stocks["Close"]

stock_returns = stock_close.pct_change().dropna()

#casgevy: 2023-12-08

casgevy = pd.to_datetime("2023-12-08")
start = casgevy - pd.Timedelta(days=5)
end = casgevy +pd.Timedelta(days=20)

casgevy_window = (stock_returns.index >= start) & (stock_returns.index <= end)

crsp_in = stock_returns["CRSP"][casgevy_window]
crsp_out = stock_returns["CRSP"][~casgevy_window]

t_stat, p_value = stats.ttest_ind(crsp_in, crsp_out)

print("--- CRSP around Casgevy approval ---")
print("CRSP avg return in window:", crsp_in.mean())
print("CRSP avg return outside:", crsp_out.mean())
print("p-value:", p_value)

# check which subsectors survived the regulatory headwind

reform_start = pd.to_datetime("2022-08-16")

reform_returns = returns[returns.index >= reform_start]

reform_returns = reform_returns.drop(columns=["^VIX"])

print("reform era from", reform_returns.index[0].date(), "to", reform_returns.index[-1].date())
print("number of trading days:", len(reform_returns))

#test one stock

one_stock = yf.download("CRSP", start="2010-01-01", end="2025-07-01")

one_close = one_stock["Close"]

one_returns = one_close.pct_change().dropna()

print(one_returns.tail())

#test crsp around casgevvy approval 

crsp_event = pd.to_datetime("2023-12-08")

crsp_start = crsp_event - pd.Timedelta(days=5)

crsp_end = crsp_event + pd.Timedelta(days=20)

crsp_window = (one_returns.index >= crsp_start) & (one_returns.index <= crsp_end)

crsp_in = one_returns["CRSP"][crsp_window]

crsp_out = one_returns["CRSP"][~crsp_window]

print("CRSP in window average:", crsp_in.mean())
print("CRSP outside average:", crsp_out.mean())
print("Days in window:", crsp_window.sum())

#check if this is significant

t_stat, p_value = stats.ttest_ind(crsp_in, crsp_out)

print("CRSP p-value:", p_value)

#test more events

stock_events = {
    "CRSP": "2023-12-08",   # Casgevy approval (innovation)
    "SRPT": "2023-06-22",   # Elevidys approval - failed endpoint (innovation)
    "MRK":  "2024-08-15",   # Januvia on IRA negotiated-price list (pricing)
    "BMY":  "2024-08-15",   # Eliquis on IRA list (pricing)
    "ABBV": "2024-08-15",   # Imbruvica on IRA list (pricing)
    "AMGN": "2024-08-15",   # Enbrel on IRA list (pricing)
}

all_stocks = yf.download(list(stock_events.keys()), start="2015-01-01", end="2025-07-01")

all_stock_close = all_stocks["Close"]

all_stock_returns = all_stock_close.pct_change().dropna()

print("SINGLE-STOCK EVENT TESTS")

for ticker in stock_events:
    event = pd.to_datetime(stock_events[ticker])
    start = event - pd.Timedelta(days=5)
    end = event + pd.Timedelta(days=20)

    stock_data = all_stock_returns[ticker].dropna()

    window = (all_stock_returns.index >= start) & (all_stock_returns.index <= end)

    in_window = all_stock_returns[ticker][window]
    out_window = all_stock_returns[ticker][~window]

    t_stat, p_value = stats.ttest_ind(in_window, out_window)

    print(ticker, "| in:", round(in_window.mean(), 4), "| out:", round(out_window.mean(), 4), "| p-value:", round(p_value, 4))

    #new method - which subsectors survive regulations 

    reform_start = pd.to_datetime("2022-08-16")

    reform_returns = returns[returns.index >= reform_start]

    reform_returns = reform_returns.drop(columns=["^VIX"])

    print("reform era")
    print("from", reform_returns.index[0].date(), "to", reform_returns.index[-1].date())
    print("Trading days:", len(reform_returns))

#rank sub-sectors

total_return = (1 + reform_returns).prod() - 1 

sharpe = reform_returns.mean() / reform_returns.std() * (252 ** 0.5)

cumulative = (1 + reform_returns).cumprod()
running_max = cumulative.cummax()
drawdown = (cumulative - running_max) / running_max
max_drawdown = drawdown.min()

print("total return since reform")
print((total_return * 100).round(1).sort_values(ascending=False))

print("sharpe")
print(sharpe.round(2).sort_values(ascending=False))

print("max drawdown")
print((max_drawdown * 100).round(1).sort_values(ascending=False))

#chart this 

plt.figure()

sharpe_sorted = sharpe.sort_values(ascending=False)

sharpe_sorted.plot(kind="bar", color="teal")

plt.title("Which Sub-Sectors Survived the Regulatory Headwind (2022+)")
plt.ylabel("Sharpe Ratio (risk-adjusted return)")
plt.xlabel("Sub-Sector ETF")
plt.axhline(0, color="black", linewidth=0.8)

plt.savefig("survival_chart.png", bbox_inches="tight")

#where alpha lives

recent_start = returns.index[-1] - pd.Timedelta(days=365)

recent_returns = returns[returns.index >= recent_start]

recent_returns = recent_returns.drop(columns=["^VIX"])

recent_total = (1 + recent_returns).prod() - 1

print("recent 12 months returns")
print((recent_total * 100).round(1).sort_values(ascending=False))

#combine the two 

alpha_table = pd.DataFrame({
    "Survival_Sharpe": sharpe, 
    "Recent_Return": recent_total * 100
})

alpha_table = alpha_table.round(2)

print("survival vs alpha")
print(alpha_table.sort_values("Recent_Return", ascending=False))

#where alpha lives

plt.figure()

plt.scatter(alpha_table["Survival_Sharpe"], alpha_table["Recent_Return_%"], color="teal", s=80)

for ticker in alpha_table.index:
    plt.annotate(ticker,
                 (alpha_table.loc[ticker, "Survival_Sharpe"], alpha_table.loc[ticker, "Recent_Return_%"]),
                 xytext=(5, 5), textcoords="offset points")

plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(0, color="black", linewidth=0.8)

plt.title("Where Healthcare Alpha Lives: Survival vs Momentum")
plt.xlabel("Survived Reform Era (Sharpe)  →  better")
plt.ylabel("Recent 12-Month Return %  →  better")

plt.savefig("alpha_chart.png", bbox_inches="tight")
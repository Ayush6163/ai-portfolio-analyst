import streamlit as st  # type: ignore
import yfinance as yf  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # ✅ this one must be here
from datetime import date, timedelta
from yahooquery import search  # type: ignore

# -------------------------------
# Title
# -------------------------------
st.title("AI Portfolio Analyst, By: A. Aryan")

# -------------------------------
# Search by Company Name
# -------------------------------
if "tickers_text" not in st.session_state:
    st.session_state["tickers_text"] = "AAPL,MSFT,GOOGL"

st.subheader("Search by company name (optional)")
names = st.text_input("Type company names (comma-separated)", "", placeholder="Tesla, Amazon, Nvidia")

def names_to_tickers(names_csv: str):
    tickers = []
    for raw in [n.strip() for n in names_csv.split(",") if n.strip()]:
        try:
            res = search(raw)
            quotes = res.get("quotes", [])
            # Pick the first reasonable equity/ETF symbol
            best = None
            for q in quotes:
                if q.get("symbol") and q.get("quoteType") in ("EQUITY", "ETF"):
                    best = q
                    break
            if best:
                tickers.append(best["symbol"])
        except Exception:
            pass
    return tickers

if st.button("Find Tickers from Names"):
    found = names_to_tickers(names)
    if found:
        st.session_state["tickers_text"] = ",".join(found)
        st.success(f"Found: {', '.join(found)} — filled into the tickers box below.")
    else:
        st.warning("No tickers found. Try different names or type symbols directly.")

# -------------------------------
# Enter tickers directly
# -------------------------------
st.subheader("Or enter tickers directly")
tickers = st.text_input("Tickers (comma-separated)", key="tickers_text").upper().replace(" ", "")
start = st.date_input("Start date", date.today() - timedelta(days=365*3))
end = st.date_input("End date", date.today())

# -------------------------------
# Fetch Data
# -------------------------------
if st.button("Fetch Data"):
    tickers_list = [t for t in tickers.split(",") if t]
    if not tickers_list:
        st.error("Please provide at least one ticker.")
    else:
        raw = yf.download(tickers_list, start=start, end=end, auto_adjust=True)
        st.write(f"Showing data for {', '.join(tickers_list)}")

        # Handle single vs multiple tickers
        if isinstance(raw.columns, pd.MultiIndex):
            close = raw["Close"].copy()
        else:
            close = raw[["Close"]].copy()
            close.columns = tickers_list  # name the single column to match input

        st.subheader("Raw Close Prices (head)")
        st.dataframe(close.head())

        # --- Charts
        st.subheader("Price Chart (Close)")
        st.line_chart(close)

        # Daily returns
        rets = close.pct_change().dropna()
        st.subheader("Daily Returns")
        st.line_chart(rets)

        # Cumulative returns (growth of 1)
        cum = (1 + rets).cumprod()
        st.subheader("Cumulative Returns (Growth of 1)")
        st.line_chart(cum)

        # -------------------------------
        # Portfolio Weights & Risk
        # -------------------------------
        st.subheader("Portfolio Weights & Risk")

        weights_in = st.text_input(
            "Weights (comma-separated, blank = equal weights)",
            value="",
            help="Example for 3 tickers: 0.4,0.3,0.3. If blank, uses equal weights.",
        )

        # parse weights
        if weights_in.strip():
            try:
                w = np.array([float(x) for x in weights_in.split(",")], dtype=float)
                if len(w) != len(tickers_list):
                    st.error(f"Number of weights ({len(w)}) must equal number of tickers ({len(tickers_list)}).")
                    st.stop()
                if (w <= 0).all():
                    st.warning("All weights are non-positive; normalizing anyway.")
                w = w / w.sum()
            except Exception as e:
                st.error(f"Could not parse weights: {e}")
                st.stop()
        else:
            if len(tickers_list) == 0:
                st.error("No tickers found. Please enter at least one.")
                st.stop()
            w = np.repeat(1 / len(tickers_list), len(tickers_list))

        # compute portfolio daily returns
        rets = close.pct_change().dropna()
        port_ret = rets @ w

        # choose a benchmark (default S&P 500). For India, try ^NSEI
        benchmark = st.text_input("Benchmark symbol", value="^GSPC", help="Examples: ^GSPC (S&P 500), ^NSEI (Nifty 50)")
        bench_df = yf.download([benchmark], start=start, end=end, auto_adjust=True, progress=False)
        if isinstance(bench_df.columns, pd.MultiIndex):
            bench_close = bench_df["Close"].iloc[:, 0]
        else:
            bench_close = bench_df["Close"]
        bench_ret = bench_close.pct_change().dropna().reindex(port_ret.index).fillna(0)

        # helpers
        def annualize(r: pd.Series):
            mu = r.mean() * 252
            vol = r.std() * np.sqrt(252)
            sharpe = (mu / vol) if vol > 0 else np.nan
            return mu, vol, sharpe

        mu, vol, sharpe = annualize(port_ret)
        bmu, bvol, bsh = annualize(bench_ret)

        # equity curves
        equity = (1 + port_ret).cumprod()
        bench_eq = (1 + bench_ret).cumprod()

        # max drawdown
        mdd = ((equity / equity.cummax()) - 1).min()

        # beta to benchmark
        beta = float(np.cov(port_ret, bench_ret)[0, 1] / (bench_ret.var() + 1e-12))

        # VaR / CVaR at 95%
        alpha = 0.95
        sorted_r = np.sort(port_ret.values)
        idx = max(1, int((1 - alpha) * len(sorted_r)))
        VaR = -sorted_r[idx]
        CVaR = -sorted_r[:idx].mean()

        # rolling volatility (21 trading days ≈ 1 month)
        roll_vol = port_ret.rolling(21).std() * np.sqrt(252)

        # correlation table (between assets)
        corr_tbl = rets.corr()

        # ---- show results ----
        st.markdown("### Key Metrics")
        metrics = pd.DataFrame({
            "Metric": ["Ann. Return","Ann. Vol","Sharpe","Beta","Max Drawdown","VaR (95%)","CVaR (95%)"],
            "Portfolio": [
                f"{mu:.2%}", f"{vol:.2%}", f"{sharpe:.2f}", f"{beta:.2f}",
                f"{mdd:.2%}", f"{VaR:.2%}", f"{CVaR:.2%}"
            ],
            "Benchmark": [f"{bmu:.2%}", f"{bvol:.2%}", f"{bsh:.2f}", "-", "-", "-", "-"]
        })
        st.dataframe(metrics, use_container_width=True)

        st.markdown("### Rolling Volatility (annualized)")
        st.line_chart(roll_vol)

        st.markdown("### Correlation Between Assets")
        st.dataframe(corr_tbl.style.format("{:.2f}"), use_container_width=True)

        # download daily portfolio returns
        st.download_button(
            "Download portfolio daily returns (CSV)",
            pd.DataFrame({"date": port_ret.index, "portfolio_return": port_ret.values}).to_csv(index=False).encode(),
            file_name="portfolio_returns.csv",
            mime="text/csv"
        )
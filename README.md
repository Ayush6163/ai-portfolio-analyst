# 📊 AI Portfolio Analyst

**Live Demo:** [Click here](https://ayush6163-ai-portfolio-analyst.streamlit.app)  
**Source Code:** [GitHub Repo](https://github.com/Ayush6163/ai-portfolio-analyst)

---

## 📌 Overview
AI Portfolio Analyst is a **Streamlit web application** for analyzing stock portfolios in real-time.  
It uses live data from Yahoo Finance and provides risk metrics, charts, and downloadable reports.

---

## 🚀 Features
- Search by company name (e.g., "Tesla", "Amazon") or enter stock tickers directly  
- Portfolio analytics: Return, Volatility, Sharpe Ratio, Beta, Max Drawdown, VaR, CVaR  
- Charts: Price trends, daily & cumulative returns, rolling volatility, correlation matrix  
- Risk contribution by asset (table + bar chart)  
- Auto-generated analyst notes  
- Download portfolio returns (CSV) and full analysis report (HTML)  

---

## ⚙️ Tech Stack
- **Framework:** Streamlit  
- **Data:** Yahoo Finance (`yfinance`, `yahooquery`)  
- **Libraries:** pandas, numpy, scipy, plotly  

---

## 🔧 Run Locally
```bash
git clone https://github.com/Ayush6163/ai-portfolio-analyst.git
cd ai-portfolio-analyst

python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

python -m streamlit run app.py

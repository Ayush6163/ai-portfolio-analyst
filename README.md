# 📊 AI Portfolio Analyst

**Live Demo:** 👉 [Streamlit App](https://ayush6163-ai-portfolio-analyst.streamlit.app)  
**Source Code:** 👉 [GitHub Repo](https://github.com/Ayush6163/ai-portfolio-analyst)

---

## 📌 Overview
The **AI Portfolio Analyst** is an interactive **Streamlit web application** that performs **real-time portfolio risk and performance analysis** using live market data.  
It combines **computational finance methods, econometrics, and data visualization** to help investors, students, and researchers analyze stock portfolios.

---

## 🚀 Features

✅ **Live Data Fetching** — Fetch historical stock prices from Yahoo Finance  
✅ **Search by Name or Ticker** — Type “Tesla” or “Amazon” and auto-convert to stock symbols  
✅ **Portfolio Analytics**  
- Annualized Return & Volatility  
- Sharpe Ratio & Beta  
- Max Drawdown (risk of loss)  
- Value-at-Risk (VaR) & Conditional VaR (CVaR)  

✅ **Visualizations**  
- Price trends & cumulative returns  
- Daily returns chart  
- Rolling volatility (21-day window)  
- Correlation heatmap between assets  

✅ **Risk Contribution**  
- Calculates each asset’s contribution to total portfolio risk  
- Shows in table + bar chart  

✅ **Analyst Narrative**  
- Auto-generated risk commentary (like an investment analyst)  

✅ **Export Options**  
- Download portfolio returns as CSV  
- Download full analysis report as HTML  

---

## 🖼️ Screenshots

### Dashboard
![Dashboard Screenshot](https://raw.githubusercontent.com/Ayush6163/ai-portfolio-analyst/main/screenshots/dashboard.png)

### Risk Contribution
![Risk Contribution Screenshot](https://raw.githubusercontent.com/Ayush6163/ai-portfolio-analyst/main/screenshots/risk_contribution.png)

*(You can take real screenshots from your deployed app and add them in a `/screenshots` folder inside your repo.)*

---

## ⚙️ Tech Stack
- **Frontend/Backend:** Streamlit  
- **Data Sources:** Yahoo Finance (`yfinance`, `yahooquery`)  
- **Libraries:** pandas, numpy, scipy, plotly  
- **Deployment:** Streamlit Community Cloud  

---

## 📂 Project Structure

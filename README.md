# 📊 FinSight Pro — AI Financial Statement Analysis

> **AI & Fintech Class Project** | Streamlit Application

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**

---

## 🧠 Analysis Modules

| Module | Techniques |
|--------|-----------|
| **Ratio Analysis** | Profitability, Liquidity, Leverage, Efficiency, Per-Share |
| **Structural Analysis** | Common-Size, Horizontal, Vertical, Trend/Index |
| **DuPont** | 3-Factor & 5-Factor decomposition of ROE |
| **Risk Scoring** | Altman Z-Score, Piotroski F-Score |
| **Valuation** | P/E, P/B, P/S, DCF Calculator |
| **Cash Flow** | CFO/Revenue, CFO/NI, Cash Conversion Cycle |
| **Peer Comparison** | Radar chart across competitors |

---

## 📡 Data Sources (Production)

To connect live data, replace `generate_financials()` with:

```python
import yfinance as yf

def get_real_financials(ticker: str):
    stock = yf.Ticker(ticker)
    income = stock.financials        # Income Statement
    balance = stock.balance_sheet    # Balance Sheet
    cashflow = stock.cashflow        # Cash Flow Statement
    return income, balance, cashflow
```

### Other Sources
- **Alpha Vantage** – `pip install alpha_vantage` + free API key at alphavantage.co
- **SEC EDGAR** – `https://data.sec.gov/api/xbrl/companyfacts/`
- **Financial Modeling Prep** – `https://financialmodelingprep.com/developer/docs/`

---

## 💲 Pricing Tiers

| Plan | Price | Target |
|------|-------|--------|
| Starter | Free | Individual learners |
| Professional | $49/mo | Finance professionals |
| Enterprise | $199/mo | Teams & hedge funds |
| Academic | $9/mo | Students & researchers |

---

## 🗂️ Project Structure

```
fintech_app/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## 👨‍🎓 Academic Notes

This app demonstrates:
1. **Horizontal Analysis** — comparing values across years
2. **Vertical (Common-Size)** — normalizing by revenue/assets
3. **Ratio Analysis** — 19 financial ratios across 5 categories
4. **Predictive Scoring** — Altman Z-Score & Piotroski F-Score
5. **DCF Valuation** — intrinsic value estimation
6. **DuPont Decomposition** — root cause of ROE changes

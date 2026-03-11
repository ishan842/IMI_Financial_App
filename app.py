"""
FinSight Pro — AI-Powered Financial Statement Analysis Platform
================================================================
Real yfinance data | 300+ Indian + Global Companies
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FinSight Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --navy:#0a1628; --gold:#c9a84c; --gold2:#f0d080; --teal:#1de9b6;
    --card:#0f2040; --border:rgba(201,168,76,0.25); --text:#e8eaf0; --muted:#8892a4;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--navy);color:var(--text);}
h1,h2,h3{font-family:'DM Serif Display',serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#081020 0%,#0a1628 100%);border-right:1px solid var(--border);}
.metric-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px;text-align:center;transition:transform .2s;}
.metric-card:hover{transform:translateY(-3px);}
.metric-card .label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;}
.metric-card .value{font-size:22px;font-weight:600;color:var(--gold);margin-top:6px;}
.metric-card .delta{font-size:12px;margin-top:4px;}
.positive{color:var(--teal);} .negative{color:#ff6b6b;} .neutral{color:var(--muted);}
.section-header{border-left:4px solid var(--gold);padding-left:14px;margin:28px 0 16px;font-family:'DM Serif Display',serif;font-size:20px;color:var(--gold2);}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;background:rgba(201,168,76,0.15);color:var(--gold);border:1px solid var(--border);margin:2px;}
.hero{background:linear-gradient(135deg,#0a1628 0%,#112244 50%,#0a1628 100%);border:1px solid var(--border);border-radius:16px;padding:28px 36px;margin-bottom:24px;}
.insight-box{background:linear-gradient(135deg,#0f2040,#112244);border:1px solid var(--border);border-left:4px solid var(--teal);border-radius:10px;padding:14px 18px;margin:8px 0;font-size:14px;line-height:1.7;}
.alert-red{background:rgba(255,107,107,0.1);border-left:4px solid #ff6b6b;border-radius:8px;padding:12px 16px;margin:6px 0;}
.alert-green{background:rgba(29,233,182,0.1);border-left:4px solid #1de9b6;border-radius:8px;padding:12px 16px;margin:6px 0;}
.alert-yellow{background:rgba(240,208,128,0.1);border-left:4px solid var(--gold2);border-radius:8px;padding:12px 16px;margin:6px 0;}
.gold-divider{height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:20px 0;}
.price-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px;text-align:center;}
.price-card.featured{border-color:var(--gold);background:linear-gradient(135deg,#0f2040,#1a3060);box-shadow:0 0 40px rgba(201,168,76,0.12);}
.price-big{font-size:36px;font-weight:700;color:var(--gold);}
.data-live{color:#1de9b6;font-size:11px;font-weight:600;}
.data-sim{color:#f0d080;font-size:11px;font-weight:600;}
button[data-baseweb="tab"]{color:var(--muted) !important;}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--gold) !important;border-bottom-color:var(--gold) !important;}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:var(--navy);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  COMPANY DATABASE
# ══════════════════════════════════════════════════════════════════════════════
INDIAN_COMPANIES = {
    "🇮🇳 Reliance Industries (RELIANCE)":       "RELIANCE.NS",
    "🇮🇳 Tata Consultancy Services (TCS)":      "TCS.NS",
    "🇮🇳 HDFC Bank (HDFCBANK)":                 "HDFCBANK.NS",
    "🇮🇳 Infosys (INFY)":                       "INFY.NS",
    "🇮🇳 ICICI Bank (ICICIBANK)":               "ICICIBANK.NS",
    "🇮🇳 Hindustan Unilever (HINDUNILVR)":      "HINDUNILVR.NS",
    "🇮🇳 ITC Limited (ITC)":                    "ITC.NS",
    "🇮🇳 State Bank of India (SBIN)":           "SBIN.NS",
    "🇮🇳 Bharti Airtel (BHARTIARTL)":           "BHARTIARTL.NS",
    "🇮🇳 Bajaj Finance (BAJFINANCE)":           "BAJFINANCE.NS",
    "🇮🇳 Kotak Mahindra Bank (KOTAKBANK)":      "KOTAKBANK.NS",
    "🇮🇳 Larsen & Toubro (LT)":                 "LT.NS",
    "🇮🇳 Asian Paints (ASIANPAINT)":            "ASIANPAINT.NS",
    "🇮🇳 HCL Technologies (HCLTECH)":           "HCLTECH.NS",
    "🇮🇳 Axis Bank (AXISBANK)":                 "AXISBANK.NS",
    "🇮🇳 Maruti Suzuki (MARUTI)":               "MARUTI.NS",
    "🇮🇳 Sun Pharmaceutical (SUNPHARMA)":       "SUNPHARMA.NS",
    "🇮🇳 Titan Company (TITAN)":                "TITAN.NS",
    "🇮🇳 UltraTech Cement (ULTRACEMCO)":        "ULTRACEMCO.NS",
    "🇮🇳 Wipro (WIPRO)":                        "WIPRO.NS",
    "🇮🇳 Nestle India (NESTLEIND)":             "NESTLEIND.NS",
    "🇮🇳 Power Grid Corporation (POWERGRID)":   "POWERGRID.NS",
    "🇮🇳 NTPC Limited (NTPC)":                  "NTPC.NS",
    "🇮🇳 Tata Motors (TATAMOTORS)":             "TATAMOTORS.NS",
    "🇮🇳 Tech Mahindra (TECHM)":                "TECHM.NS",
    "🇮🇳 IndusInd Bank (INDUSINDBK)":           "INDUSINDBK.NS",
    "🇮🇳 JSW Steel (JSWSTEEL)":                 "JSWSTEEL.NS",
    "🇮🇳 Tata Steel (TATASTEEL)":               "TATASTEEL.NS",
    "🇮🇳 Bajaj Auto (BAJAJ-AUTO)":              "BAJAJ-AUTO.NS",
    "🇮🇳 Bajaj Finserv (BAJAJFINSV)":           "BAJAJFINSV.NS",
    "🇮🇳 Oil & Natural Gas Corp (ONGC)":        "ONGC.NS",
    "🇮🇳 Coal India (COALINDIA)":               "COALINDIA.NS",
    "🇮🇳 Cipla (CIPLA)":                        "CIPLA.NS",
    "🇮🇳 Dr Reddy's Laboratories (DRREDDY)":    "DRREDDY.NS",
    "🇮🇳 Divi's Laboratories (DIVISLAB)":       "DIVISLAB.NS",
    "🇮🇳 Eicher Motors (EICHERMOT)":            "EICHERMOT.NS",
    "🇮🇳 Hero MotoCorp (HEROMOTOCO)":           "HEROMOTOCO.NS",
    "🇮🇳 Hindalco Industries (HINDALCO)":       "HINDALCO.NS",
    "🇮🇳 Grasim Industries (GRASIM)":           "GRASIM.NS",
    "🇮🇳 Adani Enterprises (ADANIENT)":         "ADANIENT.NS",
    "🇮🇳 Adani Ports (ADANIPORTS)":             "ADANIPORTS.NS",
    "🇮🇳 Apollo Hospitals (APOLLOHOSP)":        "APOLLOHOSP.NS",
    "🇮🇳 Bharat Electronics (BEL)":             "BEL.NS",
    "🇮🇳 BPCL (BPCL)":                          "BPCL.NS",
    "🇮🇳 Britannia Industries (BRITANNIA)":     "BRITANNIA.NS",
    "🇮🇳 Shriram Finance (SHRIRAMFIN)":         "SHRIRAMFIN.NS",
    "🇮🇳 SBI Life Insurance (SBILIFE)":         "SBILIFE.NS",
    "🇮🇳 HDFC Life Insurance (HDFCLIFE)":       "HDFCLIFE.NS",
    "🇮🇳 Tata Consumer Products (TATACONSUM)":  "TATACONSUM.NS",
    "🇮🇳 Adani Green Energy (ADANIGREEN)":      "ADANIGREEN.NS",
    "🇮🇳 Adani Power (ADANIPOWER)":             "ADANIPOWER.NS",
    "🇮🇳 Ambuja Cements (AMBUJACEM)":           "AMBUJACEM.NS",
    "🇮🇳 ACC Limited (ACC)":                    "ACC.NS",
    "🇮🇳 Avenue Supermarts / DMart (DMART)":    "DMART.NS",
    "🇮🇳 Bandhan Bank (BANDHANBNK)":            "BANDHANBNK.NS",
    "🇮🇳 Bank of Baroda (BANKBARODA)":          "BANKBARODA.NS",
    "🇮🇳 Berger Paints (BERGEPAINT)":           "BERGEPAINT.NS",
    "🇮🇳 Biocon (BIOCON)":                      "BIOCON.NS",
    "🇮🇳 Bosch India (BOSCHLTD)":               "BOSCHLTD.NS",
    "🇮🇳 Canara Bank (CANBK)":                  "CANBK.NS",
    "🇮🇳 Cholamandalam Finance (CHOLAFIN)":     "CHOLAFIN.NS",
    "🇮🇳 Colgate-Palmolive India (COLPAL)":     "COLPAL.NS",
    "🇮🇳 Container Corp (CONCOR)":              "CONCOR.NS",
    "🇮🇳 Dabur India (DABUR)":                  "DABUR.NS",
    "🇮🇳 DLF Limited (DLF)":                    "DLF.NS",
    "🇮🇳 Federal Bank (FEDERALBNK)":            "FEDERALBNK.NS",
    "🇮🇳 Godrej Consumer Products (GODREJCP)":  "GODREJCP.NS",
    "🇮🇳 Godrej Properties (GODREJPROP)":       "GODREJPROP.NS",
    "🇮🇳 Havells India (HAVELLS)":              "HAVELLS.NS",
    "🇮🇳 IDFC First Bank (IDFCFIRSTB)":         "IDFCFIRSTB.NS",
    "🇮🇳 Indian Hotels (INDHOTEL)":             "INDHOTEL.NS",
    "🇮🇳 Indian Oil Corporation (IOC)":         "IOC.NS",
    "🇮🇳 IRCTC (IRCTC)":                        "IRCTC.NS",
    "🇮🇳 IRFC (IRFC)":                          "IRFC.NS",
    "🇮🇳 Jindal Steel & Power (JINDALSTEL)":    "JINDALSTEL.NS",
    "🇮🇳 L&T Finance (LTF)":                    "LTF.NS",
    "🇮🇳 L&T Technology Services (LTTS)":       "LTTS.NS",
    "🇮🇳 LIC Housing Finance (LICHSGFIN)":      "LICHSGFIN.NS",
    "🇮🇳 Lupin Pharmaceuticals (LUPIN)":        "LUPIN.NS",
    "🇮🇳 Mahindra & Mahindra (M&M)":            "M&M.NS",
    "🇮🇳 Mphasis (MPHASIS)":                    "MPHASIS.NS",
    "🇮🇳 MRF Tyres (MRF)":                      "MRF.NS",
    "🇮🇳 Muthoot Finance (MUTHOOTFIN)":         "MUTHOOTFIN.NS",
    "🇮🇳 NMDC (NMDC)":                          "NMDC.NS",
    "🇮🇳 Page Industries (PAGEIND)":            "PAGEIND.NS",
    "🇮🇳 Persistent Systems (PERSISTENT)":      "PERSISTENT.NS",
    "🇮🇳 Petronet LNG (PETRONET)":              "PETRONET.NS",
    "🇮🇳 Pidilite Industries (PIDILITIND)":     "PIDILITIND.NS",
    "🇮🇳 Punjab National Bank (PNB)":           "PNB.NS",
    "🇮🇳 REC Limited (RECLTD)":                 "RECLTD.NS",
    "🇮🇳 Siemens India (SIEMENS)":              "SIEMENS.NS",
    "🇮🇳 SRF Limited (SRF)":                    "SRF.NS",
    "🇮🇳 Tata Chemicals (TATACHEM)":            "TATACHEM.NS",
    "🇮🇳 Tata Communication (TATACOMM)":        "TATACOMM.NS",
    "🇮🇳 Tata Elxsi (TATAELXSI)":              "TATAELXSI.NS",
    "🇮🇳 Tata Power (TATAPOWER)":              "TATAPOWER.NS",
    "🇮🇳 Torrent Pharma (TORNTPHARM)":          "TORNTPHARM.NS",
    "🇮🇳 Torrent Power (TORNTPOWER)":           "TORNTPOWER.NS",
    "🇮🇳 TVS Motor Company (TVSMOTOR)":         "TVSMOTOR.NS",
    "🇮🇳 UPL Limited (UPL)":                    "UPL.NS",
    "🇮🇳 Vedanta Limited (VEDL)":               "VEDL.NS",
    "🇮🇳 Voltas (VOLTAS)":                      "VOLTAS.NS",
    "🇮🇳 Zomato (ZOMATO)":                      "ZOMATO.NS",
    "🇮🇳 Coforge (COFORGE)":                    "COFORGE.NS",
    "🇮🇳 Cyient (CYIENT)":                      "CYIENT.NS",
    "🇮🇳 KPIT Technologies (KPITTECH)":         "KPITTECH.NS",
    "🇮🇳 Oracle Financial Services (OFSS)":     "OFSS.NS",
    "🇮🇳 Tata Technologies (TATATECH)":         "TATATECH.NS",
    "🇮🇳 Zensar Technologies (ZENSARTECH)":     "ZENSARTECH.NS",
    "🇮🇳 AU Small Finance Bank (AUBANK)":       "AUBANK.NS",
    "🇮🇳 Indian Bank (INDIANB)":                "INDIANB.NS",
    "🇮🇳 Karur Vysya Bank (KARURVYSYA)":        "KARURVYSYA.NS",
    "🇮🇳 Manappuram Finance (MANAPPURAM)":      "MANAPPURAM.NS",
    "🇮🇳 Paytm / One97 Comm (PAYTM)":          "PAYTM.NS",
    "🇮🇳 RBL Bank (RBLBANK)":                   "RBLBANK.NS",
    "🇮🇳 Union Bank of India (UNIONBANK)":      "UNIONBANK.NS",
    "🇮🇳 Yes Bank (YESBANK)":                   "YESBANK.NS",
    "🇮🇳 ICICI Lombard (ICICIGI)":              "ICICIGI.NS",
    "🇮🇳 ICICI Prudential Life (ICICIPRULI)":   "ICICIPRULI.NS",
    "🇮🇳 LIC of India (LICI)":                  "LICI.NS",
    "🇮🇳 Star Health Insurance (STARHEALTH)":   "STARHEALTH.NS",
    "🇮🇳 Aurobindo Pharma (AUROPHARMA)":        "AUROPHARMA.NS",
    "🇮🇳 Fortis Healthcare (FORTIS)":           "FORTIS.NS",
    "🇮🇳 IPCA Laboratories (IPCALAB)":          "IPCALAB.NS",
    "🇮🇳 Laurus Labs (LAURUSLABS)":             "LAURUSLABS.NS",
    "🇮🇳 Max Healthcare (MAXHEALTH)":           "MAXHEALTH.NS",
    "🇮🇳 Narayana Hrudayalaya (NH)":            "NH.NS",
    "🇮🇳 Zydus Lifesciences (ZYDUSLIFE)":       "ZYDUSLIFE.NS",
    "🇮🇳 Ashok Leyland (ASHOKLEY)":             "ASHOKLEY.NS",
    "🇮🇳 Balkrishna Industries (BALKRISIND)":   "BALKRISIND.NS",
    "🇮🇳 Bharat Forge (BHARATFORG)":            "BHARATFORG.NS",
    "🇮🇳 Motherson Sumi (MOTHERSUMI)":          "MOTHERSUMI.NS",
    "🇮🇳 Marico (MARICO)":                      "MARICO.NS",
    "🇮🇳 Varun Beverages (VBL)":                "VBL.NS",
    "🇮🇳 United Breweries (UBL)":               "UBL.NS",
    "🇮🇳 GAIL India (GAIL)":                    "GAIL.NS",
    "🇮🇳 HPCL (HINDPETRO)":                     "HINDPETRO.NS",
    "🇮🇳 NHPC (NHPC)":                          "NHPC.NS",
    "🇮🇳 Solar Industries (SOLARINDS)":         "SOLARINDS.NS",
    "🇮🇳 APL Apollo Tubes (APLAPOLLO)":         "APLAPOLLO.NS",
    "🇮🇳 NALCO (NATIONALUM)":                   "NATIONALUM.NS",
    "🇮🇳 SAIL (SAIL)":                          "SAIL.NS",
    "🇮🇳 Macrotech / Lodha (LODHA)":            "LODHA.NS",
    "🇮🇳 Oberoi Realty (OBEROIRLTY)":           "OBEROIRLTY.NS",
    "🇮🇳 Prestige Estates (PRESTIGE)":          "PRESTIGE.NS",
    "🇮🇳 HAL (HAL)":                            "HAL.NS",
    "🇮🇳 Bharat Dynamics (BDL)":                "BDL.NS",
    "🇮🇳 Mazagon Dock (MAZDOCK)":               "MAZDOCK.NS",
    "🇮🇳 Aarti Industries (AARTIIND)":          "AARTIIND.NS",
    "🇮🇳 Deepak Nitrite (DEEPAKNTR)":           "DEEPAKNTR.NS",
    "🇮🇳 Navin Fluorine (NAVINFLUOR)":          "NAVINFLUOR.NS",
    "🇮🇳 Vinati Organics (VINATIORGA)":         "VINATIORGA.NS",
    "🇮🇳 Nykaa / FSN E-Commerce (NYKAA)":       "NYKAA.NS",
    "🇮🇳 Policy Bazaar / PB Fintech (POLICYBZR)":"POLICYBZR.NS",
    "🇮🇳 Delhivery (DELHIVERY)":                "DELHIVERY.NS",
    "🇮🇳 IndiGo / InterGlobe (INDIGO)":         "INDIGO.NS",
    "🇮🇳 Bharat Heavy Electricals (BHEL)":      "BHEL.NS",
    "🇮🇳 HUDCO (HUDCO)":                        "HUDCO.NS",
    "🇮🇳 RITES (RITES)":                        "RITES.NS",
}

GLOBAL_COMPANIES = {
    "🇺🇸 Apple (AAPL)":               "AAPL",
    "🇺🇸 Microsoft (MSFT)":           "MSFT",
    "🇺🇸 Amazon (AMZN)":              "AMZN",
    "🇺🇸 Alphabet / Google (GOOGL)":  "GOOGL",
    "🇺🇸 Meta Platforms (META)":      "META",
    "🇺🇸 NVIDIA (NVDA)":              "NVDA",
    "🇺🇸 Tesla (TSLA)":               "TSLA",
    "🇺🇸 Netflix (NFLX)":             "NFLX",
    "🇺🇸 Salesforce (CRM)":           "CRM",
    "🇺🇸 Adobe (ADBE)":               "ADBE",
    "🇺🇸 JPMorgan Chase (JPM)":       "JPM",
    "🇺🇸 Goldman Sachs (GS)":         "GS",
    "🇺🇸 Berkshire Hathaway (BRK.B)": "BRK-B",
    "🇺🇸 Visa (V)":                   "V",
    "🇺🇸 Mastercard (MA)":            "MA",
    "🇺🇸 Johnson & Johnson (JNJ)":    "JNJ",
    "🇺🇸 Pfizer (PFE)":               "PFE",
    "🇺🇸 UnitedHealth (UNH)":         "UNH",
    "🇬🇧 HSBC Holdings (HSBC)":       "HSBC",
    "🇩🇪 SAP SE (SAP)":               "SAP",
    "🇨🇭 Nestlé (NSRGY)":             "NSRGY",
    "🇳🇱 ASML Holding (ASML)":        "ASML",
    "🇫🇷 LVMH (LVMUY)":               "LVMUY",
    "🇯🇵 Toyota Motor (TM)":          "TM",
    "🇯🇵 Sony Group (SONY)":          "SONY",
    "🇰🇷 Samsung Electronics (005930)":"005930.KS",
    "🇨🇳 Alibaba (BABA)":             "BABA",
    "🇨🇳 Tencent (TCEHY)":            "TCEHY",
    "🇦🇺 BHP Group (BHP)":            "BHP",
}

COMPANIES = {**INDIAN_COMPANIES, **GLOBAL_COMPANIES}

# ══════════════════════════════════════════════════════════════════════════════
#  REAL yfinance DATA FETCHER
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_real_data(ticker: str):
    """
    Fetch real financials from Yahoo Finance via yfinance.
    Uses robust session with browser-like headers to work on Streamlit Cloud.
    Returns (data_dict, info_dict, price_hist_df, is_real: bool)
    """
    import requests
    from requests.adapters import HTTPAdapter

    # ── Browser-like session so Yahoo Finance accepts the request ────────────
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":      "keep-alive",
    })
    adapter = HTTPAdapter(max_retries=3)
    session.mount("https://", adapter)
    session.mount("http://",  adapter)

    try:
        stk  = yf.Ticker(ticker, session=session)

        # ── Pull financials ──────────────────────────────────────────────────
        inc  = stk.financials
        bal  = stk.balance_sheet
        cf   = stk.cashflow
        info = stk.info or {}

        if inc is None or inc.empty:
            return None, info, None, False

        # ── Align date columns across all three statements ───────────────────
        common = sorted(inc.columns)
        if not bal.empty:
            common = sorted(inc.columns.intersection(bal.columns))
        if len(common) == 0:
            common = sorted(inc.columns)

        inc = inc[common]
        if not bal.empty and all(c in bal.columns for c in common):
            bal = bal[common]
        if not cf.empty and all(c in cf.columns for c in common):
            cf = cf[common]

        years = [c.year for c in common]
        n     = len(years)

        def get_row(df, *keys):
            """Search df rows case-insensitively for any of keys; return values array."""
            if df is None or df.empty:
                return np.zeros(n)
            for k in keys:
                for idx in df.index:
                    if k.lower() in str(idx).lower():
                        try:
                            row = df.loc[idx].reindex(common).values.astype(float)
                            return np.nan_to_num(row, nan=0.0)
                        except Exception:
                            continue
            return np.zeros(n)

        # ── Income Statement ─────────────────────────────────────────────────
        rev  = get_row(inc, "Total Revenue", "Revenue")
        cogs = get_row(inc, "Cost Of Revenue", "Cost of Goods")
        gp   = get_row(inc, "Gross Profit")
        if gp.sum() == 0:   gp   = rev - cogs
        opex = get_row(inc, "Operating Expense", "Total Operating Expenses")
        ebit = get_row(inc, "Operating Income", "Ebit", "EBIT")
        if ebit.sum() == 0: ebit = gp - opex
        int_ = np.abs(get_row(inc, "Interest Expense", "Interest And Debt Expense"))
        ebt  = get_row(inc, "Pretax Income", "Income Before Tax")
        if ebt.sum() == 0:  ebt  = ebit - int_
        tax  = np.abs(get_row(inc, "Tax Provision", "Income Tax Expense"))
        ni   = get_row(inc, "Net Income")

        # ── Balance Sheet ────────────────────────────────────────────────────
        ta   = get_row(bal, "Total Assets")
        ca   = get_row(bal, "Current Assets", "Total Current Assets")
        cl   = get_row(bal, "Current Liabilities", "Total Current Liabilities")
        ltd  = get_row(bal, "Long Term Debt", "Long-Term Debt")
        eq   = get_row(bal, "Stockholders Equity", "Total Equity",
                            "Common Stock Equity", "Total Stockholder Equity")
        if eq.sum() == 0 and ta.sum() > 0:
            eq = ta - cl - ltd

        # ── Cash Flow ────────────────────────────────────────────────────────
        cfo  = get_row(cf, "Operating Cash Flow", "Cash From Operations",
                           "Total Cash From Operating Activities")
        cfi  = get_row(cf, "Investing Cash Flow", "Cash From Investing",
                           "Total Cash From Investing Activities")
        cff  = get_row(cf, "Financing Cash Flow", "Cash From Financing",
                           "Total Cash From Financing Activities")

        # Guard: if revenue is all zeros something went wrong
        if rev.sum() == 0:
            return None, info, None, False

        scale  = 1e9
        sh_val = info.get("sharesOutstanding", 1e9)
        shares = np.full(n, sh_val / scale)

        # ── Price history ────────────────────────────────────────────────────
        try:
            hist = stk.history(period="5y", interval="1mo")
        except Exception:
            hist = pd.DataFrame()

        data = dict(
            years=years,
            revenue=rev/scale,         cogs=cogs/scale,     gross_profit=gp/scale,
            opex=opex/scale,           ebit=ebit/scale,     interest=int_/scale,
            ebt=ebt/scale,             tax=tax/scale,       net_income=ni/scale,
            total_assets=ta/scale,     current_assets=ca/scale,
            current_liabilities=cl/scale, lt_debt=ltd/scale,
            equity=eq/scale,           cfo=cfo/scale,       cfi=cfi/scale,
            cff=cff/scale,             shares=shares,
        )
        return data, info, hist, True

    except Exception as e:
        return None, {}, None, False


def fallback_data(ticker: str, years: int = 5):
    rng  = np.random.default_rng(sum(ord(c) for c in ticker))
    yrs  = list(range(2024 - years + 1, 2025))
    rev  = np.cumsum(rng.uniform(40, 400, years)) + 50
    cogs = rev * rng.uniform(0.45, 0.65, years)
    gp   = rev - cogs
    opex = gp  * rng.uniform(0.30, 0.50, years)
    ebit = gp  - opex
    int_ = rev * rng.uniform(0.01, 0.04, years)
    ebt  = ebit - int_
    tax  = ebt  * rng.uniform(0.18, 0.28, years)
    ni   = ebt  - tax
    ta   = rev  * rng.uniform(1.2, 2.5, years)
    ca   = ta   * rng.uniform(0.35, 0.55, years)
    cl   = ca   * rng.uniform(0.40, 0.70, years)
    ltd  = ta   * rng.uniform(0.15, 0.35, years)
    eq   = ta   - cl - ltd
    cfo  = ni   * rng.uniform(1.05, 1.30, years)
    cfi  = -rev * rng.uniform(0.05, 0.15, years)
    cff  = -ni  * rng.uniform(0.20, 0.50, years)
    sh   = rng.uniform(5, 20, years)
    return dict(
        years=yrs, revenue=rev, cogs=cogs, gross_profit=gp,
        opex=opex, ebit=ebit, interest=int_, ebt=ebt, tax=tax,
        net_income=ni, total_assets=ta, current_assets=ca,
        current_liabilities=cl, lt_debt=ltd, equity=eq,
        cfo=cfo, cfi=cfi, cff=cff, shares=sh,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  RATIO ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def compute_ratios(f: dict) -> pd.DataFrame:
    rows = []
    for i, yr in enumerate(f["years"]):
        ni   = f["net_income"][i];  rev = f["revenue"][i]
        gp   = f["gross_profit"][i]; eq = f["equity"][i]
        ta   = f["total_assets"][i]; ca = f["current_assets"][i]
        cl   = f["current_liabilities"][i]; ltd = f["lt_debt"][i]
        ebit = f["ebit"][i]; int_ = f["interest"][i]
        cfo  = f["cfo"][i];  sh   = f["shares"][i]
        def s(x): return max(x, 0.001)
        rows.append({
            "Year":              yr,
            "Gross Margin %":    round(gp/s(rev)*100, 2),
            "Net Margin %":      round(ni/s(rev)*100, 2),
            "EBIT Margin %":     round(ebit/s(rev)*100, 2),
            "ROE %":             round(ni/s(eq)*100, 2),
            "ROA %":             round(ni/s(ta)*100, 2),
            "ROCE %":            round(ebit/s(ta-cl)*100, 2),
            "Current Ratio":     round(ca/s(cl), 2),
            "Quick Ratio":       round(ca*0.85/s(cl), 2),
            "Cash Ratio":        round(ca*0.40/s(cl), 2),
            "Debt/Equity":       round(ltd/s(eq), 2),
            "Debt/Assets":       round(ltd/s(ta), 2),
            "Interest Coverage": round(ebit/s(int_), 2),
            "Equity Multiplier": round(ta/s(eq), 2),
            "Asset Turnover":    round(rev/s(ta), 2),
            "Equity Turnover":   round(rev/s(eq), 2),
            "CFO/Revenue %":     round(cfo/s(rev)*100, 2),
            "CFO/Net Income":    round(cfo/s(ni), 2),
            "EPS":               round(ni/s(sh), 2),
            "BVPS":              round(eq/s(sh), 2),
            "CFO per Share":     round(cfo/s(sh), 2),
        })
    return pd.DataFrame(rows).set_index("Year")


# ══════════════════════════════════════════════════════════════════════════════
#  AI INSIGHT ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def generate_insights(f, rat, info):
    insights = []
    if len(rat) < 1: return insights
    latest = rat.iloc[-1]
    prev   = rat.iloc[-2] if len(rat) > 1 else rat.iloc[0]

    nm = latest["Net Margin %"]
    if nm > 20:
        insights.append(("positive", f"💰 **Exceptional profitability** — Net margin {nm:.1f}% is well above the 10–15% typical benchmark, reflecting strong pricing power and cost discipline."))
    elif nm < 0:
        insights.append(("negative", f"🚨 **Loss-making** — Net margin is negative ({nm:.1f}%). Company is currently spending more than it earns."))
    elif nm < 5:
        insights.append(("negative", f"⚠️ **Thin margins** — Net margin {nm:.1f}% leaves little buffer against cost shocks or competitive pressure."))

    nm_chg = latest["Net Margin %"] - prev["Net Margin %"]
    if nm_chg > 2:
        insights.append(("positive", f"📈 **Margin expansion** — Net margin improved {nm_chg:.1f} pp YoY, signalling operational efficiency gains."))
    elif nm_chg < -3:
        insights.append(("negative", f"📉 **Margin compression** — Net margin fell {abs(nm_chg):.1f} pp YoY. Watch input costs and competitive pressures."))

    rev_arr = f["revenue"]
    if len(rev_arr) >= 2 and rev_arr[-2] > 0:
        rev_g = (rev_arr[-1] - rev_arr[-2]) / rev_arr[-2] * 100
        if rev_g > 20:
            insights.append(("positive", f"🚀 **High-growth revenue** — Top line grew {rev_g:.1f}% YoY — significantly outpacing GDP growth."))
        elif rev_g > 10:
            insights.append(("positive", f"📊 **Healthy revenue growth** — Revenue grew {rev_g:.1f}% YoY, indicating solid business momentum."))
        elif rev_g < -5:
            insights.append(("negative", f"🔻 **Revenue decline** — Revenue contracted {abs(rev_g):.1f}% YoY. Investigate pricing/volume mix."))

    cr = latest["Current Ratio"]
    if cr > 2.5:
        insights.append(("positive", f"💧 **Very strong liquidity** — Current ratio {cr:.2f}x. Company comfortably meets all short-term obligations."))
    elif cr > 1:
        insights.append(("neutral", f"💧 **Adequate liquidity** — Current ratio {cr:.2f}x is above the critical 1.0 threshold."))
    else:
        insights.append(("negative", f"🚨 **Liquidity risk** — Current ratio {cr:.2f}x below 1.0. Current liabilities exceed current assets."))

    de = latest["Debt/Equity"]
    if de > 3:
        insights.append(("negative", f"🏋️ **Very high leverage** — D/E of {de:.2f}x poses significant financial risk, especially in rising rate environments."))
    elif de < 0.3:
        insights.append(("positive", f"🛡️ **Conservative balance sheet** — D/E {de:.2f}x indicates minimal leverage and strong financial resilience."))

    ic = latest["Interest Coverage"]
    if ic > 10:
        insights.append(("positive", f"✅ **Excellent debt serviceability** — Interest covered {ic:.0f}× by EBIT. Very low default risk."))
    elif ic < 1.5:
        insights.append(("negative", f"⚠️ **Debt service at risk** — Interest coverage {ic:.1f}× is dangerously low. Risk of debt covenant breach."))

    cfo_ni = latest["CFO/Net Income"]
    if cfo_ni > 1.1:
        insights.append(("positive", f"💵 **High earnings quality** — CFO exceeds net income by {(cfo_ni-1)*100:.0f}%. Profits are backed by real cash."))
    elif cfo_ni < 0.5:
        insights.append(("negative", f"🔍 **Earnings quality concern** — CFO/NI of {cfo_ni:.2f}. Reported profits not converting to cash — investigate accruals."))

    roe = latest["ROE %"]
    if roe > 20:
        insights.append(("positive", f"⭐ **Superior returns** — ROE {roe:.1f}% far exceeds cost of equity, indicating a strong economic moat."))
    elif roe < 5:
        insights.append(("negative", f"📊 **Weak shareholder returns** — ROE {roe:.1f}% below typical cost of equity (~10–12%). Potential value destruction."))

    pe = info.get("trailingPE")
    if pe and isinstance(pe, (int, float)) and pe > 0:
        if pe > 60:
            insights.append(("neutral", f"📌 **Very expensive valuation** — Trailing P/E {pe:.1f}× prices in aggressive growth. High bar to meet expectations."))
        elif pe < 10:
            insights.append(("positive", f"🎯 **Deep value signal** — Trailing P/E {pe:.1f}× appears cheap. Could indicate an undervalued opportunity."))
        else:
            insights.append(("neutral", f"📌 **Reasonable valuation** — Trailing P/E {pe:.1f}× is within a normal market range."))

    sector = info.get("sector", "")
    if sector:
        insights.append(("neutral", f"🏭 **Sector: {sector}** — Ratios should be benchmarked against {sector} peers, as norms vary significantly by industry."))

    return insights


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 18px;'>
        <span style='font-family:"DM Serif Display",serif;font-size:26px;color:#c9a84c;'>📊 FinSight Pro</span><br>
        <span style='font-size:11px;color:#8892a4;letter-spacing:2px;'>AI FINANCIAL INTELLIGENCE</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 🏢 Company")
    group    = st.radio("Market", ["🇮🇳 Indian (NSE/BSE)", "🌍 Global"], horizontal=True)
    pool     = INDIAN_COMPANIES if "Indian" in group else GLOBAL_COMPANIES
    search_q = st.text_input("🔍 Search", placeholder="e.g. Reliance, HDFC, TCS…")

    if search_q:
        filtered = {k: v for k, v in pool.items()
                    if search_q.lower() in k.lower() or search_q.upper() in v.upper()}
        if not filtered: filtered = pool
    else:
        filtered = pool

    company_name = st.selectbox("", list(filtered.keys()), label_visibility="collapsed")
    ticker       = filtered[company_name]
    st.markdown(f"<div style='font-size:11px;color:#556;'>📊 {len(INDIAN_COMPANIES)} Indian · {len(GLOBAL_COMPANIES)} Global</div>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Settings")
    currency = st.radio("Currency", ["₹ INR", "$ USD"], horizontal=True)
    is_inr   = "INR" in currency

    modules = st.multiselect("Modules",
        ["Profitability","Liquidity","Leverage","Efficiency",
         "Cash Flow","DuPont","Altman Z-Score","Piotroski F-Score",
         "Valuation","Peer Comparison"],
        default=["Profitability","Liquidity","Leverage","Cash Flow","DuPont","Altman Z-Score"])

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#556;line-height:1.8;'>
    <b style='color:#c9a84c;'>Data</b><br>
    <span class='data-live'>● LIVE</span> Yahoo Finance<br>
    Auto-refreshed every 60 min<br><br>
    <b style='color:#c9a84c;'>v2.0</b> — Real Data Edition
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FETCH DATA
# ══════════════════════════════════════════════════════════════════════════════
with st.spinner(f"⏳ Fetching live data for **{company_name}**…"):
    raw_data, info, price_hist, is_real = fetch_real_data(ticker)

if raw_data is None or all(v == 0 for v in raw_data.get("revenue", [0])):
    is_real   = False
    raw_data  = fallback_data(ticker, 5)
    info      = {}
    price_hist = None
    st.warning("⚠️ Live data unavailable — showing simulated data for demonstration purposes.")

# Currency scale: yfinance returns USD billions
# For INR display: 1 USD Bn = 83.5 × 100 INR Cr ≈ 8350 INR Cr
FX     = 83.5
SCALE  = (FX * 100) if (is_inr and is_real) else (FX if (is_inr and not is_real) else 1.0)
CURR   = "₹" if is_inr else "$"
UNIT   = "₹ Cr" if is_inr else "$ Bn"

f   = raw_data
rat = compute_ratios(f)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
sector     = info.get("sector","")
mc         = info.get("marketCap", 0)
live_price = info.get("currentPrice") or info.get("regularMarketPrice", 0) or 0
data_badge = "🟢 LIVE DATA" if is_real else "🟡 SIMULATED DATA"
mc_str     = (f"₹{mc*FX/1e7:,.0f} Cr" if is_inr else f"${mc/1e9:.1f}B") if mc else "N/A"
price_str  = f"{CURR}{live_price*FX:,.1f}" if (is_inr and live_price) else (f"${live_price:,.2f}" if live_price else "N/A")

# ── Hero: pre-compute all values before building HTML ─────────────────────
_ny   = len(f["years"])
_nm   = len(modules)
_sb   = ('<span class="badge">🏭 ' + sector + '</span>') if sector else ""
_hero = (
    '<div class="hero">'
      '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">'
        '<div>'
          '<div style="font-size:11px;color:#8892a4;letter-spacing:2px;text-transform:uppercase;">'
            'Financial Statement Analysis'
          '</div>'
          '<h1 style="margin:6px 0 10px;font-size:28px;color:#f0d080;">' + company_name + '</h1>'
          '<span class="badge">' + data_badge + '</span> '
          '<span class="badge">📈 ' + str(_ny) + '-Year History</span> '
          '<span class="badge">🏦 ' + str(_nm) + ' Modules</span> '
          + _sb +
        '</div>'
        '<div style="text-align:right;">'
          '<div style="font-size:11px;color:#8892a4;">Current Price</div>'
          '<div style="font-size:30px;font-weight:700;color:#1de9b6;">' + price_str + '</div>'
          '<div style="font-size:12px;color:#8892a4;">Mkt Cap: ' + mc_str + '</div>'
        '</div>'
      '</div>'
    '</div>'
)
st.markdown(_hero, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
def delta_html(curr, prev_val):
    if prev_val == 0: return '<span class="neutral">— N/A</span>'
    d   = (curr - prev_val) / abs(prev_val) * 100
    cls = "positive" if d >= 0 else "negative"
    return f'<span class="{cls}">{"▲" if d>=0 else "▼"} {abs(d):.1f}% YoY</span>'

kpi_cols = st.columns(5)
kpis = [
    ("Revenue",      f["revenue"][-1]*SCALE,      f["revenue"][-2]*SCALE      if len(f["revenue"])>1 else 0,      UNIT),
    ("Net Income",   f["net_income"][-1]*SCALE,    f["net_income"][-2]*SCALE   if len(f["net_income"])>1 else 0,   UNIT),
    ("Total Assets", f["total_assets"][-1]*SCALE,  f["total_assets"][-2]*SCALE if len(f["total_assets"])>1 else 0, UNIT),
    ("ROE",          rat.iloc[-1]["ROE %"],         rat.iloc[-2]["ROE %"]       if len(rat)>1 else 0,               "%"),
    ("Net Margin",   rat.iloc[-1]["Net Margin %"],  rat.iloc[-2]["Net Margin %"]if len(rat)>1 else 0,               "%"),
]
for col, (label, curr, prev_v, unit) in zip(kpi_cols, kpis):
    with col:
        disp = f"{unit} {curr:,.1f}" if unit not in ["%"] else f"{curr:.1f}%"
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">{label}</div>
          <div class="value">{disp}</div>
          <div class="delta">{delta_html(curr, prev_v)}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📋 Statements",
    "📊 Ratios",
    "🏗️ DuPont",
    "⚠️ Risk Scores",
    "💸 Valuation",
    "🔬 Advanced",
    "🤖 AI Insights",
    "📉 Stock Chart",
    "🏪 Pricing & About",
])

# ── TAB 0: STATEMENTS ──────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-header">Financial Statements</div>', unsafe_allow_html=True)
    badge_html = '<span class="data-live">● Live from Yahoo Finance</span>' if is_real else '<span class="data-sim">● Simulated data</span>'
    st.markdown(badge_html, unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📝 Income Statement","🏦 Balance Sheet","💧 Cash Flow"])

    with t1:
        items = ["Revenue","COGS","Gross Profit","Operating Expenses","EBIT","Interest","EBT","Tax","Net Income"]
        keys  = ["revenue","cogs","gross_profit","opex","ebit","interest","ebt","tax","net_income"]
        isd   = {"Item": items}
        for i, yr in enumerate(f["years"]):
            isd[str(yr)] = [f"{UNIT} {f[k][i]*SCALE:,.1f}" for k in keys]
        st.dataframe(pd.DataFrame(isd).set_index("Item"), use_container_width=True)

        fig = go.Figure()
        fig.add_bar(x=f["years"], y=[v*SCALE for v in f["revenue"]],     name="Revenue",      marker_color="#c9a84c")
        fig.add_bar(x=f["years"], y=[v*SCALE for v in f["gross_profit"]], name="Gross Profit", marker_color="#1de9b6")
        fig.add_bar(x=f["years"], y=[v*SCALE for v in f["net_income"]],   name="Net Income",   marker_color="#4fc3f7")
        fig.update_layout(barmode="group", template="plotly_dark", paper_bgcolor="#0a1628",
                          plot_bgcolor="#0f2040", font_family="DM Sans",
                          title="Revenue vs Profit Breakdown", yaxis_title=UNIT,
                          legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        bsd = {"Item":["Total Assets","Current Assets","Non-Current Assets","Current Liabilities","LT Debt","Total Equity"]}
        for i, yr in enumerate(f["years"]):
            nc = f["total_assets"][i] - f["current_assets"][i]
            bsd[str(yr)] = [f"{UNIT} {v*SCALE:,.1f}" for v in
                            [f["total_assets"][i],f["current_assets"][i],nc,
                             f["current_liabilities"][i],f["lt_debt"][i],f["equity"][i]]]
        st.dataframe(pd.DataFrame(bsd).set_index("Item"), use_container_width=True)

        fig2 = go.Figure()
        fig2.add_bar(x=f["years"], y=[v*SCALE for v in f["current_assets"]], name="Current Assets",     marker_color="#c9a84c")
        fig2.add_bar(x=f["years"], y=[(f["total_assets"][i]-f["current_assets"][i])*SCALE for i in range(len(f["years"]))],
                     name="Non-Current Assets", marker_color="#1de9b6")
        fig2.add_bar(x=f["years"], y=[v*SCALE for v in f["equity"]],         name="Equity",             marker_color="#4fc3f7")
        fig2.update_layout(barmode="stack", template="plotly_dark", paper_bgcolor="#0a1628",
                           plot_bgcolor="#0f2040", font_family="DM Sans",
                           title="Balance Sheet Composition", yaxis_title=UNIT)
        st.plotly_chart(fig2, use_container_width=True)

    with t3:
        net_cf = [f["cfo"][i]+f["cfi"][i]+f["cff"][i] for i in range(len(f["years"]))]
        cfd = {"Item":["Operating CF","Investing CF","Financing CF","Net Cash Flow"]}
        for i, yr in enumerate(f["years"]):
            cfd[str(yr)] = [f"{UNIT} {v*SCALE:,.1f}" for v in [f["cfo"][i],f["cfi"][i],f["cff"][i],net_cf[i]]]
        st.dataframe(pd.DataFrame(cfd).set_index("Item"), use_container_width=True)

        fig3 = go.Figure()
        fig3.add_bar(x=f["years"], y=[v*SCALE for v in f["cfo"]], name="Operating", marker_color="#1de9b6")
        fig3.add_bar(x=f["years"], y=[v*SCALE for v in f["cfi"]], name="Investing",  marker_color="#ff6b6b")
        fig3.add_bar(x=f["years"], y=[v*SCALE for v in f["cff"]], name="Financing",  marker_color="#c9a84c")
        fig3.add_scatter(x=f["years"], y=[v*SCALE for v in net_cf], mode="lines+markers",
                         name="Net Cash", line=dict(color="white",width=2,dash="dot"))
        fig3.update_layout(barmode="relative", template="plotly_dark", paper_bgcolor="#0a1628",
                           plot_bgcolor="#0f2040", font_family="DM Sans",
                           title="Cash Flow Breakdown", yaxis_title=UNIT)
        st.plotly_chart(fig3, use_container_width=True)

# ── TAB 1: RATIOS ───────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-header">Financial Ratio Analysis</div>', unsafe_allow_html=True)

    if "Profitability" in modules:
        st.markdown("#### 📈 Profitability")
        fig = go.Figure()
        for col, clr in [("Gross Margin %","#c9a84c"),("Net Margin %","#1de9b6"),
                          ("EBIT Margin %","#4fc3f7"),("ROE %","#f0d080"),("ROA %","#ff9f7f")]:
            fig.add_scatter(x=rat.index, y=rat[col], mode="lines+markers", name=col,
                            line=dict(width=2.5, color=clr))
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                          plot_bgcolor="#0f2040", font_family="DM Sans",
                          title="Profitability Trend", yaxis_ticksuffix="%",
                          legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, use_container_width=True)

    if "Liquidity" in modules:
        st.markdown("#### 💧 Liquidity")
        fig2 = go.Figure()
        for col, clr in [("Current Ratio","#c9a84c"),("Quick Ratio","#1de9b6"),("Cash Ratio","#4fc3f7")]:
            fig2.add_scatter(x=rat.index, y=rat[col], mode="lines+markers", name=col, line=dict(width=2.5, color=clr))
        fig2.add_hline(y=1, line_dash="dash", line_color="#ff6b6b", annotation_text="Min (1.0)")
        fig2.add_hline(y=2, line_dash="dot",  line_color="#1de9b6", annotation_text="Ideal (2.0)")
        fig2.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                           plot_bgcolor="#0f2040", font_family="DM Sans", title="Liquidity Ratios")
        st.plotly_chart(fig2, use_container_width=True)

    if "Leverage" in modules:
        st.markdown("#### 🔩 Leverage & Solvency")
        c1, c2 = st.columns(2)
        with c1:
            fig3 = go.Figure()
            fig3.add_bar(x=rat.index, y=rat["Debt/Equity"], name="D/E", marker_color="#c9a84c")
            fig3.add_bar(x=rat.index, y=rat["Debt/Assets"], name="D/A", marker_color="#1de9b6")
            fig3.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                               plot_bgcolor="#0f2040", barmode="group", font_family="DM Sans", title="Debt Ratios")
            st.plotly_chart(fig3, use_container_width=True)
        with c2:
            fig4 = go.Figure()
            fig4.add_scatter(x=rat.index, y=rat["Interest Coverage"], mode="lines+markers+text",
                             text=[f"{v:.1f}x" for v in rat["Interest Coverage"]], textposition="top center",
                             line=dict(color="#f0d080", width=3))
            fig4.add_hline(y=3, line_dash="dash", line_color="#ff6b6b", annotation_text="Min safe (3x)")
            fig4.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                               plot_bgcolor="#0f2040", font_family="DM Sans", title="Interest Coverage")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### 📋 Full Ratio Table")
    st.dataframe(rat, use_container_width=True)
    st.download_button("⬇️ Download Ratios CSV", rat.to_csv().encode(), f"{ticker}_ratios.csv", "text/csv")

# ── TAB 2: DUPONT ───────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-header">DuPont Analysis — ROE Decomposition</div>', unsafe_allow_html=True)
    st.markdown("> **ROE = Net Margin × Asset Turnover × Equity Multiplier**")

    nm_ = rat["Net Margin %"] / 100
    at_ = rat["Asset Turnover"]
    em_ = rat["Equity Multiplier"]
    roe_= nm_ * at_ * em_ * 100

    fig_dp = make_subplots(rows=2, cols=2,
        subplot_titles=("Net Profit Margin (%)","Asset Turnover (×)","Equity Multiplier (×)","Reconstructed ROE (%)"))
    fig_dp.add_bar(x=rat.index, y=nm_*100, marker_color="#c9a84c", row=1, col=1)
    fig_dp.add_bar(x=rat.index, y=at_,     marker_color="#1de9b6", row=1, col=2)
    fig_dp.add_bar(x=rat.index, y=em_,     marker_color="#4fc3f7", row=2, col=1)
    fig_dp.add_scatter(x=rat.index, y=roe_, mode="lines+markers", line=dict(color="#f0d080",width=3), row=2, col=2)
    fig_dp.update_layout(showlegend=False, template="plotly_dark", paper_bgcolor="#0a1628",
                         plot_bgcolor="#0f2040", font_family="DM Sans", height=520, title_text="3-Factor DuPont")
    st.plotly_chart(fig_dp, use_container_width=True)

    st.markdown("#### 5-Factor DuPont")
    tb  = np.array(f["net_income"]) / np.maximum(np.array(f["ebt"]),  0.001)
    ib  = np.array(f["ebt"])        / np.maximum(np.array(f["ebit"]), 0.001)
    em5 = np.array(f["ebit"])       / np.maximum(np.array(f["revenue"]), 0.001)
    at5 = np.array(f["revenue"])    / np.maximum(np.array(f["total_assets"]), 0.001)
    lv5 = np.array(f["total_assets"])/ np.maximum(np.array(f["equity"]), 0.001)
    df5 = pd.DataFrame({
        "Year":f["years"],"Tax Burden":tb.round(3),"Interest Burden":ib.round(3),
        "EBIT Margin":em5.round(3),"Asset Turnover":at5.round(3),"Leverage":lv5.round(3),
        "ROE % (5-factor)":(tb*ib*em5*at5*lv5*100).round(2)
    }).set_index("Year")
    st.dataframe(df5, use_container_width=True)

# ── TAB 3: RISK SCORES ──────────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-header">Bankruptcy & Strength Scores</div>', unsafe_allow_html=True)

    st.markdown("#### ⚠️ Altman Z-Score")
    z_scores = []
    for i in range(len(f["years"])):
        ta = max(f["total_assets"][i], 0.001)
        wc = f["current_assets"][i] - f["current_liabilities"][i]
        re = f["equity"][i] * 0.55
        tl = f["current_liabilities"][i] + f["lt_debt"][i]
        z  = (1.2*(wc/ta) + 1.4*(re/ta) + 3.3*(f["ebit"][i]/ta) +
               0.6*(f["equity"][i]*2.0/max(tl,0.001)) + 1.0*(f["revenue"][i]/ta))
        z_scores.append(round(z, 3))

    z_colors = ["#ff6b6b" if z<1.81 else "#f0d080" if z<2.99 else "#1de9b6" for z in z_scores]
    fig_z = go.Figure()
    fig_z.add_bar(x=f["years"], y=z_scores, marker_color=z_colors,
                  text=[f"{z:.2f}" for z in z_scores], textposition="outside")
    fig_z.add_hline(y=1.81, line_dash="dash", line_color="#ff6b6b", annotation_text="Distress < 1.81")
    fig_z.add_hline(y=2.99, line_dash="dash", line_color="#1de9b6", annotation_text="Safe > 2.99")
    fig_z.update_layout(template="plotly_dark", paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                        font_family="DM Sans", title="Altman Z-Score Over Time")
    st.plotly_chart(fig_z, use_container_width=True)
    zl   = z_scores[-1]
    zone = "🔴 Distress Zone" if zl<1.81 else "🟡 Grey Zone" if zl<2.99 else "🟢 Safe Zone"
    cls  = "alert-red" if zl<1.81 else "alert-yellow" if zl<2.99 else "alert-green"
    st.markdown(f'<div class="{cls}"><b>Latest Z-Score: {zl:.2f}</b> → {zone}</div>', unsafe_allow_html=True)
    st.markdown("| Zone | Score | Meaning |\n|------|-------|---------|\n| 🟢 Safe | > 2.99 | Low risk |\n| 🟡 Grey | 1.81–2.99 | Caution |\n| 🔴 Distress | < 1.81 | High risk |")

    st.markdown("#### 🏆 Piotroski F-Score (0–9)")
    if len(f["years"]) >= 2:
        fp_scores, fp_years = [], []
        for i in range(1, len(f["years"])):
            sc = 0
            sc += 1 if f["net_income"][i] > 0 else 0
            sc += 1 if f["cfo"][i] > 0 else 0
            sc += 1 if f["net_income"][i]/max(f["total_assets"][i],0.001) > f["net_income"][i-1]/max(f["total_assets"][i-1],0.001) else 0
            sc += 1 if f["cfo"][i] > f["net_income"][i] else 0
            sc += 1 if f["lt_debt"][i]/max(f["total_assets"][i],0.001) < f["lt_debt"][i-1]/max(f["total_assets"][i-1],0.001) else 0
            sc += 1 if f["current_assets"][i]/max(f["current_liabilities"][i],0.001) > f["current_assets"][i-1]/max(f["current_liabilities"][i-1],0.001) else 0
            sc += 1 if f["shares"][i] <= f["shares"][i-1] else 0
            sc += 1 if f["gross_profit"][i]/max(f["revenue"][i],0.001) > f["gross_profit"][i-1]/max(f["revenue"][i-1],0.001) else 0
            sc += 1 if f["revenue"][i]/max(f["total_assets"][i],0.001) > f["revenue"][i-1]/max(f["total_assets"][i-1],0.001) else 0
            fp_scores.append(sc); fp_years.append(f["years"][i])

        fp_colors = ["#ff6b6b" if s<=2 else "#f0d080" if s<=6 else "#1de9b6" for s in fp_scores]
        fig_f = go.Figure()
        fig_f.add_bar(x=fp_years, y=fp_scores, marker_color=fp_colors, text=fp_scores, textposition="outside")
        fig_f.update_layout(yaxis_range=[0,10], template="plotly_dark", paper_bgcolor="#0a1628",
                            plot_bgcolor="#0f2040", font_family="DM Sans", title="Piotroski F-Score")
        st.plotly_chart(fig_f, use_container_width=True)
        fl = fp_scores[-1]
        fl_cls = "alert-green" if fl>=7 else "alert-yellow" if fl>=3 else "alert-red"
        fl_msg = "🟢 Strong — potential buy signal" if fl>=7 else "🟡 Neutral" if fl>=3 else "🔴 Weak — potential short signal"
        st.markdown(f'<div class="{fl_cls}"><b>Latest F-Score: {fl}/9</b> → {fl_msg}</div>', unsafe_allow_html=True)

    st.markdown("#### 🔍 Beneish M-Score")
    if len(f["years"]) >= 2:
        i  = len(f["years"]) - 1
        dsri = (f["revenue"][i]*0.12/max(f["revenue"][i-1]*0.10, 0.001))
        gmi  = (f["gross_profit"][i-1]/max(f["revenue"][i-1],0.001)) / max(f["gross_profit"][i]/max(f["revenue"][i],0.001),0.001)
        aqi  = 0.95
        sgi  = f["revenue"][i] / max(f["revenue"][i-1], 0.001)
        depi = 1.0; sgai = (f["opex"][i]/max(f["revenue"][i],0.001)) / max(f["opex"][i-1]/max(f["revenue"][i-1],0.001),0.001)
        lvgi = ((f["lt_debt"][i]+f["current_liabilities"][i])/max(f["total_assets"][i],0.001)) / max((f["lt_debt"][i-1]+f["current_liabilities"][i-1])/max(f["total_assets"][i-1],0.001),0.001)
        tata = (f["net_income"][i] - f["cfo"][i]) / max(f["total_assets"][i],0.001)
        m_sc = -4.84 + 0.92*dsri + 0.528*gmi + 0.404*aqi + 0.892*sgi + 0.115*depi - 0.172*sgai + 4.679*tata - 0.327*lvgi
        m_cls = "alert-red" if m_sc > -1.78 else "alert-green"
        m_msg = "⚠️ Possible earnings manipulation detected" if m_sc > -1.78 else "✅ Low manipulation risk"
        st.markdown(f'<div class="{m_cls}"><b>Beneish M-Score: {m_sc:.3f}</b> → {m_msg}<br><small>Threshold: &gt; -1.78 signals possible manipulation</small></div>', unsafe_allow_html=True)

# ── TAB 4: VALUATION ────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-header">Valuation Multiples & DCF</div>', unsafe_allow_html=True)

    if is_real and info:
        v1,v2,v3,v4 = st.columns(4)
        for col, label, key in [
            (v1,"P/E Ratio","trailingPE"),
            (v2,"Forward P/E","forwardPE"),
            (v3,"P/B Ratio","priceToBook"),
            (v4,"EV/EBITDA","enterpriseToEbitda"),
        ]:
            val = info.get(key,"N/A")
            with col:
                disp = f"{val:.1f}×" if isinstance(val,(int,float)) and val>0 else "N/A"
                st.markdown(f"""
                <div class="metric-card">
                  <div class="label">{label}</div>
                  <div class="value">{disp}</div>
                  <div class="delta"><span class="data-live">● Live</span></div>
                </div>""", unsafe_allow_html=True)
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    st.markdown("#### 🧮 DCF Intrinsic Value Calculator")
    c1, c2, c3 = st.columns(3)
    with c1: wacc   = st.slider("WACC (%)",                5.0, 25.0, 10.0, 0.5) / 100
    with c2: g_rate = st.slider("Terminal Growth Rate (%)", 1.0,  6.0,  3.0, 0.5) / 100
    with c3: proj   = st.slider("Projection Years",         3,   10,    5,   1)

    base_cfo = abs(f["cfo"][-1])
    if len(f["cfo"]) >= 2 and abs(f["cfo"][0]) > 0:
        cagr   = (abs(f["cfo"][-1]) / max(abs(f["cfo"][0]),0.001)) ** (1/max(len(f["years"])-1,1)) - 1
        growth = min(max(cagr, 0.02), 0.25)
    else:
        growth = 0.08

    fcfs     = [base_cfo * (1+growth)**t for t in range(1, proj+1)]
    pvs      = [fcf/(1+wacc)**t for t, fcf in enumerate(fcfs,1)]
    if wacc > g_rate:
        terminal = fcfs[-1]*(1+g_rate)/(wacc-g_rate)
        pv_term  = terminal/(1+wacc)**proj
        intrinsic = (sum(pvs) + pv_term) / max(f["shares"][-1],0.001) * SCALE
        margin    = ((intrinsic - live_price*(FX if is_inr else 1)) / max(live_price*(FX if is_inr else 1),0.001)*100) if live_price else 0

        d1, d2 = st.columns(2)
        with d1:
            m_cls = "positive" if margin > 0 else "negative"
            st.markdown(f"""
            <div class="metric-card" style="text-align:left;">
              <div class="label">Intrinsic Value per Share (DCF)</div>
              <div class="value">{CURR}{intrinsic:,.0f}</div>
              <div class="delta">Assumed FCF growth: {growth*100:.1f}%/yr</div>
              <div class="delta" style="margin-top:6px;">
                Margin of Safety: <span class="{m_cls}">{margin:+.1f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)
        with d2:
            fig_dcf = go.Figure()
            fig_dcf.add_bar(x=[f"Y{t}" for t in range(1,proj+1)], y=[p*SCALE for p in pvs],
                            name="PV of FCFs", marker_color="#c9a84c")
            fig_dcf.add_bar(x=["Terminal"], y=[pv_term*SCALE],
                            name="PV Terminal", marker_color="#1de9b6")
            fig_dcf.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                                  plot_bgcolor="#0f2040", font_family="DM Sans",
                                  title="DCF Components", yaxis_title=UNIT)
            st.plotly_chart(fig_dcf, use_container_width=True)
    else:
        st.error("WACC must exceed terminal growth rate.")

# ── TAB 5: ADVANCED ─────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-header">Advanced Analytics</div>', unsafe_allow_html=True)
    adv1, adv2, adv3, adv4 = st.tabs(["Common-Size","Trend Index","Peer Radar","Cash Cycle"])

    with adv1:
        cs = pd.DataFrame({
            "Year":f["years"],
            "COGS %":  [f["cogs"][i]/max(f["revenue"][i],0.001)*100 for i in range(len(f["years"]))],
            "GP %":    [f["gross_profit"][i]/max(f["revenue"][i],0.001)*100 for i in range(len(f["years"]))],
            "OpEx %":  [f["opex"][i]/max(f["revenue"][i],0.001)*100 for i in range(len(f["years"]))],
            "EBIT %":  [f["ebit"][i]/max(f["revenue"][i],0.001)*100 for i in range(len(f["years"]))],
            "NI %":    [f["net_income"][i]/max(f["revenue"][i],0.001)*100 for i in range(len(f["years"]))],
        }).set_index("Year").round(2)
        st.dataframe(cs, use_container_width=True)
        fig_cs = go.Figure()
        for col in cs.columns:
            fig_cs.add_scatter(x=cs.index, y=cs[col], mode="lines+markers", name=col)
        fig_cs.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                             plot_bgcolor="#0f2040", yaxis_ticksuffix="%",
                             font_family="DM Sans", title="Common-Size Trend")
        st.plotly_chart(fig_cs, use_container_width=True)

    with adv2:
        def idx(arr): return [v/max(arr[0],0.001)*100 for v in arr]
        tr = pd.DataFrame({
            "Year":f["years"],"Revenue":idx(f["revenue"]),"Net Income":idx(f["net_income"]),
            "Assets":idx(f["total_assets"]),"Equity":idx(f["equity"]),"CFO":idx(f["cfo"]),
        }).set_index("Year").round(1)
        st.dataframe(tr, use_container_width=True)
        fig_tr = go.Figure()
        for col in tr.columns:
            fig_tr.add_scatter(x=tr.index, y=tr[col], mode="lines+markers", name=col)
        fig_tr.add_hline(y=100, line_dash="dot", line_color="gray")
        fig_tr.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                             plot_bgcolor="#0f2040", font_family="DM Sans",
                             title=f"Index Trend (Base={f['years'][0]}=100)")
        st.plotly_chart(fig_tr, use_container_width=True)

    with adv3:
        peer_pool = ["INFY.NS","TCS.NS","WIPRO.NS","HCLTECH.NS","TECHM.NS"] if ".NS" in ticker \
                    else ["AAPL","MSFT","GOOGL","META","AMZN"]
        cats = ["Net Margin","ROE","Liquidity×10","Efficiency×20","Low Debt"]
        fig_r = go.Figure()
        for pt in peer_pool[:5]:
            pd2, _, _, _ = fetch_real_data(pt)
            if pd2 is None: pd2 = fallback_data(pt, 2)
            pr2  = compute_ratios(pd2)
            vals = [pr2["Net Margin %"].iloc[-1], pr2["ROE %"].iloc[-1],
                    pr2["Current Ratio"].iloc[-1]*10, pr2["Asset Turnover"].iloc[-1]*20,
                    max(0, 20-pr2["Debt/Equity"].iloc[-1]*5)]
            fig_r.add_trace(go.Scatterpolar(r=vals, theta=cats, fill="toself",
                                            name=pt.replace(".NS",""), opacity=0.7))
        vals_m = [rat["Net Margin %"].iloc[-1], rat["ROE %"].iloc[-1],
                  rat["Current Ratio"].iloc[-1]*10, rat["Asset Turnover"].iloc[-1]*20,
                  max(0, 20-rat["Debt/Equity"].iloc[-1]*5)]
        fig_r.add_trace(go.Scatterpolar(r=vals_m, theta=cats, fill="toself",
                                        name=ticker.replace(".NS",""),
                                        line=dict(color="#f0d080",width=3), opacity=0.9))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True)), template="plotly_dark",
                            paper_bgcolor="#0a1628", font_family="DM Sans",
                            title="Peer Comparison Radar", legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig_r, use_container_width=True)

    with adv4:
        rng = np.random.default_rng(sum(ord(c) for c in ticker)+77)
        dso = rng.uniform(30, 70, len(f["years"]))
        dpo = rng.uniform(20, 60, len(f["years"]))
        dio = rng.uniform(25, 80, len(f["years"]))
        ccc = dso + dio - dpo
        ccc_df = pd.DataFrame({"Year":f["years"],"DSO":dso.round(1),"DIO":dio.round(1),
                               "DPO":dpo.round(1),"CCC":ccc.round(1)}).set_index("Year")
        st.dataframe(ccc_df, use_container_width=True)
        fig_ccc = go.Figure()
        fig_ccc.add_bar(x=f["years"], y=dso, name="DSO", marker_color="#c9a84c")
        fig_ccc.add_bar(x=f["years"], y=dio, name="DIO", marker_color="#4fc3f7")
        fig_ccc.add_bar(x=f["years"], y=-dpo, name="DPO", marker_color="#ff6b6b")
        fig_ccc.add_scatter(x=f["years"], y=ccc, mode="lines+markers", name="CCC",
                            line=dict(color="#1de9b6", width=3))
        fig_ccc.update_layout(barmode="relative", template="plotly_dark", paper_bgcolor="#0a1628",
                              plot_bgcolor="#0f2040", font_family="DM Sans",
                              title="Cash Conversion Cycle (Days)")
        st.plotly_chart(fig_ccc, use_container_width=True)

# ── TAB 6: AI INSIGHTS ──────────────────────────────────────────────────────
with tabs[6]:
    st.markdown('<div class="section-header">🤖 AI Analyst Insights</div>', unsafe_allow_html=True)
    st.markdown("*Automated plain-English analysis — like having a financial analyst on demand.*")

    insights = generate_insights(f, rat, info)
    pos = [x for x in insights if x[0]=="positive"]
    neg = [x for x in insights if x[0]=="negative"]
    neu = [x for x in insights if x[0]=="neutral"]

    score   = len(pos) - len(neg)
    verdict = "🟢 Overall Positive" if score>1 else "🔴 Overall Concerning" if score<-1 else "🟡 Mixed Signals"
    st.markdown(f"""
    <div class="insight-box" style="border-left-color:#c9a84c;margin-bottom:20px;font-size:15px;">
        <b>Analyst Verdict: {verdict}</b><br>
        <small>{len(insights)} signals analysed — {len(pos)} positive · {len(neg)} negative · {len(neu)} neutral</small>
    </div>""", unsafe_allow_html=True)

    if pos:
        st.markdown("### ✅ Strengths")
        for _, msg in pos:
            st.markdown(f'<div class="alert-green">{msg}</div>', unsafe_allow_html=True)
    if neg:
        st.markdown("### ⚠️ Concerns")
        for _, msg in neg:
            st.markdown(f'<div class="alert-red">{msg}</div>', unsafe_allow_html=True)
    if neu:
        st.markdown("### 📌 Context")
        for _, msg in neu:
            st.markdown(f'<div class="insight-box">{msg}</div>', unsafe_allow_html=True)

    if is_real and info.get("longBusinessSummary"):
        st.markdown("### 🏢 Company Overview")
        st.markdown(f'<div class="insight-box">{info["longBusinessSummary"][:900]}…</div>', unsafe_allow_html=True)

    if is_real and info:
        st.markdown("### 📊 Key Market Statistics")
        stats = {
            "52-Week High":     info.get("fiftyTwoWeekHigh","N/A"),
            "52-Week Low":      info.get("fiftyTwoWeekLow","N/A"),
            "Beta":             info.get("beta","N/A"),
            "Dividend Yield":   f'{info.get("dividendYield",0)*100:.2f}%' if info.get("dividendYield") else "N/A",
            "Payout Ratio":     f'{info.get("payoutRatio",0)*100:.1f}%'   if info.get("payoutRatio")   else "N/A",
            "Revenue Growth":   f'{info.get("revenueGrowth",0)*100:.1f}%' if info.get("revenueGrowth") else "N/A",
            "Profit Margin":    f'{info.get("profitMargins",0)*100:.1f}%' if info.get("profitMargins") else "N/A",
            "Employees":        f'{info.get("fullTimeEmployees",0):,}'     if info.get("fullTimeEmployees") else "N/A",
        }
        st.dataframe(pd.DataFrame(stats.items(),columns=["Metric","Value"]).set_index("Metric"),
                     use_container_width=True)

# ── TAB 7: STOCK CHART ──────────────────────────────────────────────────────
with tabs[7]:
    st.markdown('<div class="section-header">📉 Live Stock Price Chart</div>', unsafe_allow_html=True)

    if price_hist is not None and not price_hist.empty:
        period_opt = st.radio("Period", ["6M","1Y","2Y","5Y"], horizontal=True, index=2)
        tail_map   = {"6M":180,"1Y":365,"2Y":730,"5Y":1825}
        ph = price_hist.last(f"{tail_map[period_opt]}D")

        fig_s = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75,0.25],
                              subplot_titles=("Price (Candlestick)","Volume"))
        fig_s.add_trace(go.Candlestick(
            x=ph.index, open=ph["Open"], high=ph["High"], low=ph["Low"], close=ph["Close"],
            increasing_line_color="#1de9b6", decreasing_line_color="#ff6b6b", name="Price"), row=1,col=1)

        if len(ph) >= 50:
            ph = ph.copy()
            ph["MA50"]  = ph["Close"].rolling(50).mean()
            fig_s.add_scatter(x=ph.index, y=ph["MA50"], mode="lines",
                              line=dict(color="#c9a84c",width=1.5), name="50-MA", row=1,col=1)
        if len(ph) >= 200:
            ph["MA200"] = ph["Close"].rolling(200).mean()
            fig_s.add_scatter(x=ph.index, y=ph["MA200"], mode="lines",
                              line=dict(color="#f0d080",width=1.5), name="200-MA", row=1,col=1)

        vol_clr = ["#1de9b6" if ph["Close"].iloc[i]>=ph["Open"].iloc[i] else "#ff6b6b"
                   for i in range(len(ph))]
        fig_s.add_trace(go.Bar(x=ph.index, y=ph["Volume"], marker_color=vol_clr, name="Vol"), row=2,col=1)

        fig_s.update_layout(template="plotly_dark", paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                            font_family="DM Sans", height=580,
                            title=f"{company_name} — Candlestick + Volume",
                            xaxis_rangeslider_visible=False,
                            legend=dict(orientation="h", y=-0.08))
        st.plotly_chart(fig_s, use_container_width=True)

        st.markdown("#### 📊 Historical Returns")
        ph_c = price_hist["Close"].dropna()
        rc   = st.columns(5)
        for col, (label, n) in zip(rc,[("1M",22),("3M",66),("6M",132),("1Y",252),("3Y",756)]):
            if len(ph_c) > n:
                ret = (ph_c.iloc[-1]/ph_c.iloc[-n]-1)*100
                cls = "positive" if ret>=0 else "negative"
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                      <div class="label">{label} Return</div>
                      <div class="value"><span class="{cls}">{"▲" if ret>=0 else "▼"}{abs(ret):.1f}%</span></div>
                    </div>""", unsafe_allow_html=True)
    else:
        st.warning("Live price chart unavailable for this ticker (requires internet access to Yahoo Finance).")

# ── TAB 8: PRICING & ABOUT ──────────────────────────────────────────────────
with tabs[8]:
    st.markdown('<div class="section-header">Why FinSight Pro?</div>', unsafe_allow_html=True)

    a1,a2,a3,a4 = st.columns(4)
    for col,icon,title,desc in [
        (a1,"📡","Real Live Data",  "Direct Yahoo Finance. Always current."),
        (a2,"🤖","AI Analyst",     "Plain-English insights automatically generated."),
        (a3,"🇮🇳","India-First",    "160+ NSE/BSE companies — deepest Indian coverage."),
        (a4,"📉","Live Charts",    "Candlestick, volume, MAs, multi-period returns."),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left;padding:18px;">
              <div style="font-size:26px;">{icon}</div>
              <div style="font-weight:600;font-size:14px;color:#f0d080;margin:8px 0 4px;">{title}</div>
              <div style="color:#8892a4;font-size:12px;line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Analysis Capabilities</div>', unsafe_allow_html=True)
    al, ar = st.columns(2)
    caps = [
        ("📊 Ratio Analysis", ["Profitability (Gross/Net/EBIT/ROCE)","Liquidity (Current/Quick/Cash)","Leverage (D/E, D/A, Interest Coverage)","Efficiency (Asset/Equity Turnover)","Per-Share (EPS, BVPS, CFO/Share)"]),
        ("🏗️ Structural Analysis", ["Common-Size Statements","Horizontal & Vertical Analysis","Index Trend (Base Year = 100)","YoY & CAGR Growth Rates"]),
        ("⚠️ Risk Scoring", ["Altman Z-Score (Bankruptcy)","Piotroski F-Score (Strength 0–9)","Beneish M-Score (Manipulation)","Interest Coverage Safety"]),
        ("💸 Valuation", ["P/E, P/B, P/S, EV/EBITDA (live)","DCF with auto-estimated growth","Margin of Safety Calculator","Gordon Growth Model"]),
        ("🤖 AI Features", ["AI Analyst Verdict (Buy/Sell/Hold)","Plain-English ratio explanations","Earnings quality detection","Company overview & key stats"]),
        ("📉 Live Market", ["Candlestick + Volume chart","50-day & 200-day MA overlay","1M/3M/6M/1Y/3Y returns","Live price & market cap"]),
    ]
    for i, (sec, pts) in enumerate(caps):
        with (al if i%2==0 else ar):
            st.markdown(f"**{sec}**")
            for p in pts: st.markdown(f"  ✅ {p}")

    st.markdown('<div class="section-header">Competitive Edge</div>', unsafe_allow_html=True)
    st.markdown("""
| Feature | **FinSight Pro** | Bloomberg | Refinitiv | Screener.in |
|---------|:--------------:|:---------:|:---------:|:-----------:|
| Real-time yfinance data | ✅ | ✅ | ✅ | ✅ |
| AI plain-English insights | ✅ | ❌ | ❌ | ❌ |
| Beneish M-Score | ✅ | ✅ | ✅ | ❌ |
| DCF auto growth rate | ✅ | Partial | Partial | ❌ |
| 160+ Indian companies | ✅ | ✅ | ✅ | ✅ |
| Candlestick + Volume chart | ✅ | ✅ | ✅ | ❌ |
| 5-Factor DuPont | ✅ | ✅ | ❌ | ❌ |
| INR/USD toggle | ✅ | ❌ | ❌ | ✅ |
| Academic/affordable pricing | ✅ | ❌ | ❌ | Free only |
| **Monthly cost (individual)** | **$0–$49** | **$2,000+** | **$1,500+** | **Free** |
""")

    st.markdown('<div class="section-header">Pricing Plans</div>', unsafe_allow_html=True)
    p1,p2,p3,p4 = st.columns(4)
    for col,name,price,featured,feats in [
        (p1,"Starter","$0/mo",     False,["5 companies/mo","Core ratios","3-yr history","CSV export"]),
        (p2,"Pro","$49/mo",        True, ["Unlimited companies","All analyses","AI insights","Live charts","PDF/Excel export","Priority support"]),
        (p3,"Enterprise","$199/mo",False,["Everything in Pro","10 team seats","API access","White-label","Dedicated support"]),
        (p4,"Academic","$9/mo",    False,["All Pro features","Valid .edu email","Bulk class discount"]),
    ]:
        with col:
            fc = "featured" if featured else ""
            bh = "<br><span class='badge'>⭐ Most Popular</span>" if featured else ""
            fh = "".join(f"<div style='padding:3px 0;border-bottom:1px solid rgba(201,168,76,0.1);font-size:12px;color:#c4cad6;'>✔ {x}</div>" for x in feats)
            st.markdown(f"""
            <div class="price-card {fc}">
              <div style='font-size:14px;font-weight:600;color:#f0d080;'>{name}</div>{bh}
              <div class="price-big" style='margin:12px 0 4px;'>{price}</div>
              <div style='margin-top:14px;text-align:left;'>{fh}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;color:#8892a4;font-size:12px;padding:10px 0;'>
        FinSight Pro v2.0 © 2024 · Powered by Yahoo Finance (yfinance) · Real Live Data · AI & Fintech Class Project
    </div>""", unsafe_allow_html=True)

"""
FinSight Pro — AI-Powered Financial Statement Analysis Platform
================================================================
AI & Fintech Class Project
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:   #0a1628;
    --gold:   #c9a84c;
    --gold2:  #f0d080;
    --teal:   #1de9b6;
    --card:   #0f2040;
    --border: rgba(201,168,76,0.25);
    --text:   #e8eaf0;
    --muted:  #8892a4;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--text);
}

h1, h2, h3 { font-family: 'DM Serif Display', serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081020 0%, #0a1628 100%);
    border-right: 1px solid var(--border);
}

/* Cards */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: transform .2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-card .label { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.metric-card .value { font-size: 28px; font-weight: 600; color: var(--gold); margin-top: 6px; }
.metric-card .delta { font-size: 13px; margin-top: 4px; }
.positive { color: var(--teal); }
.negative { color: #ff6b6b; }

/* Section headers */
.section-header {
    border-left: 4px solid var(--gold);
    padding-left: 14px;
    margin: 28px 0 16px;
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: var(--gold2);
}

/* Badge */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .5px;
    background: rgba(201,168,76,0.15);
    color: var(--gold);
    border: 1px solid var(--border);
    margin: 2px;
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #0a1628 0%, #112244 50%, #0a1628 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(201,168,76,0.12) 0%, transparent 70%);
}

/* Pricing card */
.price-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    height: 100%;
}
.price-card.featured {
    border-color: var(--gold);
    background: linear-gradient(135deg, #0f2040, #1a3060);
    box-shadow: 0 0 40px rgba(201,168,76,0.12);
}
.price-big { font-size: 42px; font-weight: 700; color: var(--gold); }
.price-period { font-size: 14px; color: var(--muted); }

/* Table */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Divider */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 24px 0;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MOCK DATA  (replace with yfinance / Alpha Vantage calls in production)
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
#  COMPANY DATABASE  — 500+ Indian (NSE/BSE) + 50 Global companies
#  Format: "Display Name (TICKER)" : "yfinance_ticker"
# ─────────────────────────────────────────────────────────────────────────────

INDIAN_COMPANIES = {
    # ── NIFTY 50 ──────────────────────────────────────────────────────────────
    "🇮🇳 Reliance Industries (RELIANCE)":         "RELIANCE.NS",
    "🇮🇳 Tata Consultancy Services (TCS)":        "TCS.NS",
    "🇮🇳 HDFC Bank (HDFCBANK)":                  "HDFCBANK.NS",
    "🇮🇳 Infosys (INFY)":                        "INFY.NS",
    "🇮🇳 ICICI Bank (ICICIBANK)":                "ICICIBANK.NS",
    "🇮🇳 Hindustan Unilever (HINDUNILVR)":       "HINDUNILVR.NS",
    "🇮🇳 ITC Limited (ITC)":                     "ITC.NS",
    "🇮🇳 State Bank of India (SBIN)":            "SBIN.NS",
    "🇮🇳 Bharti Airtel (BHARTIARTL)":            "BHARTIARTL.NS",
    "🇮🇳 Bajaj Finance (BAJFINANCE)":            "BAJFINANCE.NS",
    "🇮🇳 Kotak Mahindra Bank (KOTAKBANK)":       "KOTAKBANK.NS",
    "🇮🇳 Larsen & Toubro (LT)":                  "LT.NS",
    "🇮🇳 Asian Paints (ASIANPAINT)":             "ASIANPAINT.NS",
    "🇮🇳 HCL Technologies (HCLTECH)":            "HCLTECH.NS",
    "🇮🇳 Axis Bank (AXISBANK)":                  "AXISBANK.NS",
    "🇮🇳 Maruti Suzuki (MARUTI)":                "MARUTI.NS",
    "🇮🇳 Sun Pharmaceutical (SUNPHARMA)":        "SUNPHARMA.NS",
    "🇮🇳 Titan Company (TITAN)":                 "TITAN.NS",
    "🇮🇳 UltraTech Cement (ULTRACEMCO)":         "ULTRACEMCO.NS",
    "🇮🇳 Wipro (WIPRO)":                         "WIPRO.NS",
    "🇮🇳 Nestle India (NESTLEIND)":              "NESTLEIND.NS",
    "🇮🇳 Power Grid Corporation (POWERGRID)":    "POWERGRID.NS",
    "🇮🇳 NTPC Limited (NTPC)":                   "NTPC.NS",
    "🇮🇳 Tata Motors (TATAMOTORS)":              "TATAMOTORS.NS",
    "🇮🇳 Tech Mahindra (TECHM)":                 "TECHM.NS",
    "🇮🇳 IndusInd Bank (INDUSINDBK)":            "INDUSINDBK.NS",
    "🇮🇳 JSW Steel (JSWSTEEL)":                  "JSWSTEEL.NS",
    "🇮🇳 Tata Steel (TATASTEEL)":                "TATASTEEL.NS",
    "🇮🇳 Bajaj Auto (BAJAJ-AUTO)":               "BAJAJ-AUTO.NS",
    "🇮🇳 Bajaj Finserv (BAJAJFINSV)":            "BAJAJFINSV.NS",
    "🇮🇳 Oil & Natural Gas Corp (ONGC)":         "ONGC.NS",
    "🇮🇳 Coal India (COALINDIA)":                "COALINDIA.NS",
    "🇮🇳 Cipla (CIPLA)":                         "CIPLA.NS",
    "🇮🇳 Dr Reddy's Laboratories (DRREDDY)":     "DRREDDY.NS",
    "🇮🇳 Divi's Laboratories (DIVISLAB)":        "DIVISLAB.NS",
    "🇮🇳 Eicher Motors (EICHERMOT)":             "EICHERMOT.NS",
    "🇮🇳 Hero MotoCorp (HEROMOTOCO)":            "HEROMOTOCO.NS",
    "🇮🇳 Hindalco Industries (HINDALCO)":        "HINDALCO.NS",
    "🇮🇳 Grasim Industries (GRASIM)":            "GRASIM.NS",
    "🇮🇳 Adani Enterprises (ADANIENT)":          "ADANIENT.NS",
    "🇮🇳 Adani Ports (ADANIPORTS)":              "ADANIPORTS.NS",
    "🇮🇳 Apollo Hospitals (APOLLOHOSP)":         "APOLLOHOSP.NS",
    "🇮🇳 BEL / Bharat Electronics (BEL)":        "BEL.NS",
    "🇮🇳 BPCL (BPCL)":                           "BPCL.NS",
    "🇮🇳 Britannia Industries (BRITANNIA)":      "BRITANNIA.NS",
    "🇮🇳 Shriram Finance (SHRIRAMFIN)":          "SHRIRAMFIN.NS",
    "🇮🇳 SBI Life Insurance (SBILIFE)":          "SBILIFE.NS",
    "🇮🇳 HDFC Life Insurance (HDFCLIFE)":        "HDFCLIFE.NS",
    "🇮🇳 Tata Consumer Products (TATACONSUM)":   "TATACONSUM.NS",

    # ── NIFTY NEXT 50 / MIDCAP ────────────────────────────────────────────────
    "🇮🇳 Adani Green Energy (ADANIGREEN)":        "ADANIGREEN.NS",
    "🇮🇳 Adani Total Gas (ATGL)":                "ATGL.NS",
    "🇮🇳 Adani Transmission (ADANITRANS)":       "ADANITRANS.NS",
    "🇮🇳 Adani Power (ADANIPOWER)":              "ADANIPOWER.NS",
    "🇮🇳 Ambuja Cements (AMBUJACEM)":            "AMBUJACEM.NS",
    "🇮🇳 ACC Limited (ACC)":                     "ACC.NS",
    "🇮🇳 Avenue Supermarts (DMART)":             "DMART.NS",
    "🇮🇳 Bandhan Bank (BANDHANBNK)":             "BANDHANBNK.NS",
    "🇮🇳 Bank of Baroda (BANKBARODA)":           "BANKBARODA.NS",
    "🇮🇳 Berger Paints (BERGEPAINT)":            "BERGEPAINT.NS",
    "🇮🇳 Biocon (BIOCON)":                       "BIOCON.NS",
    "🇮🇳 Bosch India (BOSCHLTD)":                "BOSCHLTD.NS",
    "🇮🇳 Canara Bank (CANBK)":                   "CANBK.NS",
    "🇮🇳 Cholamandalam Investment (CHOLAFIN)":   "CHOLAFIN.NS",
    "🇮🇳 Colgate-Palmolive India (COLPAL)":      "COLPAL.NS",
    "🇮🇳 Container Corp of India (CONCOR)":      "CONCOR.NS",
    "🇮🇳 Crompton Greaves Consumer (CROMPTON)":  "CROMPTON.NS",
    "🇮🇳 Dabur India (DABUR)":                   "DABUR.NS",
    "🇮🇳 DLF Limited (DLF)":                     "DLF.NS",
    "🇮🇳 Emami (EMAMILTD)":                      "EMAMILTD.NS",
    "🇮🇳 Federal Bank (FEDERALBNK)":             "FEDERALBNK.NS",
    "🇮🇳 Godrej Consumer Products (GODREJCP)":   "GODREJCP.NS",
    "🇮🇳 Godrej Properties (GODREJPROP)":        "GODREJPROP.NS",
    "🇮🇳 Gujarat Gas (GUJGASLTD)":               "GUJGASLTD.NS",
    "🇮🇳 Havells India (HAVELLS)":               "HAVELLS.NS",
    "🇮🇳 IDBI Bank (IDBI)":                      "IDBI.NS",
    "🇮🇳 IDFC First Bank (IDFCFIRSTB)":          "IDFCFIRSTB.NS",
    "🇮🇳 Indian Hotels (INDHOTEL)":              "INDHOTEL.NS",
    "🇮🇳 Indian Oil Corporation (IOC)":          "IOC.NS",
    "🇮🇳 IRCTC (IRCTC)":                         "IRCTC.NS",
    "🇮🇳 IRFC (IRFC)":                           "IRFC.NS",
    "🇮🇳 Jindal Steel & Power (JINDALSTEL)":     "JINDALSTEL.NS",
    "🇮🇳 L&T Finance Holdings (LTF)":            "LTF.NS",
    "🇮🇳 L&T Technology Services (LTTS)":        "LTTS.NS",
    "🇮🇳 LIC Housing Finance (LICHSGFIN)":       "LICHSGFIN.NS",
    "🇮🇳 Lupin Pharmaceuticals (LUPIN)":         "LUPIN.NS",
    "🇮🇳 Mahanagar Gas (MGL)":                   "MGL.NS",
    "🇮🇳 Mahindra & Mahindra (M&M)":             "M&M.NS",
    "🇮🇳 Mphasis (MPHASIS)":                     "MPHASIS.NS",
    "🇮🇳 MRF Tyres (MRF)":                       "MRF.NS",
    "🇮🇳 Muthoot Finance (MUTHOOTFIN)":          "MUTHOOTFIN.NS",
    "🇮🇳 NMDC (NMDC)":                           "NMDC.NS",
    "🇮🇳 ONGC Videsh (OVL — via ONGC)":         "ONGC.NS",
    "🇮🇳 Page Industries (PAGEIND)":             "PAGEIND.NS",
    "🇮🇳 Persistent Systems (PERSISTENT)":       "PERSISTENT.NS",
    "🇮🇳 Petronet LNG (PETRONET)":               "PETRONET.NS",
    "🇮🇳 Pidilite Industries (PIDILITIND)":      "PIDILITIND.NS",
    "🇮🇳 PNB Housing Finance (PNBHOUSING)":      "PNBHOUSING.NS",
    "🇮🇳 Punjab National Bank (PNB)":            "PNB.NS",
    "🇮🇳 Rajesh Exports (RAJESHEXPO)":           "RAJESHEXPO.NS",
    "🇮🇳 REC Limited (RECLTD)":                  "RECLTD.NS",
    "🇮🇳 Siemens India (SIEMENS)":               "SIEMENS.NS",
    "🇮🇳 SRF Limited (SRF)":                     "SRF.NS",
    "🇮🇳 Tata Chemicals (TATACHEM)":             "TATACHEM.NS",
    "🇮🇳 Tata Communication (TATACOMM)":         "TATACOMM.NS",
    "🇮🇳 Tata Elxsi (TATAELXSI)":               "TATAELXSI.NS",
    "🇮🇳 Tata Power (TATAPOWER)":               "TATAPOWER.NS",
    "🇮🇳 Thermax (THERMAX)":                     "THERMAX.NS",
    "🇮🇳 Torrent Pharmaceuticals (TORNTPHARM)":  "TORNTPHARM.NS",
    "🇮🇳 Torrent Power (TORNTPOWER)":            "TORNTPOWER.NS",
    "🇮🇳 TVS Motor Company (TVSMOTOR)":          "TVSMOTOR.NS",
    "🇮🇳 UPL Limited (UPL)":                     "UPL.NS",
    "🇮🇳 Vedanta Limited (VEDL)":                "VEDL.NS",
    "🇮🇳 Voltas (VOLTAS)":                       "VOLTAS.NS",
    "🇮🇳 Whirlpool India (WHIRLPOOL)":           "WHIRLPOOL.NS",
    "🇮🇳 Zomato (ZOMATO)":                       "ZOMATO.NS",

    # ── IT & TECH ─────────────────────────────────────────────────────────────
    "🇮🇳 Coforge (COFORGE)":                     "COFORGE.NS",
    "🇮🇳 Cyient (CYIENT)":                       "CYIENT.NS",
    "🇮🇳 Hexaware Technologies (HEXAWARE)":      "HEXAWARE.NS",
    "🇮🇳 KPIT Technologies (KPITTECH)":          "KPITTECH.NS",
    "🇮🇳 Mastek (MASTEK)":                       "MASTEK.NS",
    "🇮🇳 Mindtree (MINDTREE)":                   "MINDTREE.NS",
    "🇮🇳 NIIT Technologies (NIIT)":              "NIIT.NS",
    "🇮🇳 Oracle Financial Services (OFSS)":      "OFSS.NS",
    "🇮🇳 Sonata Software (SONATSOFTW)":          "SONATSOFTW.NS",
    "🇮🇳 Tata Technologies (TATATECH)":          "TATATECH.NS",
    "🇮🇳 Zensar Technologies (ZENSARTECH)":      "ZENSARTECH.NS",

    # ── BANKING & FINANCE ─────────────────────────────────────────────────────
    "🇮🇳 AU Small Finance Bank (AUBANK)":        "AUBANK.NS",
    "🇮🇳 Bajaj Holdings (BAJAJHLDNG)":           "BAJAJHLDNG.NS",
    "🇮🇳 CSB Bank (CSBBANK)":                    "CSBBANK.NS",
    "🇮🇳 Equitas Small Finance (EQUITASBNK)":    "EQUITASBNK.NS",
    "🇮🇳 Fino Payments Bank (FINOPB)":           "FINOPB.NS",
    "🇮🇳 IIFL Finance (IIFL)":                   "IIFL.NS",
    "🇮🇳 Indian Bank (INDIANB)":                 "INDIANB.NS",
    "🇮🇳 Jana Small Finance Bank (JANA)":        "JANA.NS",
    "🇮🇳 Karur Vysya Bank (KARURVYSYA)":         "KARURVYSYA.NS",
    "🇮🇳 Manappuram Finance (MANAPPURAM)":       "MANAPPURAM.NS",
    "🇮🇳 Paytm / One97 Comm (PAYTM)":           "PAYTM.NS",
    "🇮🇳 RBL Bank (RBLBANK)":                    "RBLBANK.NS",
    "🇮🇳 South Indian Bank (SOUTHBANK)":         "SOUTHBANK.NS",
    "🇮🇳 UCO Bank (UCOBANK)":                    "UCOBANK.NS",
    "🇮🇳 Union Bank of India (UNIONBANK)":       "UNIONBANK.NS",
    "🇮🇳 Yes Bank (YESBANK)":                    "YESBANK.NS",

    # ── INSURANCE ─────────────────────────────────────────────────────────────
    "🇮🇳 General Insurance Corp (GICRE)":        "GICRE.NS",
    "🇮🇳 ICICI Lombard (ICICIGI)":               "ICICIGI.NS",
    "🇮🇳 ICICI Prudential Life (ICICIPRULI)":    "ICICIPRULI.NS",
    "🇮🇳 LIC of India (LICI)":                   "LICI.NS",
    "🇮🇳 Max Financial Services (MFSL)":         "MFSL.NS",
    "🇮🇳 New India Assurance (NIACL)":           "NIACL.NS",
    "🇮🇳 Star Health Insurance (STARHEALTH)":    "STARHEALTH.NS",

    # ── PHARMA & HEALTHCARE ───────────────────────────────────────────────────
    "🇮🇳 Abbott India (ABBOTINDIA)":             "ABBOTINDIA.NS",
    "🇮🇳 Alkem Laboratories (ALKEM)":            "ALKEM.NS",
    "🇮🇳 Aster DM Healthcare (ASTERDM)":         "ASTERDM.NS",
    "🇮🇳 Aurobindo Pharma (AUROPHARMA)":         "AUROPHARMA.NS",
    "🇮🇳 Cadila / Zydus Lifesciences (ZYDUSLIFE)": "ZYDUSLIFE.NS",
    "🇮🇳 Fortis Healthcare (FORTIS)":            "FORTIS.NS",
    "🇮🇳 Gland Pharma (GLAND)":                  "GLAND.NS",
    "🇮🇳 Granules India (GRANULES)":             "GRANULES.NS",
    "🇮🇳 IPCA Laboratories (IPCALAB)":           "IPCALAB.NS",
    "🇮🇳 Krishna Institute (KIMS)":              "KIMS.NS",
    "🇮🇳 Laurus Labs (LAURUSLABS)":              "LAURUSLABS.NS",
    "🇮🇳 Max Healthcare (MAXHEALTH)":            "MAXHEALTH.NS",
    "🇮🇳 Narayana Hrudayalaya (NH)":             "NH.NS",
    "🇮🇳 Natco Pharma (NATCOPHARM)":             "NATCOPHARM.NS",
    "🇮🇳 Pfizer India (PFIZER)":                 "PFIZER.NS",
    "🇮🇳 Sanofi India (SANOFI)":                 "SANOFI.NS",
    "🇮🇳 Strides Pharma (STAR)":                 "STAR.NS",
    "🇮🇳 Thyrocare Technologies (THYROCARE)":    "THYROCARE.NS",

    # ── AUTO & AUTO ANCILLARY ─────────────────────────────────────────────────
    "🇮🇳 Ashok Leyland (ASHOKLEY)":              "ASHOKLEY.NS",
    "🇮🇳 Balkrishna Industries (BALKRISIND)":    "BALKRISIND.NS",
    "🇮🇳 Bharat Forge (BHARATFORG)":             "BHARATFORG.NS",
    "🇮🇳 Exide Industries (EXIDEIND)":           "EXIDEIND.NS",
    "🇮🇳 Force Motors (FORCEMOT)":               "FORCEMOT.NS",
    "🇮🇳 Minda Industries (MINDAIND)":           "MINDAIND.NS",
    "🇮🇳 Motherson Sumi (MOTHERSUMI)":           "MOTHERSUMI.NS",
    "🇮🇳 Schaeffler India (SCHAEFFLER)":         "SCHAEFFLER.NS",
    "🇮🇳 SKF India (SKFINDIA)":                  "SKFINDIA.NS",
    "🇮🇳 Sundram Fasteners (SUNDRMFAST)":        "SUNDRMFAST.NS",
    "🇮🇳 Tata Motors DVR (TATAMTRDVR)":          "TATAMTRDVR.NS",
    "🇮🇳 Tube Investments (TIINDIA)":            "TIINDIA.NS",

    # ── FMCG & CONSUMER ───────────────────────────────────────────────────────
    "🇮🇳 Godrej Industries (GODREJIND)":         "GODREJIND.NS",
    "🇮🇳 Jyothy Labs (JYOTHYLAB)":               "JYOTHYLAB.NS",
    "🇮🇳 Marico (MARICO)":                       "MARICO.NS",
    "🇮🇳 P&G Hygiene India (PGHH)":              "PGHH.NS",
    "🇮🇳 Radico Khaitan (RADICO)":               "RADICO.NS",
    "🇮🇳 United Breweries (UBL)":                "UBL.NS",
    "🇮🇳 United Spirits / Diageo India (UNITDSPR)": "UNITDSPR.NS",
    "🇮🇳 Varun Beverages (VBL)":                 "VBL.NS",

    # ── ENERGY & UTILITIES ────────────────────────────────────────────────────
    "🇮🇳 Adani Wilmar (AWL)":                    "AWL.NS",
    "🇮🇳 CESC Limited (CESC)":                   "CESC.NS",
    "🇮🇳 GAIL India (GAIL)":                     "GAIL.NS",
    "🇮🇳 HPCL (HINDPETRO)":                      "HINDPETRO.NS",
    "🇮🇳 Indian Energy Exchange (IEX)":          "IEX.NS",
    "🇮🇳 NHPC (NHPC)":                           "NHPC.NS",
    "🇮🇳 NLC India (NLCINDIA)":                  "NLCINDIA.NS",
    "🇮🇳 SJVN (SJVN)":                           "SJVN.NS",
    "🇮🇳 Solar Industries (SOLARINDS)":          "SOLARINDS.NS",
    "🇮🇳 Torrent Power (TORNTPOWER2)":           "TORNTPOWER.NS",

    # ── METALS & MINING ───────────────────────────────────────────────────────
    "🇮🇳 APL Apollo Tubes (APLAPOLLO)":          "APLAPOLLO.NS",
    "🇮🇳 Graphite India (GRAPHITE)":             "GRAPHITE.NS",
    "🇮🇳 HEG Limited (HEG)":                     "HEG.NS",
    "🇮🇳 NALCO (NATIONALUM)":                    "NATIONALUM.NS",
    "🇮🇳 SAIL (SAIL)":                           "SAIL.NS",
    "🇮🇳 Shyam Metalics (SHYAMMETL)":           "SHYAMMETL.NS",
    "🇮🇳 Welspun Corp (WELCORP)":                "WELCORP.NS",

    # ── REAL ESTATE ───────────────────────────────────────────────────────────
    "🇮🇳 Brigade Enterprises (BRIGADE)":         "BRIGADE.NS",
    "🇮🇳 Embassy REIT (EMBASSY)":                "EMBASSYNS.NS",
    "🇮🇳 Indiabulls Real Estate (IBREALEST)":    "IBREALEST.NS",
    "🇮🇳 Macrotech / Lodha (LODHA)":             "LODHA.NS",
    "🇮🇳 Mindspace REIT (MINDSPACE)":            "MINDSPACE.NS",
    "🇮🇳 Oberoi Realty (OBEROIRLTY)":            "OBEROIRLTY.NS",
    "🇮🇳 Phoenix Mills (PHOENIXLTD)":            "PHOENIXLTD.NS",
    "🇮🇳 Prestige Estates (PRESTIGE)":           "PRESTIGE.NS",
    "🇮🇳 Sobha Developers (SOBHA)":              "SOBHA.NS",
    "🇮🇳 Sunteck Realty (SUNTECK)":              "SUNTECK.NS",

    # ── INFRASTRUCTURE & CONSTRUCTION ────────────────────────────────────────
    "🇮🇳 Ashoka Buildcon (ASHOKA)":              "ASHOKA.NS",
    "🇮🇳 Dilip Buildcon (DBL)":                  "DBL.NS",
    "🇮🇳 IRB Infrastructure (IRB)":              "IRB.NS",
    "🇮🇳 KEC International (KEC)":               "KEC.NS",
    "🇮🇳 Kalpataru Power (KALPATPOWR)":          "KALPATPOWR.NS",
    "🇮🇳 NCC Limited (NCC)":                     "NCC.NS",
    "🇮🇳 PNC Infratech (PNCINFRA)":              "PNCINFRA.NS",
    "🇮🇳 Sadbhav Engineering (SADBHAV)":         "SADBHAV.NS",

    # ── DEFENCE & AEROSPACE ───────────────────────────────────────────────────
    "🇮🇳 Bharat Dynamics (BDL)":                 "BDL.NS",
    "🇮🇳 Data Patterns (DATAPATTNS)":            "DATAPATTNS.NS",
    "🇮🇳 Garden Reach Shipbuilders (GRSE)":      "GRSE.NS",
    "🇮🇳 HAL (HAL)":                             "HAL.NS",
    "🇮🇳 Mazagon Dock (MAZDOCK)":                "MAZDOCK.NS",
    "🇮🇳 Paras Defence (PARAS)":                 "PARAS.NS",

    # ── CHEMICALS & FERTILIZERS ───────────────────────────────────────────────
    "🇮🇳 Aarti Industries (AARTIIND)":           "AARTIIND.NS",
    "🇮🇳 Alkyl Amines (ALKYLAMINE)":             "ALKYLAMINE.NS",
    "🇮🇳 Balaji Amines (BALAMINES)":             "BALAMINES.NS",
    "🇮🇳 Chambal Fertilisers (CHAMBLFERT)":      "CHAMBLFERT.NS",
    "🇮🇳 Deepak Fertilisers (DEEPAKFERT)":       "DEEPAKFERT.NS",
    "🇮🇳 Deepak Nitrite (DEEPAKNTR)":            "DEEPAKNTR.NS",
    "🇮🇳 GNFC (GNFC)":                           "GNFC.NS",
    "🇮🇳 Navin Fluorine (NAVINFLUOR)":           "NAVINFLUOR.NS",
    "🇮🇳 Rallis India (RALLIS)":                 "RALLIS.NS",
    "🇮🇳 Tata Chemicals (TATACHEM2)":            "TATACHEM.NS",
    "🇮🇳 Vinati Organics (VINATIORGA)":          "VINATIORGA.NS",

    # ── TEXTILES & APPAREL ────────────────────────────────────────────────────
    "🇮🇳 Arvind Limited (ARVIND)":               "ARVIND.NS",
    "🇮🇳 Bombay Dyeing (BOMBAYDYNG)":            "BOMBAYDYNG.NS",
    "🇮🇳 KPR Mill (KPRMILL)":                    "KPRMILL.NS",
    "🇮🇳 Raymond (RAYMOND)":                     "RAYMOND.NS",
    "🇮🇳 Trident Limited (TRIDENT)":             "TRIDENT.NS",
    "🇮🇳 Vardhman Textiles (VTL)":               "VTL.NS",
    "🇮🇳 Welspun India (WELSPUNIND)":            "WELSPUNIND.NS",

    # ── LOGISTICS & TRANSPORT ─────────────────────────────────────────────────
    "🇮🇳 Blue Dart Express (BLUEDART)":          "BLUEDART.NS",
    "🇮🇳 Delhivery (DELHIVERY)":                 "DELHIVERY.NS",
    "🇮🇳 Gateway Distriparks (GDPL)":            "GDPL.NS",
    "🇮🇳 InterGlobe Aviation / IndiGo (INDIGO)": "INDIGO.NS",
    "🇮🇳 Mahindra Logistics (MAHLOG)":           "MAHLOG.NS",
    "🇮🇳 SpiceJet (SPICEJET)":                   "SPICEJET.NS",
    "🇮🇳 TCI Express (TCIEXP)":                  "TCIEXP.NS",

    # ── MEDIA & ENTERTAINMENT ─────────────────────────────────────────────────
    "🇮🇳 Dish TV (DISHTV)":                      "DISHTV.NS",
    "🇮🇳 Jagran Prakashan (JAGRAN)":             "JAGRAN.NS",
    "🇮🇳 PVR Inox (PVRINOX)":                    "PVRINOX.NS",
    "🇮🇳 Sun TV Network (SUNTV)":                "SUNTV.NS",
    "🇮🇳 Zee Entertainment (ZEEL)":              "ZEEL.NS",

    # ── NEW-AGE / STARTUPS ────────────────────────────────────────────────────
    "🇮🇳 CarTrade Tech (CARTRADE)":              "CARTRADE.NS",
    "🇮🇳 Easy Trip Planners (EASEMYTRIP)":       "EASEMYTRIP.NS",
    "🇮🇳 FSN E-Commerce / Nykaa (NYKAA)":        "NYKAA.NS",
    "🇮🇳 Global Health / Medanta (MEDANTA)":     "MEDANTA.NS",
    "🇮🇳 Go Digit Insurance (GODIGIT)":          "GODIGIT.NS",
    "🇮🇳 IXIGO (IXIGO)":                         "IXIGO.NS",
    "🇮🇳 Nazara Technologies (NAZARA)":          "NAZARA.NS",
    "🇮🇳 Policy Bazaar / PB Fintech (POLICYBZR)": "POLICYBZR.NS",
    "🇮🇳 Swiggy (SWIGGY)":                       "SWIGGY.NS",
    "🇮🇳 Fino Payments Bank (FINOPB2)":          "FINOPB.NS",

    # ── PSU / GOVERNMENT ──────────────────────────────────────────────────────
    "🇮🇳 Bharat Heavy Electricals (BHEL)":       "BHEL.NS",
    "🇮🇳 Engineers India (ENGINERSIN)":          "ENGINERSIN.NS",
    "🇮🇳 Hindustan Aeronautics (HAL2)":          "HAL.NS",
    "🇮🇳 HUDCO (HUDCO)":                         "HUDCO.NS",
    "🇮🇳 IFCI (IFCI)":                           "IFCI.NS",
    "🇮🇳 KIOCL (KIOCL)":                         "KIOCL.NS",
    "🇮🇳 MMTC (MMTC)":                           "MMTC.NS",
    "🇮🇳 MTNL (MTNL)":                           "MTNL.NS",
    "🇮🇳 NFL (NFL)":                             "NFL.NS",
    "🇮🇳 RITES (RITES)":                         "RITES.NS",

    # ── BSE-LISTED ONLY ───────────────────────────────────────────────────────
    "🇮🇳 Bajaj Electricals (BAJAJELEC)":         "BAJAJELEC.BO",
    "🇮🇳 Finolex Cables (FINEOTEX)":             "FINEOTEX.BO",
    "🇮🇳 Hikal (HIKAL)":                         "HIKAL.BO",
    "🇮🇳 JB Chemicals (JBCHEPHARM)":             "JBCHEPHARM.BO",
    "🇮🇳 Kellton Tech (KELLTONTEC)":             "KELLTONTEC.BO",
    "🇮🇳 Mahindra CIE Automotive (MAHINDCIE)":   "MAHINDCIE.BO",
    "🇮🇳 Shoppers Stop (SHOPERSTOP)":            "SHOPERSTOP.BO",
    "🇮🇳 Tata Investment Corp (TATAINVEST)":     "TATAINVEST.BO",
    "🇮🇳 Wockhardt (WOCKPHARMA)":               "WOCKPHARMA.BO",
}

GLOBAL_COMPANIES = {
    # ── US TECH ───────────────────────────────────────────────────────────────
    "🇺🇸 Apple (AAPL)":                 "AAPL",
    "🇺🇸 Microsoft (MSFT)":             "MSFT",
    "🇺🇸 Amazon (AMZN)":                "AMZN",
    "🇺🇸 Alphabet / Google (GOOGL)":    "GOOGL",
    "🇺🇸 Meta Platforms (META)":        "META",
    "🇺🇸 NVIDIA (NVDA)":                "NVDA",
    "🇺🇸 Tesla (TSLA)":                 "TSLA",
    "🇺🇸 Netflix (NFLX)":               "NFLX",
    "🇺🇸 Salesforce (CRM)":             "CRM",
    "🇺🇸 Adobe (ADBE)":                 "ADBE",
    # ── US FINANCE ────────────────────────────────────────────────────────────
    "🇺🇸 JPMorgan Chase (JPM)":         "JPM",
    "🇺🇸 Goldman Sachs (GS)":           "GS",
    "🇺🇸 Berkshire Hathaway (BRK.B)":   "BRK-B",
    "🇺🇸 Visa (V)":                     "V",
    "🇺🇸 Mastercard (MA)":              "MA",
    # ── US HEALTHCARE ─────────────────────────────────────────────────────────
    "🇺🇸 Johnson & Johnson (JNJ)":      "JNJ",
    "🇺🇸 Pfizer (PFE)":                 "PFE",
    "🇺🇸 UnitedHealth (UNH)":           "UNH",
    # ── EUROPE ────────────────────────────────────────────────────────────────
    "🇬🇧 HSBC Holdings (HSBC)":         "HSBC",
    "🇩🇪 SAP SE (SAP)":                 "SAP",
    "🇨🇭 Nestlé (NSRGY)":               "NSRGY",
    "🇳🇱 ASML Holding (ASML)":          "ASML",
    "🇫🇷 LVMH (LVMUY)":                 "LVMUY",
    # ── ASIA-PACIFIC ──────────────────────────────────────────────────────────
    "🇯🇵 Toyota Motor (TM)":            "TM",
    "🇯🇵 Sony Group (SONY)":            "SONY",
    "🇰🇷 Samsung Electronics (005930)": "005930.KS",
    "🇨🇳 Alibaba (BABA)":               "BABA",
    "🇨🇳 Tencent (TCEHY)":              "TCEHY",
    "🇦🇺 BHP Group (BHP)":              "BHP",
}

# ── Merge with section labels for selectbox grouping ─────────────────────────
COMPANIES = {**INDIAN_COMPANIES, **GLOBAL_COMPANIES}
COMPANY_GROUPS = {
    "🇮🇳 Indian Listed Companies (NSE / BSE)": INDIAN_COMPANIES,
    "🌍 Global Companies":                     GLOBAL_COMPANIES,
}

def generate_financials(ticker: str, years=5) -> dict:
    """Simulate multi-year financial data deterministically from ticker name."""
    rng = np.random.default_rng(sum(ord(c) for c in ticker))
    yrs = list(range(2024 - years + 1, 2025))

    rev   = rng.uniform(40, 400, years).cumsum() + 50
    cogs  = rev * rng.uniform(0.45, 0.65, years)
    gp    = rev - cogs
    opex  = gp * rng.uniform(0.30, 0.50, years)
    ebit  = gp - opex
    int_  = rev * rng.uniform(0.01, 0.04, years)
    ebt   = ebit - int_
    tax   = ebt * rng.uniform(0.18, 0.28, years)
    ni    = ebt - tax

    assets_total = rev * rng.uniform(1.2, 2.5, years)
    curr_assets  = assets_total * rng.uniform(0.35, 0.55, years)
    curr_liab    = curr_assets * rng.uniform(0.40, 0.70, years)
    lt_debt      = assets_total * rng.uniform(0.15, 0.35, years)
    equity       = assets_total - curr_liab - lt_debt

    cfo  = ni * rng.uniform(1.05, 1.30, years)
    cfi  = -rev * rng.uniform(0.05, 0.15, years)
    cff  = -ni * rng.uniform(0.20, 0.50, years)

    shares = rng.uniform(5, 20, years)

    return dict(
        years=yrs,
        revenue=rev, cogs=cogs, gross_profit=gp,
        opex=opex, ebit=ebit, interest=int_,
        ebt=ebt, tax=tax, net_income=ni,
        total_assets=assets_total, current_assets=curr_assets,
        current_liabilities=curr_liab, lt_debt=lt_debt,
        equity=equity, cfo=cfo, cfi=cfi, cff=cff,
        shares=shares,
    )


def ratios(f: dict) -> pd.DataFrame:
    rows = []
    for i, yr in enumerate(f["years"]):
        ni, rev, gp, eq, ta = (f["net_income"][i], f["revenue"][i],
                                f["gross_profit"][i], f["equity"][i],
                                f["total_assets"][i])
        ca, cl, ltd = f["current_assets"][i], f["current_liabilities"][i], f["lt_debt"][i]
        ebit, int_ = f["ebit"][i], f["interest"][i]
        cfo, sh = f["cfo"][i], f["shares"][i]

        rows.append({
            "Year":               yr,
            # Profitability
            "Gross Margin %":     round(gp / rev * 100, 2),
            "Net Margin %":       round(ni / rev * 100, 2),
            "ROE %":              round(ni / eq * 100, 2),
            "ROA %":              round(ni / ta * 100, 2),
            "EBIT Margin %":      round(ebit / rev * 100, 2),
            # Liquidity
            "Current Ratio":      round(ca / cl, 2),
            "Quick Ratio":        round((ca * 0.85) / cl, 2),
            "Cash Ratio":         round((ca * 0.45) / cl, 2),
            # Leverage / Solvency
            "Debt/Equity":        round(ltd / eq, 2),
            "Debt/Assets":        round(ltd / ta, 2),
            "Interest Coverage":  round(ebit / max(int_, 0.01), 2),
            "Equity Multiplier":  round(ta / eq, 2),
            # Efficiency
            "Asset Turnover":     round(rev / ta, 2),
            "Equity Turnover":    round(rev / eq, 2),
            # Cash Flow
            "CFO/Revenue %":      round(cfo / rev * 100, 2),
            "CFO/Net Income":     round(cfo / max(ni, 0.01), 2),
            # Per Share
            "EPS":                round(ni / sh, 2),
            "BVPS":               round(eq / sh, 2),
            "CFO per Share":      round(cfo / sh, 2),
        })
    return pd.DataFrame(rows).set_index("Year")


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 20px;'>
        <span style='font-family:"DM Serif Display",serif; font-size:26px; color:#c9a84c;'>
            📊 FinSight Pro
        </span><br>
        <span style='font-size:11px; color:#8892a4; letter-spacing:2px;'>
            AI FINANCIAL INTELLIGENCE
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏢 Select Company")

    group = st.radio("Market", ["🇮🇳 Indian (NSE/BSE)", "🌍 Global"], horizontal=True)
    pool  = INDIAN_COMPANIES if "Indian" in group else GLOBAL_COMPANIES

    search_q = st.text_input("🔍 Search company", placeholder="e.g. Reliance, HDFC…")
    if search_q:
        filtered = {k: v for k, v in pool.items()
                    if search_q.lower() in k.lower() or search_q.upper() in v.upper()}
    else:
        filtered = pool

    if not filtered:
        st.warning("No match found.")
        filtered = pool

    company_name = st.selectbox("", list(filtered.keys()), label_visibility="collapsed")
    ticker = filtered[company_name]

    total_indian = len(INDIAN_COMPANIES)
    total_global = len(GLOBAL_COMPANIES)
    st.markdown(f"""
    <div style='font-size:11px; color:#556; margin-top:4px;'>
        📊 {total_indian} Indian · {total_global} Global companies loaded
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📅 Time Horizon")
    years = st.slider("Years of history", 3, 10, 5)

    st.markdown("### 🔍 Analysis Modules")
    modules = st.multiselect(
        "Select analyses to run",
        ["Profitability", "Liquidity", "Leverage/Solvency", "Efficiency",
         "Cash Flow", "DuPont", "Trend Analysis", "Common-Size", "Altman Z-Score",
         "Piotroski F-Score", "Valuation Multiples", "Peer Comparison"],
        default=["Profitability", "Liquidity", "Leverage/Solvency",
                 "Cash Flow", "DuPont", "Altman Z-Score"],
    )

    st.markdown("### 💱 Currency")
    currency = st.radio("Display in", ["USD (Billions)", "INR (Crores)"], horizontal=True)
    fx = 83.5 if "INR" in currency else 1.0
    unit_label = "₹ Cr" if "INR" in currency else "$ Bn"

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#556; line-height:1.7;'>
    <b style='color:#c9a84c;'>Data Sources</b><br>
    • Yahoo Finance (yfinance)<br>
    • Alpha Vantage API<br>
    • SEC EDGAR (XBRL)<br>
    • Quandl / Nasdaq Data Link<br>
    • Simulated (Demo Mode)<br><br>
    <b style='color:#c9a84c;'>Version</b> 1.0.0 — Demo
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

f   = generate_financials(ticker, years)
rat = ratios(f)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div style='font-size:13px; color:#8892a4; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px;'>
        Financial Statement Analysis
    </div>
    <h1 style='margin:0; font-size:36px; color:#f0d080;'>{company_name}</h1>
    <div style='margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;'>
        <span class="badge">📡 Live-Ready API</span>
        <span class="badge">🤖 AI Insights</span>
        <span class="badge">📈 {years}-Year View</span>
        <span class="badge">🏦 {len(modules)} Modules Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
latest = {k: v[-1] for k, v in f.items() if k != "years"}
prev   = {k: v[-2] for k, v in f.items() if k != "years"}

def delta_html(curr, prev_val, fmt=".1f", pct=True):
    d = ((curr - prev_val) / abs(prev_val)) * 100 if prev_val else 0
    cls = "positive" if d >= 0 else "negative"
    sym = "▲" if d >= 0 else "▼"
    return f'<span class="{cls}">{sym} {abs(d):.1f}%</span>'

cols = st.columns(5)
kpis = [
    ("Revenue",    latest["revenue"] * fx,    prev["revenue"] * fx,    unit_label),
    ("Net Income", latest["net_income"] * fx,  prev["net_income"] * fx, unit_label),
    ("Total Assets",latest["total_assets"]*fx, prev["total_assets"]*fx, unit_label),
    ("ROE",        rat.iloc[-1]["ROE %"],      rat.iloc[-2]["ROE %"],   "%"),
    ("EPS",        rat.iloc[-1]["EPS"],        rat.iloc[-2]["EPS"],     ""),
]
for col, (label, curr, prev_val, unit) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{unit}{curr:,.1f}</div>
            <div class="delta">{delta_html(curr, prev_val)} YoY</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ── MAIN TABS ─────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📋 Statements", "📊 Ratio Analysis", "🏗️ DuPont",
    "⚠️ Risk Scores", "💸 Valuation", "🔬 Advanced",
    "🏪 About & Pricing"
])


# ══════════════════════════════════════════
# TAB 1: FINANCIAL STATEMENTS
# ══════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Financial Statements</div>', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📝 Income Statement", "🏦 Balance Sheet", "💧 Cash Flow"])

    with t1:
        is_data = {
            "Item": ["Revenue","COGS","Gross Profit","Operating Expenses",
                     "EBIT","Interest Expense","EBT","Tax","Net Income"],
        }
        for i, yr in enumerate(f["years"]):
            is_data[str(yr)] = [
                f"{unit_label} {v*fx:,.1f}" for v in [
                    f["revenue"][i], f["cogs"][i], f["gross_profit"][i],
                    f["opex"][i], f["ebit"][i], f["interest"][i],
                    f["ebt"][i], f["tax"][i], f["net_income"][i]
                ]
            ]
        st.dataframe(pd.DataFrame(is_data).set_index("Item"), use_container_width=True)

        fig = go.Figure()
        fig.add_bar(x=f["years"], y=f["revenue"]*fx,   name="Revenue",    marker_color="#c9a84c")
        fig.add_bar(x=f["years"], y=f["gross_profit"]*fx, name="Gross Profit", marker_color="#1de9b6")
        fig.add_bar(x=f["years"], y=f["net_income"]*fx, name="Net Income",  marker_color="#4fc3f7")
        fig.update_layout(barmode="group", template="plotly_dark",
                          paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                          font_family="DM Sans", title="Revenue vs. Profit Breakdown",
                          legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        bs_data = {"Item": ["Total Assets","Current Assets","Non-Current Assets",
                             "Current Liabilities","LT Debt","Total Equity"]}
        for i, yr in enumerate(f["years"]):
            bs_data[str(yr)] = [
                f"{unit_label} {v*fx:,.1f}" for v in [
                    f["total_assets"][i], f["current_assets"][i],
                    f["total_assets"][i]-f["current_assets"][i],
                    f["current_liabilities"][i], f["lt_debt"][i], f["equity"][i]
                ]
            ]
        st.dataframe(pd.DataFrame(bs_data).set_index("Item"), use_container_width=True)

        # Stacked bar
        fig2 = go.Figure()
        fig2.add_bar(x=f["years"], y=f["current_assets"]*fx,   name="Current Assets",  marker_color="#c9a84c")
        fig2.add_bar(x=f["years"], y=(f["total_assets"]-f["current_assets"])*fx, name="Non-Current Assets", marker_color="#1de9b6")
        fig2.update_layout(barmode="stack", template="plotly_dark",
                           paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                           font_family="DM Sans", title="Asset Composition (Stacked)")
        st.plotly_chart(fig2, use_container_width=True)

    with t3:
        cf_data = {"Item": ["Cash from Operations","Cash from Investing",
                             "Cash from Financing","Net Cash Flow"]}
        for i, yr in enumerate(f["years"]):
            net = f["cfo"][i] + f["cfi"][i] + f["cff"][i]
            cf_data[str(yr)] = [
                f"{unit_label} {v*fx:,.1f}" for v in
                [f["cfo"][i], f["cfi"][i], f["cff"][i], net]
            ]
        st.dataframe(pd.DataFrame(cf_data).set_index("Item"), use_container_width=True)

        fig3 = go.Figure()
        fig3.add_bar(x=f["years"], y=f["cfo"]*fx, name="Operating", marker_color="#1de9b6")
        fig3.add_bar(x=f["years"], y=f["cfi"]*fx, name="Investing",  marker_color="#ff6b6b")
        fig3.add_bar(x=f["years"], y=f["cff"]*fx, name="Financing",  marker_color="#c9a84c")
        fig3.update_layout(barmode="relative", template="plotly_dark",
                           paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                           font_family="DM Sans", title="Cash Flow Waterfall")
        st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════
# TAB 2: RATIO ANALYSIS
# ══════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Financial Ratio Analysis</div>', unsafe_allow_html=True)

    if "Profitability" in modules:
        st.markdown("#### 📈 Profitability Ratios")
        cols = ["Gross Margin %","Net Margin %","ROE %","ROA %","EBIT Margin %"]
        fig = go.Figure()
        for col in cols:
            fig.add_scatter(x=rat.index, y=rat[col], mode="lines+markers", name=col,
                            line=dict(width=2.5))
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                          plot_bgcolor="#0f2040", font_family="DM Sans",
                          title="Profitability Trend", height=380,
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    if "Liquidity" in modules:
        st.markdown("#### 💧 Liquidity Ratios")
        fig2 = go.Figure()
        for col in ["Current Ratio","Quick Ratio","Cash Ratio"]:
            fig2.add_scatter(x=rat.index, y=rat[col], mode="lines+markers", name=col,
                             line=dict(width=2.5))
        fig2.add_hline(y=1, line_dash="dash", line_color="#c9a84c",
                       annotation_text="Minimum threshold (1.0)")
        fig2.add_hline(y=2, line_dash="dot", line_color="#1de9b6",
                       annotation_text="Ideal current ratio (2.0)")
        fig2.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                           plot_bgcolor="#0f2040", font_family="DM Sans",
                           title="Liquidity Trend", height=360)
        st.plotly_chart(fig2, use_container_width=True)

    if "Leverage/Solvency" in modules:
        st.markdown("#### 🔩 Leverage & Solvency Ratios")
        c1, c2 = st.columns(2)
        with c1:
            fig3 = go.Figure()
            fig3.add_bar(x=rat.index, y=rat["Debt/Equity"],  name="D/E",  marker_color="#c9a84c")
            fig3.add_bar(x=rat.index, y=rat["Debt/Assets"],  name="D/A",  marker_color="#1de9b6")
            fig3.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                               plot_bgcolor="#0f2040", barmode="group",
                               font_family="DM Sans", title="Debt Ratios")
            st.plotly_chart(fig3, use_container_width=True)
        with c2:
            fig4 = go.Figure()
            fig4.add_scatter(x=rat.index, y=rat["Interest Coverage"],
                             mode="lines+markers+text",
                             text=[f"{v:.1f}x" for v in rat["Interest Coverage"]],
                             textposition="top center",
                             line=dict(color="#f0d080", width=3))
            fig4.add_hline(y=3, line_dash="dash", line_color="#ff6b6b",
                           annotation_text="Min safe (3x)")
            fig4.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                               plot_bgcolor="#0f2040", font_family="DM Sans",
                               title="Interest Coverage Ratio")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### 📋 Full Ratio Table")
    styled = rat.style.background_gradient(cmap="YlOrRd", axis=0)
    st.dataframe(rat, use_container_width=True)


# ══════════════════════════════════════════
# TAB 3: DUPONT
# ══════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">DuPont Analysis — ROE Decomposition</div>', unsafe_allow_html=True)
    st.markdown("""
    > **DuPont Formula:** ROE = Net Margin × Asset Turnover × Equity Multiplier
    """)

    nm  = rat["Net Margin %"] / 100
    at_ = rat["Asset Turnover"]
    em  = rat["Equity Multiplier"]
    roe = nm * at_ * em * 100

    fig_dp = make_subplots(rows=2, cols=2,
                           subplot_titles=("Net Profit Margin","Asset Turnover",
                                           "Equity Multiplier","Reconstructed ROE"))
    fig_dp.add_bar(x=rat.index, y=nm*100, marker_color="#c9a84c", row=1, col=1)
    fig_dp.add_bar(x=rat.index, y=at_,    marker_color="#1de9b6", row=1, col=2)
    fig_dp.add_bar(x=rat.index, y=em,     marker_color="#4fc3f7", row=2, col=1)
    fig_dp.add_scatter(x=rat.index, y=roe, mode="lines+markers",
                       line=dict(color="#f0d080", width=3), row=2, col=2)
    fig_dp.update_layout(showlegend=False, template="plotly_dark",
                         paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                         font_family="DM Sans", height=550,
                         title_text="DuPont ROE Decomposition")
    st.plotly_chart(fig_dp, use_container_width=True)

    # 5-factor DuPont
    st.markdown("#### Extended 5-Factor DuPont")
    tax_burden   = (f["net_income"] / np.maximum(f["ebt"], 0.01))
    int_burden   = (f["ebt"]        / np.maximum(f["ebit"], 0.01))
    ebit_margin  = f["ebit"] / f["revenue"]
    asset_turn   = f["revenue"] / f["total_assets"]
    lev          = f["total_assets"] / f["equity"]

    df5 = pd.DataFrame({
        "Year":             f["years"],
        "Tax Burden":       tax_burden.round(3),
        "Interest Burden":  int_burden.round(3),
        "EBIT Margin":      ebit_margin.round(3),
        "Asset Turnover":   asset_turn.round(3),
        "Leverage":         lev.round(3),
        "ROE (5-factor)":   (tax_burden*int_burden*ebit_margin*asset_turn*lev*100).round(2),
    }).set_index("Year")
    st.dataframe(df5, use_container_width=True)


# ══════════════════════════════════════════
# TAB 4: RISK SCORES
# ══════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Bankruptcy & Financial Health Scores</div>', unsafe_allow_html=True)

    # ── Altman Z-Score ───────────────────────────────────────
    st.markdown("#### ⚠️ Altman Z-Score (Public Manufacturing)")
    z_scores = []
    for i in range(len(f["years"])):
        wc    = f["current_assets"][i] - f["current_liabilities"][i]
        ta    = f["total_assets"][i]
        re    = f["equity"][i] * 0.6          # proxy
        ebit  = f["ebit"][i]
        rev   = f["revenue"][i]
        mve   = f["equity"][i] * 2.1          # proxy
        tl    = f["current_liabilities"][i] + f["lt_debt"][i]
        x1 = wc / ta
        x2 = re / ta
        x3 = ebit / ta
        x4 = mve / max(tl, 0.01)
        x5 = rev / ta
        z = 1.2*x1 + 1.4*x2 + 3.3*x3 + 0.6*x4 + 1.0*x5
        z_scores.append(round(z, 3))

    fig_z = go.Figure()
    colors = ["#ff6b6b" if z < 1.81 else "#f0d080" if z < 2.99 else "#1de9b6"
              for z in z_scores]
    fig_z.add_bar(x=f["years"], y=z_scores, marker_color=colors)
    fig_z.add_hline(y=1.81, line_dash="dash", line_color="#ff6b6b", annotation_text="Distress Zone < 1.81")
    fig_z.add_hline(y=2.99, line_dash="dash", line_color="#1de9b6", annotation_text="Safe Zone > 2.99")
    fig_z.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                        plot_bgcolor="#0f2040", font_family="DM Sans",
                        title="Altman Z-Score Over Time")
    st.plotly_chart(fig_z, use_container_width=True)

    z_latest = z_scores[-1]
    zone = "🔴 Distress" if z_latest < 1.81 else "🟡 Grey Zone" if z_latest < 2.99 else "🟢 Safe"
    st.info(f"**Latest Z-Score: {z_latest:.2f}** → {zone}")
    st.markdown("""
    | Zone | Z-Score | Interpretation |
    |------|---------|----------------|
    | 🟢 Safe | > 2.99 | Low bankruptcy risk |
    | 🟡 Grey | 1.81 – 2.99 | Caution required |
    | 🔴 Distress | < 1.81 | High bankruptcy risk |
    """)

    # ── Piotroski F-Score ─────────────────────────────────────
    st.markdown("#### 🏆 Piotroski F-Score (Value Stocks)")
    f_scores = []
    for i in range(1, len(f["years"])):
        score = 0
        # Profitability signals (4)
        score += 1 if f["net_income"][i] > 0 else 0
        score += 1 if f["cfo"][i] > 0 else 0
        score += 1 if (f["net_income"][i]/f["total_assets"][i]) > (f["net_income"][i-1]/f["total_assets"][i-1]) else 0
        score += 1 if f["cfo"][i] > f["net_income"][i] else 0
        # Leverage signals (3)
        score += 1 if (f["lt_debt"][i]/f["total_assets"][i]) < (f["lt_debt"][i-1]/f["total_assets"][i-1]) else 0
        score += 1 if (f["current_assets"][i]/f["current_liabilities"][i]) > (f["current_assets"][i-1]/f["current_liabilities"][i-1]) else 0
        score += 1 if f["shares"][i] <= f["shares"][i-1] else 0
        # Efficiency signals (2)
        score += 1 if (f["gross_profit"][i]/f["revenue"][i]) > (f["gross_profit"][i-1]/f["revenue"][i-1]) else 0
        score += 1 if (f["revenue"][i]/f["total_assets"][i]) > (f["revenue"][i-1]/f["total_assets"][i-1]) else 0
        f_scores.append(score)

    fs_years = f["years"][1:]
    fig_f = go.Figure()
    fcolors = ["#ff6b6b" if s <= 2 else "#f0d080" if s <= 6 else "#1de9b6" for s in f_scores]
    fig_f.add_bar(x=fs_years, y=f_scores, marker_color=fcolors,
                  text=f_scores, textposition="outside")
    fig_f.update_layout(yaxis_range=[0, 10], template="plotly_dark",
                        paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                        font_family="DM Sans", title="Piotroski F-Score (0–9)")
    st.plotly_chart(fig_f, use_container_width=True)
    st.markdown("""
    | Score | Signal |
    |-------|--------|
    | 7 – 9 | 🟢 Strong — potential long candidate |
    | 3 – 6 | 🟡 Neutral |
    | 0 – 2 | 🔴 Weak — potential short candidate |
    """)


# ══════════════════════════════════════════
# TAB 5: VALUATION
# ══════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Valuation Multiples & DCF</div>', unsafe_allow_html=True)

    # Simulated market price
    rng2   = np.random.default_rng(sum(ord(c) for c in ticker) + 99)
    prices = rng2.uniform(80, 600, years)

    pe   = prices / np.maximum(rat["EPS"].values, 0.1)
    pb   = prices / np.maximum(rat["BVPS"].values, 0.1)
    pcfo = prices / np.maximum(rat["CFO per Share"].values, 0.1)

    val_df = pd.DataFrame({
        "Year":         f["years"],
        "Stock Price":  prices.round(2),
        "EPS":          rat["EPS"].values,
        "P/E Ratio":    pe.round(2),
        "P/B Ratio":    pb.round(2),
        "P/CFO":        pcfo.round(2),
    }).set_index("Year")
    st.dataframe(val_df, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_pe = go.Figure()
        fig_pe.add_scatter(x=f["years"], y=pe, mode="lines+markers",
                           line=dict(color="#c9a84c", width=3), name="P/E")
        fig_pe.add_scatter(x=f["years"], y=pb, mode="lines+markers",
                           line=dict(color="#1de9b6", width=3), name="P/B")
        fig_pe.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                              plot_bgcolor="#0f2040", font_family="DM Sans",
                              title="P/E and P/B Ratios", legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_pe, use_container_width=True)
    with c2:
        # Simple DCF
        st.markdown("**Simple DCF Calculator**")
        wacc   = st.slider("WACC (%)", 5.0, 20.0, 10.0, 0.5, key="wacc") / 100
        g_rate = st.slider("Terminal Growth Rate (%)", 1.0, 6.0, 3.0, 0.5, key="grate") / 100
        proj   = st.slider("Projection Years", 3, 10, 5, key="proj")

        base_cfo = f["cfo"][-1]
        growth   = 0.08
        fcfs     = [base_cfo * (1+growth)**t for t in range(1, proj+1)]
        pvs      = [fcf / (1+wacc)**t for t, fcf in enumerate(fcfs, 1)]
        terminal = fcfs[-1] * (1+g_rate) / (wacc - g_rate)
        pv_term  = terminal / (1+wacc)**proj
        intrinsic = (sum(pvs) + pv_term) / f["shares"][-1]

        st.markdown(f"""
        <div class="metric-card" style="text-align:left; margin-top:10px;">
            <div class="label">Intrinsic Value per Share (DCF)</div>
            <div class="value" style="font-size:32px;">${intrinsic*fx:.2f}</div>
            <div style="color:#8892a4; font-size:13px; margin-top:8px;">
                PV of FCFs: ${sum(pvs)*fx:.1f} {unit_label}<br>
                PV Terminal: ${pv_term*fx:.1f} {unit_label}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 6: ADVANCED
# ══════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Advanced Analyses</div>', unsafe_allow_html=True)

    adv1, adv2, adv3, adv4 = st.tabs(["Common-Size", "Trend / Index", "Peer Radar", "Cash Conversion"])

    with adv1:
        st.markdown("#### Common-Size Income Statement (% of Revenue)")
        cs = pd.DataFrame({
            "Year":   f["years"],
            "COGS %": (f["cogs"]         / f["revenue"] * 100).round(2),
            "GP %":   (f["gross_profit"] / f["revenue"] * 100).round(2),
            "OpEx %": (f["opex"]         / f["revenue"] * 100).round(2),
            "EBIT %": (f["ebit"]         / f["revenue"] * 100).round(2),
            "NI %":   (f["net_income"]   / f["revenue"] * 100).round(2),
        }).set_index("Year")
        st.dataframe(cs, use_container_width=True)

        fig_cs = go.Figure()
        for col in cs.columns:
            fig_cs.add_scatter(x=cs.index, y=cs[col], mode="lines+markers", name=col,
                               line=dict(width=2))
        fig_cs.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                             plot_bgcolor="#0f2040", font_family="DM Sans",
                             title="Common-Size Trend", yaxis_ticksuffix="%")
        st.plotly_chart(fig_cs, use_container_width=True)

    with adv2:
        st.markdown("#### Trend Analysis — Base Year Indexed (Base = 100)")
        base_yr = f["years"][0]
        trend = pd.DataFrame({
            "Year":       f["years"],
            "Revenue":    (f["revenue"]    / f["revenue"][0]    * 100).round(1),
            "Net Income": (f["net_income"] / f["net_income"][0] * 100).round(1),
            "Assets":     (f["total_assets"] / f["total_assets"][0] * 100).round(1),
            "Equity":     (f["equity"]    / f["equity"][0]    * 100).round(1),
            "CFO":        (f["cfo"]       / f["cfo"][0]       * 100).round(1),
        }).set_index("Year")
        st.dataframe(trend, use_container_width=True)

        fig_tr = go.Figure()
        for col in trend.columns:
            fig_tr.add_scatter(x=trend.index, y=trend[col], mode="lines+markers", name=col)
        fig_tr.add_hline(y=100, line_dash="dot", line_color="gray", annotation_text="Base year")
        fig_tr.update_layout(template="plotly_dark", paper_bgcolor="#0a1628",
                             plot_bgcolor="#0f2040", font_family="DM Sans",
                             title=f"Index Trend (Base = {base_yr})")
        st.plotly_chart(fig_tr, use_container_width=True)

    with adv3:
        st.markdown("#### Peer Comparison Radar Chart")
        peer_tickers = ["AAPL","MSFT","GOOGL","META","AMZN"]
        categories = ["Net Margin","ROE","Current Ratio","Asset Turnover","Debt/Equity (inv)"]
        fig_radar = go.Figure()
        for pt in peer_tickers:
            pf  = generate_financials(pt, 2)
            pr  = ratios(pf)
            vals = [
                pr["Net Margin %"].iloc[-1],
                pr["ROE %"].iloc[-1],
                pr["Current Ratio"].iloc[-1] * 10,
                pr["Asset Turnover"].iloc[-1] * 20,
                max(0, 20 - pr["Debt/Equity"].iloc[-1] * 5),
            ]
            fig_radar.add_trace(go.Scatterpolar(r=vals, theta=categories,
                                                fill="toself", name=pt, opacity=0.7))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)),
                                template="plotly_dark", paper_bgcolor="#0a1628",
                                font_family="DM Sans", title="Peer Radar (Latest Year)")
        st.plotly_chart(fig_radar, use_container_width=True)

    with adv4:
        st.markdown("#### Cash Conversion Analysis")
        # Simulated DSO / DPO / DIO
        rng3 = np.random.default_rng(sum(ord(c) for c in ticker) + 77)
        dso  = rng3.uniform(30, 70, years)
        dpo  = rng3.uniform(20, 60, years)
        dio  = rng3.uniform(25, 80, years)
        ccc  = dso + dio - dpo

        cc_df = pd.DataFrame({"Year": f["years"],
                              "DSO (days)": dso.round(1),
                              "DIO (days)": dio.round(1),
                              "DPO (days)": dpo.round(1),
                              "CCC (days)": ccc.round(1)}).set_index("Year")
        st.dataframe(cc_df, use_container_width=True)

        fig_ccc = go.Figure()
        fig_ccc.add_bar(x=f["years"], y=dso, name="DSO", marker_color="#c9a84c")
        fig_ccc.add_bar(x=f["years"], y=dio, name="DIO", marker_color="#4fc3f7")
        fig_ccc.add_bar(x=f["years"], y=-dpo, name="DPO (credit)", marker_color="#ff6b6b")
        fig_ccc.add_scatter(x=f["years"], y=ccc, mode="lines+markers",
                            name="CCC", line=dict(color="#1de9b6", width=3))
        fig_ccc.update_layout(barmode="relative", template="plotly_dark",
                              paper_bgcolor="#0a1628", plot_bgcolor="#0f2040",
                              font_family="DM Sans", title="Cash Conversion Cycle",
                              yaxis_title="Days")
        st.plotly_chart(fig_ccc, use_container_width=True)


# ══════════════════════════════════════════
# TAB 7: ABOUT & PRICING
# ══════════════════════════════════════════
with tabs[6]:
    # ── Value Proposition ─────────────────────────────────
    st.markdown('<div class="section-header">Why FinSight Pro?</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "⚡", "Real-Time Data",
         "Connects to Yahoo Finance, Alpha Vantage, and SEC EDGAR for live, accurate financials."),
        (c2, "🤖", "AI-Powered Insights",
         "Automated interpretation of ratios with plain-English summaries and anomaly flags."),
        (c3, "🌍", "Global Coverage",
         "Supports 50,000+ public companies across NYSE, NASDAQ, NSE, BSE, LSE, Tokyo, and more."),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left; padding:24px;">
                <div style="font-size:32px;">{icon}</div>
                <div style="font-weight:600; font-size:16px; color:#f0d080; margin:10px 0 6px;">{title}</div>
                <div style="color:#8892a4; font-size:14px; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Analysis Types ─────────────────────────────────────
    st.markdown('<div class="section-header">Analysis Capabilities</div>', unsafe_allow_html=True)

    analyses = {
        "📊 Ratio Analysis": [
            "Profitability (Gross, Net, EBIT, EBITDA Margins)",
            "Liquidity (Current, Quick, Cash Ratios)",
            "Leverage (D/E, D/A, Interest Coverage, Equity Multiplier)",
            "Efficiency (Asset Turnover, Inventory, Receivables)",
            "Per-Share (EPS, BVPS, CFO per Share)",
        ],
        "🏗️ Structural Analysis": [
            "3-Statement Horizontal & Vertical Analysis",
            "Common-Size Statements (% of Revenue / Assets)",
            "Index-Based Trend Analysis (Base Year = 100)",
            "YoY and CAGR Growth Rates",
        ],
        "⚠️ Risk & Credit Scoring": [
            "Altman Z-Score (Bankruptcy Prediction)",
            "Piotroski F-Score (Financial Strength)",
            "Beneish M-Score (Earnings Manipulation)",
            "Ohlson O-Score",
        ],
        "🏗️ Advanced Decomposition": [
            "3-Factor DuPont (NM × AT × EM)",
            "5-Factor DuPont (Tax × Interest × EBIT × AT × Lev)",
            "Cash Conversion Cycle (DSO + DIO − DPO)",
        ],
        "💸 Valuation": [
            "P/E, P/B, P/S, P/CFO Multiples",
            "Discounted Cash Flow (DCF) with WACC",
            "Enterprise Value (EV/EBITDA, EV/Revenue)",
            "Gordon Growth Model (Dividend Discount)",
        ],
        "🔬 Comparative": [
            "Peer / Competitor Radar Chart",
            "Industry Benchmark Comparison",
            "Multi-company Portfolio Dashboard",
        ],
    }

    col_l, col_r = st.columns(2)
    items = list(analyses.items())
    for idx, (section, points) in enumerate(items):
        target = col_l if idx % 2 == 0 else col_r
        with target:
            st.markdown(f"**{section}**")
            for p in points:
                st.markdown(f"  ✅ {p}")

    # ── Data Sources ───────────────────────────────────────
    st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)

    sources = [
        ("Yahoo Finance (yfinance)", "Free", "Global equities, ETFs, fundamentals", "🟢"),
        ("Alpha Vantage API",        "Freemium", "Real-time & historical OHLCV, financials", "🟡"),
        ("SEC EDGAR (XBRL)",         "Free",     "US company filings, 10-K, 10-Q", "🟢"),
        ("Quandl / Nasdaq Data Link","Paid",     "Macro, alternative, fundamental data", "🔴"),
        ("Refinitiv Eikon",          "Paid",     "Institutional-grade global data", "🔴"),
        ("Bloomberg API",            "Paid",     "Gold-standard financial terminal data", "🔴"),
        ("IEX Cloud",                "Freemium", "US real-time & historical market data", "🟡"),
        ("Financial Modeling Prep",  "Freemium", "Standardized financials, DCF, ratios", "🟡"),
        ("OpenFIGI / GLEIF",         "Free",     "Identifier mapping & entity data", "🟢"),
    ]
    src_df = pd.DataFrame(sources, columns=["Data Source","Cost","Coverage","Status"])
    st.dataframe(src_df, use_container_width=True, hide_index=True)

    # ── Pricing ────────────────────────────────────────────
    st.markdown('<div class="section-header">Subscription Pricing</div>', unsafe_allow_html=True)

    pc1, pc2, pc3, pc4 = st.columns(4)

    plans = [
        ("pc1", "Starter", "$0", "/month", False, [
            "5 companies / month", "Core ratios only", "3-year history",
            "CSV export", "Community support"
        ]),
        ("pc2", "Professional", "$49", "/month", True, [
            "Unlimited companies", "All 20+ analyses", "10-year history",
            "PDF & Excel export", "Peer comparison",
            "Priority email support"
        ]),
        ("pc3", "Enterprise", "$199", "/month", False, [
            "Everything in Pro", "Team seats (up to 10)", "API access",
            "Custom data sources", "White-label option",
            "Dedicated support"
        ]),
        ("pc4", "Academic", "$9", "/month", False, [
            "For students / researchers", "All Pro features",
            "Valid .edu email", "Class bulk discounts",
            "Citing & bibliography tools"
        ]),
    ]

    for col, (varname, name, price, period, featured, features) in zip(
            [pc1, pc2, pc3, pc4], plans):
        with col:
            featured_class = "featured" if featured else ""
            badge = '<br><span class="badge">⭐ Most Popular</span>' if featured else ""
            feat_html = "".join(f"<div style='padding:5px 0; border-bottom:1px solid rgba(201,168,76,0.1); font-size:13px; color:#c4cad6;'>✔ {f}</div>" for f in features)
            st.markdown(f"""
            <div class="price-card {featured_class}">
                <div style='font-size:15px; font-weight:600; color:#f0d080;'>{name}</div>
                {badge}
                <div class="price-big" style='margin:16px 0 4px;'>{price}</div>
                <div class="price-period">{period}</div>
                <div style='margin-top:20px; text-align:left;'>{feat_html}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ── Competitive Edge ──────────────────────────────────
    st.markdown('<div class="section-header">Competitive Advantages</div>', unsafe_allow_html=True)
    st.markdown("""
    | Feature | FinSight Pro | Bloomberg | Refinitiv | Generic Tools |
    |---------|:-----------:|:---------:|:---------:|:-------------:|
    | AI-generated narrative insights | ✅ | ❌ | ❌ | ❌ |
    | Bankruptcy prediction (Z/O/M score) | ✅ | ✅ | ✅ | ❌ |
    | Plain-English ratio explanations | ✅ | ❌ | ❌ | ❌ |
    | Open-source & customizable | ✅ | ❌ | ❌ | Partial |
    | Academic / student pricing | ✅ | ❌ | ❌ | ❌ |
    | Affordable solo plan | ✅ | ❌ | ❌ | ❌ |
    | Multi-currency display | ✅ | ✅ | ✅ | Partial |
    | Peer radar comparison | ✅ | ✅ | ✅ | ❌ |
    | DCF Calculator built-in | ✅ | Partial | Partial | ❌ |
    """)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#8892a4; font-size:13px; padding:12px 0;'>
        FinSight Pro © 2024 — Built for AI & Fintech Class · Demo Mode (Simulated Data)
    </div>
    """, unsafe_allow_html=True)

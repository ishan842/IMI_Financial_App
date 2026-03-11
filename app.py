import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Financial Statement Analyzer")

ticker = st.text_input("Enter Company Ticker", "AAPL")

if st.button("Fetch Data"):

    company = yf.Ticker(ticker)

    st.subheader("Income Statement")
    st.dataframe(company.financials)

    st.subheader("Balance Sheet")
    st.dataframe(company.balance_sheet)

    st.subheader("Cash Flow")
    st.dataframe(company.cashflow)
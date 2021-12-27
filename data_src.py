import yfinance as yf
import pandas as pd
import streamlit as st

class DataSource:
    def __init__(self, maxDays):
        # components: tickers and df, assign keys to states 
        if "tickers" not in st.session_state:
            st.session_state.tickers = {
                'apple': 'AAPL',
                'facebook': 'FB',
                'google': 'GOOGL',
                'microsoft': 'MSFT',
                'netflix': 'NFLX',
                'amazon': 'AMZN'
            }
            
        if "df" not in st.session_state:
            st.session_state.df = pd.DataFrame()
        self.maxDays = maxDays
        
    def _get_data(self, companies):
        for company in companies:
            # check whether visited, if yes, continue
            if company not in st.session_state.tickers:
                continue
            # load data
            tkr = yf.Ticker(st.session_state.tickers[company])
            hist = tkr.history(period=f'{self.maxDays}d')
            # store data in state(dataFrame)
            if st.session_state.df.empty:
                st.session_state.df = pd.DataFrame({
                    company: list(hist["Close"])}, 
                    # assign date as indexes
                    index = hist.index.strftime('%Y-%m-%d')
                )
            else:
                st.session_state.df[company] = list(hist["Close"])
            # mark the visited company reversely
            del st.session_state.tickers[company]
    
    
    
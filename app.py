import pandas as pd
import altair as alt
import streamlit as st
from sidebar import Sidebar
from data_src import DataSource

class App:
    # initialize the parameters of main page's display condition control
    if "error" not in st.session_state:
        st.session_state.error = 0
    if "showData" not in st.session_state:
        st.session_state.showData = 0
        
    def __init__(self, maxDays=50):
        self.tickers = {
            'apple': 'AAPL',
            'facebook': 'FB',
            'google': 'GOOGL',
            'microsoft': 'MSFT',
            'netflix': 'NFLX',
            'amazon': 'AMZN'
        }

        self.sidebar = Sidebar(self.tickers, maxDays)
        self.data = DataSource(maxDays)
        
        # use this func control the rerun main page
        self._display_main()
        # use confirm button to show data or error message
        st.sidebar.button("確認", on_click=self._check_button)
    
    def _display_main(self, 
                     error=st.session_state.error,
                     showData=st.session_state.showData):
        
        st.title('米国GAFA株価トレンド')
        if not showData:
            st.write('会社名と日数を選んで、"確認"  ボタンをクリックしください')
            st.write(f"### 過去 ?? 日間")
        else:
            st.write(f"### 過去**{st.session_state.days}日間**")
        if error:
            st.error('会社名か日数を選んでいません')
            st.session_state.error = 0
        if showData:
            self.data._get_data(st.session_state.companies)
            self._display_data()
            
            # restart a new session
            st.write('また会社名と日数を選んで、"確認"  ボタンをクリックしてください')
            st.session_state.showData = 0
                
    def _check_button(self):
        if not(st.session_state.companies and st.session_state.days):
            st.session_state.error = 1
        else:
            st.session_state.showData = 1
        
    def _display_data(self):
        current_frame = self._get_current_frame()
        st.write("##### 各社株価データ(USD)") 
        with st.expander(""):
            st.table(current_frame.style.format("{:.2f}"))
        st.write("##### 各社株価トレンド")
        with st.expander(""):
            # streamlit version is not ideal
            # st.line_chart(current_frame)
            self._display_plot(current_frame)
    
    def _get_current_frame(self):
        df = st.session_state.df
        companies = st.session_state.companies
        recentDays = -st.session_state.days        
        return df.loc[:,companies][recentDays:]
    
    def _display_plot(self, current_frame):
        # make index date to column
        current_frame = current_frame.reset_index()
        # make companies' names to one column
        current_frame = current_frame.melt(
            id_vars=['Date'], 
            value_vars=st.session_state.companies,
            var_name='Company Name',
            value_name='Stock Prices (USD)'
        )
        
        # set y-axis range
        ymax = ((current_frame['Stock Prices (USD)'].max() // 500)+1) * 500
        ymin = (current_frame['Stock Prices (USD)'].min() // 500) * 500
        
        chart = (
            alt.Chart(current_frame).
            mark_line(opacity=0.8, clip=True).
            encode(
                x="Date:T",
                y=alt.Y("Stock Prices (USD):Q", 
                        scale=alt.Scale(domain=[ymin, ymax])),
                color='Company Name:N'
            )
        )
        
        st.altair_chart(chart, use_container_width=True)

if __name__ == '__main__':
    app = App()


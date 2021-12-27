import streamlit as st

class Sidebar:
    def __init__(self, tickers, maxDays):
        # components, assign keys to store states          
        st.sidebar.multiselect(
            '会社名',
            list(tickers.keys()),
            ['google', 'amazon'],
            key="companies"
        )

        st.sidebar.slider(
            '日数', 0, maxDays, 10, 10,
            key="days"
        )
        
        # sidebar style: control the width
        sidebar_width = 10
        st.markdown(f'''
                    <style>
                        section[data-testid="stSidebar"] 
                        .css-ng1t4o {{width: {sidebar_width}rem;}}
                    </style>
                    ''',
                    unsafe_allow_html=True)

                    

        
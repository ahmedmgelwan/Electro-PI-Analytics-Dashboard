import pandas as pd
import streamlit as st
from utils import conn
import warnings

warnings.filterwarnings('ignore')

conn = conn
st.set_page_config(page_title='Electro PI Dashboard',
                    page_icon='📊',
                    layout='centered'
                    )
st.title('📔Electro PI Analysis')
st.write('*Dashboard for Tracking & Analysis All Company Projects* 🧑🏻‍💻')


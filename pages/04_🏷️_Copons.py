import streamlit as st
from utils import conn
import plotly.express as px
import pandas as pd

conn = conn
st.title('Copons')
@st.cache_data
def get_copons():
    copons = pd.read_sql(
        sql='SELECT copon_code, users, (max_users - users) AS remaining, disount_rate FROM copons /*WHERE `users` > 0*/ ORDER BY users DESC;',
        con=conn
    )
    return copons
copons = get_copons()
col_1,col_2,col_3 = st.columns(3)
col_1.metric('Number of Copons',copons['copon_code'].count())
col_2.metric('Number of using copons',copons['users'].sum())
col_3.metric('Max discount rate',copons['disount_rate'].max())

col_1 , col_2 = st.columns(2)
with col_1:
    st.subheader('Copons Usages')
    fig = px.pie(
        data_frame=copons,
        names = 'copon_code',
        values = 'users',
        hole=0.2,
        hover_data=['remaining','disount_rate'],
        # title='## Used Copons'
    )
    fig.update_traces(
        textposition='inside',
        textinfo='label+value',
        showlegend=False
    )
    st.plotly_chart(fig,use_container_width=True)
with col_2:
    st.subheader('Most Used Copons')
    st.dataframe(copons.head(10))
import streamlit as st
from utils import *

conn = conn
st.title('Bundles')
date_item = get_date_item()
if date_item:
    bundles = load_table('bundles',['bundle_id','bundle_name'],'creation_date',date_item,_con=conn )
    bundles_fillter = date_fillter(bundles,date_item,'count','bundles-fillter')
    if bundles_fillter[0]:
        st.write(f'__Number of bundles in {bundles_fillter[0]} is `{bundles_fillter[1]}`__')    
    fig = plot(bundles,date_item,'bar','bundle_name')
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(bundles,use_container_width=True)
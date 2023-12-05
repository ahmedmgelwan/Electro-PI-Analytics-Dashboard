import streamlit as st
from utils import *

conn = conn
st.title('🧑🏻‍💻 Admins')
date_item = get_date_item()
if date_item:
    admin_capstones = load_table(
        table = 'capstone_evaluation_history',
        col_name = ['lesson_id','admin_id'],
        dt_col = 'evaluation_date',
        date_item = date_item
    )
    admin_capstones_fillter = date_fillter(admin_capstones,date_item,'count','admin-caps-fillter',True)
    if admin_capstones_fillter[0]:
        col_1, col_2 = st.columns(2)
        with col_1:
            st.subheader(f'Admins Evalution General Pattern for {date_item}')
            fig = plot(admin_capstones,date_item,'line',color='admin_id')
            st.plotly_chart(fig,use_container_width=True)
        with col_2:
            st.subheader(f'Evalution for {admin_capstones_fillter[0]}')
            fig_2 = plot(admin_capstones_fillter[1],date_item,'pie',color='admin_id')
            fig_2.update_traces(
                                textposition='inside',
                                textinfo='label+value+percent',
                            )
            st.plotly_chart(fig_2,use_container_width=True)
        st.dataframe(admin_capstones_fillter[1].reset_index(drop=True),width=500)


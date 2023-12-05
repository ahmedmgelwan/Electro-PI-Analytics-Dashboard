import streamlit as st
from utils import db_conn,get_date_item,get_search_id,table_search
import pandas as pd
conn,cursor = db_conn()

cursor.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")

st.title('🤝10k AI initiative')

@st.cache_data
def get_initiative_data():
    initiative = pd.read_sql(
        sql='select * from initiative;',con=conn
    )
    return initiative

initiative = get_initiative_data()
col_1, col_2 = st.columns(2)

initiative_users_count = pd.read_sql(
    sql = 'select count(user_id) from initiative;',con=conn
)
col_1.metric('No. of Initiative Users',initiative_users_count.values)
initiative_completed_courses = pd.read_sql(
    sql = 'select sum(completed_courses) from initiative;',con=conn
)
col_2.metric('No of Completed Courses',int(initiative_completed_courses.values))
col_1, col_2 = st.columns(2)
with col_1:
    st.subheader('🏆 Top 10 10k AI Initiative Users')
    st.dataframe(initiative.head(10))
with col_2:
    st.subheader('📢 Least 10 Completed Courses')
    st.dataframe(initiative.sort_values(by='last_completion_date',ascending=False).head(10).reset_index())
user_id = get_search_id('enter user id','Enter initiative user id to get its info','user-id-10k')
initiative_search = table_search(user_id,initiative,'user_id')
st.dataframe(initiative_search)


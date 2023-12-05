import streamlit as st
from utils import *
import pandas as pd
import plotly.express as px

st.title('Employment Grant')
sql = '''
SELECT
    u.user_id,
    u.fresh_grad,
    u.education_title,
    u.military_status,
    u.ability_to_travel,
    u.avilable_city_to_travel,
    u.work_remotly,
    u.full_time,
    u.english_level,
    u.status AS current_status,
    u.application_date,
    e.submitted,
    e.preparation,
    e.pending,
    e.hold,
    e.inreview,
    e.shortlisted,
    e.postponed,
    e.accepted
FROM
    users_employment_grant u
LEFT JOIN
    users_employment_grant_actions e ON u.user_id = e.user_id
ORDER BY
    u.user_id

'''
grant = pd.read_sql(sql,conn)
user_id = get_search_id('Enter user id','Enter use_id to get its grant info','grant')
grant_result = table_search(user_id,grant,'user_id','grant')
st.dataframe(grant_result)
st.subheader('Sattuses')
for col in grant.drop(columns='user_id').columns:
    st.write(f'__{col.replace("_", " ").title()}__')
    try:
        col_vcount = (grant[col].apply(lambda x: x.title().strip())).value_counts()
        fig = px.pie(col_vcount, names=col_vcount.index, values=col)
        st.plotly_chart(fig)
    except:
        col_vcount = (grant[col]).value_counts()
        fig = px.line(col_vcount, x=col_vcount.index, y=col)
        st.plotly_chart(fig)
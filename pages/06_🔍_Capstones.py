import streamlit as st
from utils import *

conn = conn
st.title('Capstones')
sql = '''
SELECT
    capstone_evaluation_history.user_id,
    capstone_evaluation_history.course_id,
    capstone_evaluation_history.chapter_id,
    capstone_evaluation_history.lesson_id,
    capstone_evaluation_history.evaluation_date,
    capstone_evaluation_history.degree,
    capstones.`lock`,
    capstones.last_submission_date,
    capstones.reviewed,
    capstones.revision_date
FROM
    capstone_evaluation_history
JOIN
    capstones USING (course_id, chapter_id, lesson_id)
ORDER BY evaluation_date DESC;
'''
capstones_info = pd.read_sql(sql=sql,con=conn)
user_id = get_search_id('user id','Enter user_id to get its all capstones data','capstones-info-search')
capstones_info_search = table_search(user_id,capstones_info,'user_id')
st.dataframe(capstones_info_search)



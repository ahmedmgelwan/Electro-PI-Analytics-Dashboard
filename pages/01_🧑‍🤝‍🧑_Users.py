from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st
from utils import *

conn, cursor = conn, cursor
cursor.execute(
        "SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));"
    )
st.title('Users Analysis')
tab_1, tab_2 = st.tabs(['New Users', 'Current Users'])

with tab_1:
    date_item = get_date_item()
    col_1, col_2 = st.columns(2)
    if date_item:
        reg_data = load_table('users', 'user_id', 'registration_date', date_item,conn)
        sub_data = load_table('users', 'user_id', 'subscription_date', date_item,conn)
        
        with col_1:

            st.header('Registrations')
            reg_date_fillter = date_fillter(reg_data,date_item,'count','reg-fillter')
            
            if reg_date_fillter[0]:
                st.metric('New Registrations',reg_date_fillter[1])
                # st.write(f'__Number of registered users in {reg_date_fillter[0]} is `{reg_date_fillter[1]}`__')
            reg_fig = plot(reg_data, date_item) 
            st.plotly_chart(reg_fig, use_container_width=True)


        with col_2:
            st.header('Subscriptions')
            sub_date_fillter = date_fillter(sub_data,date_item,'count','sub-fillter')
            if sub_date_fillter[0]:
                st.metric('New Subscriptions',sub_date_fillter[1])
                # st.write(f'__Number of registered users in {sub_date_fillter[0]} is `{sub_date_fillter[1]}`__')
            sub_fig = plot(sub_data, date_item)  
            st.plotly_chart(sub_fig, use_container_width=True)

with tab_2:
    st.subheader('Users Info')
    
    user_info = pd.read_sql(
        sql='''
            select 
                user_id, 
                bundle_name,
                count(user_courses.course_id) current_courses,
                completed_courses,
                last_degree,
                last_completion_date
                 
            from 
                users 
                join bundles using(user_id) 
                join user_new_completed_course using(user_id) 
                join user_courses using(user_id) 
            group by 
                users.user_id ;
        ''',
        con=conn
    )
    user_id = get_search_id('user id','Enter user id  to get its all info like bundle, courses, quizzes,..., etc','users-info-search')
    user_info_search = table_search(user_id,user_info,'user_id')
    st.dataframe(user_info_search)
    st.divider()
    st.subheader('Users Courses')
    date_item = get_date_item('course-completion-dt-item')
    if date_item:
        col_1, col_2 = st.columns(2)
        with col_1:
            user_courses = pd.read_sql(
                sql='select user_id, count(course_id) user_courses from user_courses group by user_id order by user_courses desc;',
                con=conn
            )
            users_courses_fig = px.bar(user_courses['user_courses'],x='user_courses',title='Users Registred Courses [Count]')
            users_courses_fig.update_layout(xaxis_title='No. of courses',yaxis_title='No. of users Distribution')
            st.plotly_chart(users_courses_fig,use_container_width=True)


        with col_2:
            
                user_completed_courses = load_table('user_completed_courses',['course_id','user_id'],'completion_date',date_item,conn)
                
                user_completed_courses_fig = plot(user_completed_courses.drop(columns='user_id'),date_item,'bar',title='Users completed courses distrubution')
                st.plotly_chart(user_completed_courses_fig,use_container_width=True)
        

    st.divider()
    # ---------------------Grouping by age ----------
    st.subheader('Users Ages & Degrees Analysis')
    users_age_degree = pd.read_sql(
        sql = '''
        SELECT
            age, study_degree, count(user_id) count 
            FROM users 
            GROUP BY age, study_degree 
            ORDER BY `count` DESC;
        ''',
        con=conn
    )
    users_age_degree_fig = plot(users_age_degree,'age','bar','study_degree','Users Ages vs Degrees')
    user_age = get_search_id('Enter age','Enter age to get number of users age and study degree','age and study degree')
    users_age_degree_search = table_search(user_age,users_age_degree,'age','age and study degree')
    col_1, col_2 = st.columns(2)
    col_1.dataframe(users_age_degree_search)
    col_2.plotly_chart(users_age_degree_fig,use_container_width=True)
    col_1, col_2 = st.columns(2)
    with col_1:
        users_ages_fig = px.bar(users_age_degree,x='age',y='count',title='Users Ages')
        st.plotly_chart(users_ages_fig,use_container_width=True)
    with col_2:
        users_degrees_fig = px.pie(
            users_age_degree,values='count',names='study_degree',title='Users Degrees'
        )
        users_degrees_fig.update_traces(
        textposition='inside',
        textinfo='label+value+percent',
        showlegend=False
    )
        st.plotly_chart(users_degrees_fig,use_container_width=True)
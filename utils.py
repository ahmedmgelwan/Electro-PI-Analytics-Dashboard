import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Create a connection to the MySQL server

def db_conn():
    _ = load_dotenv()
    conn = mysql.connector.connect(host=os.getenv('HOST'),
                                database=os.getenv('DATABASE'),
                                user=os.getenv('USER'),
                                password=os.getenv('PASSWORD'),
                                )
    cursor = conn.cursor()
    return conn, cursor
conn,cursor = db_conn()



def get_date_item(key=None):
    date_items_dict = {'Daily': 'DATE',
                        'Weekly': 'YEARWEEK',
                       'Monthly': 'MONTH',
                       'Yearly': 'YEAR',
                       }
    date_item = st.selectbox('Choose date item', 
                            date_items_dict.keys(),
                            index=None,
                            key=key
                            )
    if date_item:
        return date_items_dict[date_item]

@st.cache_data
def load_table(table, col_name, dt_col, date_item,_con=conn):
    if not _con.is_connected():
        _con.connect()

    if isinstance(col_name,str):
        q = f'SELECT {date_item}({dt_col}) AS {date_item}, COUNT({col_name}) AS count FROM {table} WHERE {date_item}({dt_col}) IS NOT NULL GROUP BY {date_item}({dt_col}) ORDER BY count DESC; ORDER BY count DESC;'
    elif isinstance(col_name,list):
        q = f'SELECT {date_item}({dt_col}) AS {date_item}, {col_name[1]},COUNT({col_name[0]}) AS count FROM {table} WHERE {date_item}({dt_col}) IS NOT NULL GROUP BY {date_item}({dt_col}), {col_name[1]} ORDER BY count DESC;'
    
    data = pd.read_sql(sql=q, con=_con)
    
    if date_item == 'DATE':
        data[date_item] = pd.to_datetime(data[date_item]).dt.date
    return data

@st.cache_data
def plot(data, date_item, chart='line',color=None,title=None):  
    data.sort_values(by=date_item, inplace=True)
    try:
        charts = {
            'line': px.line(data, x=date_item, y='count', color=color,title=title),
            'bar': px.bar(data, x=date_item, y='count', color=color,barmode='group',title=title),
            'pie': px.pie(data, names=color, values='count',title=title)
        }
    except Exception as e:
        return e

    fig = charts.get(chart, px.line(data, x=date_item, y='count', color=color))  # Default to line chart
    if chart in ['line', 'bar']:
        fig.update_layout(
            xaxis_title=date_item, yaxis_title="Count"
        )
    return fig


def date_fillter(data,date_item,col_name='count',key=None,full_table=False):
    dt_col = data[date_item]
    if date_item == 'DATE':
        fillter_option = st.date_input('Choose Date',dt_col.max(),min_value=dt_col.min(),max_value=dt_col.max(),key=key)
    
    else:
        fillter_option = st.selectbox(f'Choose {date_item}:',options=set(dt_col.to_list()),index=None,key=key+'select')
    if full_table:
        return fillter_option, data[dt_col == fillter_option]
    try:
        result = data[dt_col == fillter_option][col_name].values[0]
    except IndexError:
        result = 0

    return fillter_option, result

def get_search_id(label,placeholder,key=None):
    user_id = st.number_input(
        f'{label.title()}:',
        placeholder=placeholder,
        value=None,
        step=1,
        key=key
    )
    return user_id
@st.cache_data
def table_search(user_id,table,col,tag=None):
    if user_id:
        return ((table.query(f'{col} == {user_id}')).reset_index(drop=True))
    else:
        return table


import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import write_pandas
from pages import Connect_Db

class load_data():
    
    def app(self):
        st.subheader("Load CSV")
        csv_file = st.file_uploader("Upload file", type=["csv"])

        if csv_file is not None:

            # To See details
            file_details = {"filename":csv_file.name, "filetype":csv_file.type,
                          "filesize":csv_file.size}

            try:
                
                load_df = pd.read_csv(file_details['filename'])
                load_df = load_df[['DATE', 'DESCRIPTION', 'ORIGINAL_DESCRIPTION', 'AMOUNT',
           'TRANSACTION_TYPE', 'CATEGORY', 'ACCOUNT_NAME', 'LABELS', 'NOTES']]
                #st.write('hello')
                load_df['DATE'] = [i.replace("'",'') for i in load_df['DATE']]
                load_df['DESCRIPTION'] = load_df['DESCRIPTION'].str.replace("'",'')
                load_df['ORIGINAL_DESCRIPTION'] = load_df['ORIGINAL_DESCRIPTION'].str.replace("'",'')
                load_df['ACCOUNT_NAME'] = load_df['ACCOUNT_NAME'].str.replace("'",'')
                load_df['TRANSACTION_TYPE'] = [i.replace("'",'') for i in load_df['TRANSACTION_TYPE']]
                load_df['CATEGORY'] = [i.replace("'",'') for i in load_df['CATEGORY']]
                load_df = load_df.fillna('NA')
                st.write(load_df)
                try:
                    #st.write('i got here')
                    conn = Connect_Db.connectdb()
                    cur = conn.cursor()

                    cur.execute('select * FROM SAMPLE2 ORDER BY INDEX DESC LIMIT 1')
                    d = cur.fetchall()
                    if len(d) <1:
                        last_index = -1
                    else:
                        last_index = d[0][-1]
                    rge = load_df.shape[0]

                    load_index = []
                    for k in range(rge):
                        idx = int(last_index) + 1
                        load_index.append(str(idx))
                        last_index = idx

                    load_df['INDEX'] = load_index

                    write_pandas( conn,load_df,'SAMPLE2',database='TEST',schema='PUBLIC')

                    st.write('Data Has been added')


                    df = pd.read_sql('select * from SAMPLE1',conn)
                    conn.close()
                    df['DATE'] = [str(i).split(' ')[0] for i in df['DATE']]
                    df = df[df.columns[1:]]
                    #st.write(df)
                except:
                    st.write('error connecting to database')

            except:
                    st.write('An error occured, file doesnt match or table does not exists or the file is not the working directory')
        
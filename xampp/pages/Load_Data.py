import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
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
                    conn = Connect_Db.connectdb()
                    cur = conn.cursor()

                    for l in load_df.values:
                        #st.write('hello')
                        val = list(l)
                        val = str(val).replace('[','(').replace(']',')')
                        query = f"INSERT INTO sample1 (`DATE`, `DESCRIPTION`, `ORIGINAL_DESCRIPTION`, `AMOUNT`, `TRANSACTION_TYPE`, `CATEGORY`, `ACCOUNT_NAME`, `LABELS`, `NOTES`) VALUES{val}"
                        #st.write(query)
                        cur.execute(query)
                        conn.commit()

                    st.write('Data Has been added')
                    conn.close()
                except:
                    st.write('error connecting to the database')

            except:
                    st.write('An error occured, file doesnt match or table does not exists or the file is not the working directory')
        
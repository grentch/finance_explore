import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from pages import Connect_Db

class edit_data():
    
    def app(self):
        st.subheader("Edit CSV")
        try:
            #st.write('fxfgcgf')
            conn = Connect_Db.connectdb()

            df = pd.read_sql('select * from SAMPLE1',conn)
            conn.close()

            #preprocess the columns
            df['CATEGORY'] = df['CATEGORY'].str.replace("'",'')
            df['TRANSACTION_TYPE'] = df['TRANSACTION_TYPE'].str.replace("'",'')
            df['DESCRIPTION'] = df['DESCRIPTION'].str.replace("'",'')
            df['ORIGINAL_DESCRIPTION'] = df['ORIGINAL_DESCRIPTION'].str.replace("'",'')
            df['ACCOUNT_NAME'] = df['ACCOUNT_NAME'].str.replace("'",'')
            df['AMOUNT'] = df['AMOUNT'].astype(float)

            #list to hold unique categories in the data
            categories = [] 

            #list to hold unique transaction type in the data
            transact_type = []

            #insert into category list
            for j in df['CATEGORY'].unique():
                categories.append(j)

            #insert into transaction type list
            for j in df['TRANSACTION_TYPE'].unique():
                transact_type.append(j)

            #st.write(df.columns)
            index = st.text_input("Enter the index/row number of the data you want to edit")
            col1, col2, col3, col4= st.columns(4)

            with col1:
                date = st.text_input("Enter your date (mm/dd/yyyy)")
            with col2:
                amount = st.text_input("Enter the amount")
            with col3:
                trans_type = st.text_input("Enter the transaction type")
            with col4:
                category_name = st.text_input("Enter the category name")

            apply = st.button('Apply') 

            if apply:
                #st.write('fgf')
                flag = []
                try:
                    datetime.datetime.strptime(date, '%m/%d/%Y')
                except:
                    flag.append(False)
                    st.write('date not in right format')
                try:
                    float(amount)
                except:
                    flag.append(False)
                    st.write('amount not in right format')

                ttype = [trans_type in transact_type]
                if ttype[0]==True:
                    #st.write(trans_type, 'is in right format')
                    pass
                else:
                    flag.append(False)
                    st.write('transact_type not in right format')

                ttype = [category_name in categories]
                if ttype[0]==True:
                    pass
                    #st.write(category_name, 'is in right format')
                else:
                    flag.append(False)
                    st.write('category_name not in right format')

                if len(flag) == 0:
                    try:
                        conn = Connect_Db.connectdb()
                       
                        #st.write(cur.fetchone())
                        query = f"UPDATE sample1 SET `DATE` = '{date}', `AMOUNT` = {amount}, `TRANSACTION_TYPE` = '{trans_type}', `CATEGORY` = '{category_name}' WHERE id = {index}"
                        #st.write(query)
                        cur = conn.cursor()
                        cur.execute(query)
                        #pd.read_sql(query,conn)
                        conn.commit()
                        conn.close()
                        st.write('Update has been made to the database')
                    except:
                        st.write("index not exist")
        except:
            st.write('probably issue with the database connection')
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from pages import Connect_Db,table

class explore_raw():
    def get_month_difference(self):
        month = self.month
        yar = self.yar
        df = self.df
        
        if month ==1:
                last_month = 12
                last_month_year = yar - 1
        else:
            last_month = month - 1
            last_month_year = yar 

        last_date_start = datetime.datetime.strptime(str(last_month_year) +'-' + str(last_month) + '-'+'01', '%Y-%m-%d')
        #st.write('last_date_start ',last_date_start)
        if last_month==2:
            try:
                last_date_end = datetime.datetime.strptime(str(last_month_year) +'-' + str(last_month) + '-'+'29', '%Y-%m-%d')
            except:
                last_date_end = datetime.datetime.strptime(str(last_month_year) +'-' + str(last_month) + '-'+'28', '%Y-%m-%d')
        else:
            try:
                last_date_end = datetime.datetime.strptime(str(last_month_year) +'-' + str(last_month) + '-'+'31', '%Y-%m-%d')
            except:
                last_date_end = datetime.datetime.strptime(str(last_month_year) +'-' + str(last_month) + '-'+'30', '%Y-%m-%d')   
        #st.write('last_date_end ',last_date_end)
        
        lastest_month_df =  df[(df['DATE'] > self.current_date_start) & (df['DATE'] <= self.current_date_end)]
        last_month_df =  df[(df['DATE'] > last_date_start) & (df['DATE'] <= last_date_end)]
        
        
        return lastest_month_df,last_month_df
    
    def get_current_date_end(self):
        
        month = self.month
        yar = self.yar
        if month==2:
            try:
                current_date_end = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'29', '%Y-%m-%d')
            except:
                current_date_end = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'28', '%Y-%m-%d')
        else:
            try:
                current_date_end = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'31', '%Y-%m-%d')
            except:
                current_date_end = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'30', '%Y-%m-%d')

        return current_date_end
        
    def get_unique_year(self):
        year = []
        df = self.df
        for i in df.Year.unique():
            yaer = str(i)
            if yaer != 'nan':
                year.append(int(float(yaer)))
        year = tuple(sorted(year))
        return year
    
    def five_months(self):
        month = self.month
        selected_year = self.selected_year
        yar = self.yar
        yre = self.yar
        
        five_months = [[month,selected_year] ]
        for i in range(4):
            if month == 1:
                month = 12
                yre = int(yar) - 1
            else:
                month = month - 1
                yre = yre 
            five_months.append([month,yre])
        if month <10:
            month = '0'+str(month)

        return five_months,yre
    
    def app(self):
        st.write('Explore Raw Data Page')
        try:
            
            conn = Connect_Db.connectdb()
            
            cur = conn.cursor()
            table_name = table.table()
            query = f'select * from {table_name}'
            #st.write('vjgj')
            cur.execute(query)

            names = [ x[0] for x in cur.description]
            rows = cur.fetchall()
            #st.write('hbbfb')
            self.df = pd.DataFrame( rows, columns=names)
            conn.close()
            #preprocess the columns
            self.df['CATEGORY'] = self.df['CATEGORY'].str.replace("'",'')
            self.df['TRANSACTION_TYPE'] = self.df['TRANSACTION_TYPE'].str.replace("'",'')
            self.df['DESCRIPTION'] = self.df['DESCRIPTION'].str.replace("'",'')
            self.df['ORIGINAL_DESCRIPTION'] = self.df['ORIGINAL_DESCRIPTION'].str.replace("'",'')
            self.df['ACCOUNT_NAME'] = self.df['ACCOUNT_NAME'].str.replace("'",'')
            self.df['AMOUNT'] = self.df['AMOUNT'].astype(float)

            #list to hold unique categories in the data
            self.categories = [] 

            #list to hold unique transaction type in the data
            self.transact_type = []

            #insert into category list
            for j in self.df['CATEGORY'].unique():
                self.categories.append(j)
            #st.write(categories)
            #insert into transaction type list
            for j in self.df['TRANSACTION_TYPE'].unique():
                self.transact_type.append(j)

            #convert the date column to  a datetime object
            self.df['DATE'] = pd.to_datetime(self.df['DATE'],errors="coerce")
            #extract month, day , year into seperate columns
            self.df['Month'] = self.df['DATE'].dt.month
            self.df['Day'] = self.df['DATE'].dt.day
            self.df['Year'] = self.df['DATE'].dt.year

            #gets the unique year in the data for the dropdown

            # Text/Title
            #st.title("Interactive Dashboard")
            self.year = self.get_unique_year()

            #year select box    
            self.selected_year = st.selectbox(
                 'Select Year:',
                 self.year)
            
            self.yer =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec']
            
            #month slider
            self.selected_month = st.select_slider(
             'Select year',
             options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec'])
            self.cate = st.multiselect('Select One or more category', self.categories)

            #add to add one because python list starts at index 0, so Dec would be 11 if 1 isnt added
            self.month = self.yer.index(self.selected_month)+1

            #st.write('Month')
            #st.write(month)
            #another variable to hold the selected year

            self.yar = self.selected_year

            current_date_start = datetime.datetime.strptime(str(self.yar) +'-' + str(self.month) + '-'+'01', '%Y-%m-%d')
            current_date_end = self.get_current_date_end()
            
            if self.cate:
                self.new_df = self.df[self.df['CATEGORY'].isin(self.cate)]
            else:
                self.new_df = self.df
            self.new_df = self.new_df[(self.new_df['DATE'] > current_date_start) & (self.new_df['DATE'] <= current_date_end)].sort_values(by='AMOUNT',ascending=False)
            self.new_df['DATE'] = [str(i).split(' ')[0] for i in self.new_df['DATE']]
            self.new_df = self.new_df[['DATE','DESCRIPTION','ORIGINAL_DESCRIPTION','AMOUNT','TRANSACTION_TYPE','CATEGORY','ACCOUNT_NAME','LABELS','NOTES']]
            st.write('Click on the column to sort by that column')
            st.write(self.new_df)

        except:
            st.write('error connecting to database')
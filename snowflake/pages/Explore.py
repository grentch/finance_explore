import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from pages import Connect_Db

class explore_page():
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
        st.write('Explore Page')
        #st.write('app was called')
        try:
            conn = Connect_Db.connectdb()
            self.df = pd.read_sql('select * from SAMPLE2',conn)
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
            #st.write(self.categories)
            #insert into transaction type list
            for j in self.df['TRANSACTION_TYPE'].unique():
                self.transact_type.append(j)

            #convert the date column to  a datetime object
            self.df['DATE'] = pd.to_datetime(self.df['DATE'],errors="coerce")
            #extract month, day , year into seperate columns
            self.df['Month'] = self.df['DATE'].dt.month
            self.df['Day'] = self.df['DATE'].dt.day
            self.df['Year'] = self.df['DATE'].dt.year
            
            self.yer =  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec']
            #gets the unique year in the data for the dropdown
          
            self.year = self.get_unique_year()
            
            self.cate = st.multiselect('Select One or more category', self.categories)
            
            self.selected_year = st.selectbox(
                 'Select Year:',
                 self.year)

            self.selected_month = st.select_slider(
             'Select a color of the rainbow',
             options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec'])

            self.month = self.yer.index(self.selected_month)+1


            self.yar = self.selected_year
            
            five_months,yre = self.five_months()

            start_date = self.get_current_date_end()
            #st.write(start_date)
            end_date = datetime.datetime.strptime(str(five_months[-1][-1]) +'-' +str(five_months[-1][-0]) + '-'+'01', '%Y-%m-%d')
            
            try:
                new_df = self.df[self.df['CATEGORY'].isin(self.cate)]
                page_mask = new_df[(new_df['DATE'] > end_date) & (new_df['DATE'] <= start_date)]
                page_mask = page_mask[page_mask['TRANSACTION_TYPE']=='debit']

                page_mask = page_mask[['Month','Year','AMOUNT','CATEGORY']]

                page_mask['Month'] = page_mask['Month'].astype("Int64")
                page_mask['Year'] = page_mask['Year'].astype("Int64")

                combined_date = [ ]

                two = page_mask[['Month','Year']].copy()
                two = two.values.tolist()

                for i,j in two:
                    combined_date.append(f'{self.yer[i-1]} {j}')
                page_mask['period'] = combined_date

                page_mask = page_mask[['period','AMOUNT','CATEGORY']]
                #st.write(page_mask)
                dff = page_mask.groupby(['period','CATEGORY']).sum().reset_index()

                idx_month = []

                idx_year = []

                for i in dff['period']:
                    q = i.split()
                    idx_month.append(q[0])
                    idx_year.append(q[1])

                dff['idx_month'] = idx_month

                dff['idx_year'] = idx_year

                dff.idx_month = dff.idx_month.astype('category')
                dff.idx_month.cat.set_categories(self.yer,inplace=True)                                         

                dff = dff.sort_values(by=['idx_year','idx_month'],ascending=[True,True])
                fig = px.bar(dff, x="period", y="AMOUNT", color="CATEGORY", title="Sum Debit for the last 5 months")

                st.plotly_chart(fig, use_container_width=False, sharing="streamlit")
            except:
                if cate and selected_month:
                    st.write("No sufficient data for this period")
                else:
                    st.write("select a category and a year")

        except:
            st.write('error connecting to database')

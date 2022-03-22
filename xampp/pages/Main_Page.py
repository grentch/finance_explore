import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from pages import Connect_Db

class main_page():
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
        #st.write('app was called')
        try:
            conn = Connect_Db.connectdb()
            self.df = pd.read_sql('select * from SAMPLE1',conn)
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

            #add to add one because python list starts at index 0, so Dec would be 11 if 1 isnt added
            self.month = self.yer.index(self.selected_month)+1

            #st.write('Month')
            #st.write(month)
            #another variable to hold the selected year

            self.yar = self.selected_year

            #st.write('sleected year')
            #st.write(self.yar)
            #current start date

            self.current_date_start = datetime.datetime.strptime(str(self.yar) +'-' + str(self.month) + '-'+'01', '%Y-%m-%d')

            #st.write('current date start')
            #st.write(self.current_date_start)

            self.current_date_end = self.get_current_date_end()

            #st.write('current date end')
            #st.write(self.current_date_end)


            # Showing aggregations with the difference with the previous month
            #
            #st.write(current_date_end)
            lastest_month_df,last_month_df = self.get_month_difference()

            #st.write('lastest month df')
            #st.write(lastest_month_df)
            #st.write(last_month_df)

            col1, col2, col3, col4= st.columns(4)

            with col1:
                two_a = round(lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='credit']['AMOUNT'].sum(),2)
                last_two_a = round(last_month_df[last_month_df['TRANSACTION_TYPE']=='credit']['AMOUNT'].sum(),2)

                if last_two_a != 0.0:
                    difference = round(two_a-last_two_a,2)
                else:
                    difference = two_a
                st.metric(label='Total Credit',value=two_a,delta=f"{difference}")
            with col2:   
                two_b = lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='debit'].shape[0]
                last_two_b = last_month_df[last_month_df['TRANSACTION_TYPE']=='debit'].shape[0]
                difference = two_b - last_two_b
                st.metric(label='Total Number of Debit Transaction',value=two_b,delta=f"{difference}")
            with col3:
                two_c = lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='debit']['AMOUNT'].max()
                st.metric(label="Highest Debit", value=two_c)
            with col4:
                two_d = lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='debit']['AMOUNT'].mean()
                last_two_d = last_month_df[last_month_df['TRANSACTION_TYPE']=='debit']['AMOUNT']
                if last_two_d.shape[0] !=0:
                    met = round(two_d - last_two_d.mean(),2)
                else:
                    met = round(two_d,2)

                st.metric(label='Average Debit Transaction',value=round(two_d,2),delta=f"{met}")

            five_months,yre = self.five_months()

            start_date = self.get_current_date_end()
            #st.write(start_date)
            end_date = datetime.datetime.strptime(str(five_months[-1][-1]) +'-' +str(five_months[-1][-0]) + '-'+'01', '%Y-%m-%d')
            #st.write(end_date)
            try:

                mask = self.df[(self.df['DATE'] > end_date) & (self.df['DATE'] <= start_date)]
                #st.write(mask)
                mask = mask[mask['TRANSACTION_TYPE']=='debit'].sort_values(by='DATE')
                #st.write(mask)
                later_mask = mask[mask['Month']== self.yer.index(self.selected_month)+1]
                #st.write(later_mask)
                new_mask = mask[['Month','Year','AMOUNT']]
                new_mask['Month'] = new_mask['Month'].astype(int)
                new_mask['Year'] = new_mask['Year'].astype(int)

                combined_date = [ ]

                two = new_mask[['Month','Year']].copy()
                two = two.values.tolist()
                #st.write(two)
                for i,j in two:
                    #st.write(i,j)
                    combined_date.append(f'{self.yer[i-1]} {j}')
                #st.write(two)
                new_mask['period'] = combined_date
                new_mask = new_mask[['period','AMOUNT']]

                fd = new_mask.groupby(['period']).sum()

                dff = fd.groupby('period').sum().reset_index()

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

                dff = dff.sort_values(by=['idx_year','idx_month'])
                fig = px.bar(dff,'period','AMOUNT',title="Sum Debit for the recent 5 months completed months")
                st.plotly_chart(fig, use_container_width=False, sharing="streamlit")


                new_mask = mask[['CATEGORY','AMOUNT']]
                fd = new_mask.groupby(['CATEGORY']).sum().sort_values(by='AMOUNT',ascending=False).reset_index().head(10)
                fd = fd.sort_values(by=['AMOUNT'],ascending=False)
                fig = px.bar(fd,'CATEGORY','AMOUNT',title="Top 10 categories that had the highest Debit for the recent 5 months completed months")
                st.plotly_chart(fig, use_container_width=False, sharing="streamlit")

                new_mask = later_mask[['CATEGORY','AMOUNT']]
                fd = new_mask.groupby(['CATEGORY']).sum().sort_values(by='AMOUNT',ascending=False).reset_index().head(10)
                fd = fd.sort_values(by=['AMOUNT'],ascending=False)
                fig = px.bar(fd,'CATEGORY','AMOUNT',title="Top 10 categories that had the highest Debit for the chosen months")
                st.plotly_chart(fig, use_container_width=False, sharing="streamlit")

            except:
                st.write("No Sufficient Data for this period")


        except:
            pass


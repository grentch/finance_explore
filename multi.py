import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import sqlite3
import pymysql
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import sys

try:
    with open('env.txt','r') as r:
        details = r.read()

    details = eval(details)
except:
    sys.exit()
    
def connectdb():
    
#     connection =pymysql.connect(
#         user = 'root',
#         password = '',
#         db = 'test',
#         host = 'localhost',


#     )

    conn = snowflake.connector.connect(
                                 user= details['user'],
                                 password=details['password'],
                                 account=details['account'],
                                 database=details['database'],
                                 schema= details['schema']
                                )
    print("success in connecting", conn)
    return conn

st.set_page_config(page_title="page", layout="wide")

def get_current_date_end(month,yar):
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


def five_months(month,selected_year,yar):
    yre = yar
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
    

#months in a year, this list was created for indexing
yer = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec']

#read in csv, instead of querying the database
#df = pd.read_csv('sample1.csv')
try:
    conn = connectdb()
except:
    print('error connecting to database')
    sys.exit()
    
df = pd.read_sql('select * from SAMPLE1',conn)
conn.close()
#df = df[df.columns[1:]]
#extract the column names
col = df.columns
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

#convert the date column to  a datetime object
df[col[0]] = pd.to_datetime(df[col[0]],errors="coerce")

#extract month, day , year into seperate columns
df['Month'] = df[col[0]].dt.month
df['Day'] = df[col[0]].dt.day
df['Year'] = df[col[0]].dt.year

#drop columns that doesnt have value/interest
#df = df.drop(['DESCRIPTION', 'ORIGINAL_DESCRIPTION'],axis=1)

# #create bins
# bins = [0,10,20,30,40,50,60,70,80,90]
# df['binned'] = pd.cut(df[col[3]],bins)


#gets the unique year in the data for the dropdown
year = []
for i in df.Year.unique():
    yaer = str(i)
    if yaer != 'nan':
        year.append(int(float(yaer)))
year = tuple(sorted(year))

# Text/Title
st.title("Interactive Dashboard")


#menu sidebar
menu = st.sidebar.radio(
     'Select Menu:', ['Main','Explore Categories','Explore raw data','Load Data into Database','Edit Data'],index=0)


if menu == "Main":
    #year select box    
    selected_year = st.selectbox(
         'Select Year:',
         year)
    
    #month slider
    selected_month = st.select_slider(
     'Select a color of the rainbow',
     options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec'])
    
    #add to add one because python list starts at index 0, so Dec would be 11 if 1 isnt added
    month = yer.index(selected_month)+1
    
    #another variable to hold the selected year
    yar = selected_year
    
    #current start date
    current_date_start = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'01', '%Y-%m-%d')
    
    current_date_end = get_current_date_end(month,yar)
    
    #st.write(current_date_end)
    
    #
    # Showing aggregations with the difference with the previous month
    #
    #st.write(current_date_end)
    if month ==1:
        last_month = 12
        last_month_year = yar - 1
    else:
        last_month = month - 1
        last_month_year = yar 
        
    last_date_start = datetime.datetime.strptime(str(last_month_year) +'-' + str(last_month) + '-'+'01', '%Y-%m-%d')
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

    lastest_month_df =  df[(df['DATE'] > current_date_start) & (df['DATE'] <= current_date_end)]
    last_month_df =  df[(df['DATE'] > last_date_start) & (df['DATE'] <= last_date_end)]
    
    
    #st.write(difference)
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
        
    #gets the fifth month date
    if yar !="All":
        
        
        five_months,yre = five_months(month,selected_year,yar)
        
        #st.write(five_months)
        #st.write('i got here')
        start_date = get_current_date_end(yer.index(selected_month)+1,selected_year)
#         st.write(start_date)
#         start_date = datetime.datetime.strptime(str(selected_year) +'-' + str(yer.index(selected_month)+1) + '-'+'30', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(str(five_months[-1][-1]) +'-' +str(five_months[-1][-0]) + '-'+'01', '%Y-%m-%d')
        #st.write(start_date,end_date)
        
        try:
            mask = df[(df['DATE'] > end_date) & (df['DATE'] <= start_date)]
            #st.write(mask)
            mask = mask[mask['TRANSACTION_TYPE']=='debit'].sort_values(by='DATE')
            #st.write(mask)
            later_mask = mask[mask['Month']== yer.index(selected_month)+1]
            #st.write(later_mask)
            #st.write(later_mask)
            new_mask = mask[['Month','Year','AMOUNT']]
            new_mask['Month'] = new_mask['Month'].astype(int)
            new_mask['Year'] = new_mask['Year'].astype(int)
            
            
            combined_date = [ ]
            
            two = new_mask[['Month','Year']].copy()
            two = two.values.tolist()
            #st.write(two)
            for i,j in two:
                combined_date.append(f'{yer[i-1]} {j}')
                #print(combined_date)
            
            #print(combined_date)
            new_mask['period'] = combined_date
            new_mask = new_mask[['period','AMOUNT']]
            #st.write(new_mask)
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
            dff.idx_month.cat.set_categories(yer,inplace=True)                                         
                                             
            dff = dff.sort_values(by=['idx_year','idx_month'])
            fig = px.bar(dff,'period','AMOUNT',title="Sum Debit for the recent 5 months completed months")
            st.plotly_chart(fig, use_container_width=False, sharing="streamlit")

            #col1, col2 = st.columns(2)
            
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
        
        
if menu == "Explore Categories":
    cate = st.multiselect('Select One or more category', categories)
    selected_year = st.selectbox(
         'Select Year:',
         year)
    
    selected_month = st.select_slider(
     'Select a color of the rainbow',
     options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec'])
    
    month = yer.index(selected_month)+1
    
     
    yar = selected_year
  
    if yar !="All":
        five_months,yre = five_months(month,selected_year,yar)
        
        start_date = get_current_date_end(yer.index(selected_month)+1,selected_year)
        #start_date = datetime.datetime.strptime(str(selected_year) +'-' + str(yer.index(selected_month)+1) + '-'+'30', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(str(five_months[-1][-1]) +'-' +str(five_months[-1][-0]) + '-'+'01', '%Y-%m-%d')
        try:
            new_df = df[df['CATEGORY'].isin(cate)]
            page_mask = new_df[(new_df['DATE'] > end_date) & (new_df['DATE'] <= start_date)]
            page_mask = page_mask[page_mask['TRANSACTION_TYPE']=='debit']

            page_mask = page_mask[['Month','Year','AMOUNT','CATEGORY']]
            
            page_mask['Month'] = page_mask['Month'].astype("Int64")
            page_mask['Year'] = page_mask['Year'].astype("Int64")
            
            combined_date = [ ]
            
            two = page_mask[['Month','Year']].copy()
            two = two.values.tolist()
            
            for i,j in two:
                combined_date.append(f'{yer[i-1]} {j}')
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
            dff.idx_month.cat.set_categories(yer,inplace=True)                                         
                                             
            dff = dff.sort_values(by=['idx_year','idx_month'],ascending=[True,True])
            fig = px.bar(dff, x="period", y="AMOUNT", color="CATEGORY", title="Sum Debit for the last 5 months")
            
            st.plotly_chart(fig, use_container_width=False, sharing="streamlit")
        except:
            if cate and selected_month:
                st.write("No sufficient data for this period")
            else:
                st.write("select a category and a year")
if menu == "Explore raw data":
    selected_year = st.selectbox(
     'Select Year:',
     year)
    selected_month = st.select_slider(
     'Select a color of the rainbow',
     options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec'])
    
    cate = st.multiselect('Select One or more category', categories)
    
    month = yer.index(selected_month)+1
    
     
    yar = selected_year
    current_date_start = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'01', '%Y-%m-%d')
    current_date_end = get_current_date_end(month,yar)
    
    if cate:
        new_df = df[df['CATEGORY'].isin(cate)]
    else:
        new_df = df
    new_df = new_df[(new_df['DATE'] > current_date_start) & (new_df['DATE'] <= current_date_end)].sort_values(by='AMOUNT',ascending=False)
    new_df['DATE'] = [str(i).split(' ')[0] for i in new_df['DATE']]
    new_df = new_df[['DATE','DESCRIPTION','ORIGINAL_DESCRIPTION','AMOUNT','TRANSACTION_TYPE','CATEGORY','ACCOUNT_NAME','LABELS','NOTES']]
    st.write('Click on the column to sort by that column')
    st.write(new_df)
    
    
if menu =="Load Data into Database":
    
    st.subheader("Load CSV")
    csv_file = st.file_uploader("Upload file", type=["csv"])
    
    if csv_file is not None:

        # To See details
        file_details = {"filename":csv_file.name, "filetype":csv_file.type,
                      "filesize":csv_file.size}
        
        
        load_df = pd.read_csv(file_details['filename'])
        load_df['DATE'] = [i.replace("'",'') for i in load_df['DATE']]
        load_df['DESCRIPTION'] = load_df['DESCRIPTION'].str.replace("'",'')
        load_df['ORIGINAL_DESCRIPTION'] = load_df['ORIGINAL_DESCRIPTION'].str.replace("'",'')
        load_df['ACCOUNT_NAME'] = load_df['ACCOUNT_NAME'].str.replace("'",'')
        load_df['TRANSACTION_TYPE'] = [i.replace("'",'') for i in load_df['TRANSACTION_TYPE']]
        load_df['CATEGORY'] = [i.replace("'",'') for i in load_df['CATEGORY']]
       
        st.write(load_df)
        try:
            conn = connectdb()
            cur = conn.cursor()
            cur.execute('select * FROM SAMPLE1 ORDER BY INDEX DESC LIMIT 1')
            d = cur.fetchall()
            last_index = d[0][-1]
            rge = load_df.shape[0]

            load_index = []
            for k in range(rge):
                idx = int(last_index) + 1
                load_index.append(str(idx))

            load_df['INDEX'] = load_index
           
            write_pandas( conn,load_df,'SAMPLE1',database='TEST',schema='PUBLIC')

            st.write('Data Has been added')


            df = pd.read_sql('select * from SAMPLE1',conn)
            conn.close()
            df['DATE'] = [str(i).split(' ')[0] for i in df['DATE']]
            df = df[df.columns[1:]]
            st.write(df)
        except:
            st.write('An error occured')

if menu =="Edit Data":
    st.subheader("Edit CSV")
    
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
                try:
                    conn = connectdb()
                    query = f"UPDATE sample1 SET DATE = '{date}', AMOUNT = {amount}, TRANSACTION_TYPE = '{trans_type}', CATEGORY = '{category_name}' WHERE INDEX = {index}"

                    cur = conn.cursor()
    #                 query = f"UPDATE sample1 SET DATE = '05/28/2021', AMOUNT = '1.0', TRANSACTION_TYPE = 'credit', CATEGORY = 'Parking' WHERE id = 0 "
                    #cur.execute(query)
    #                 conn.execute("UPDATE sample1 SET DATE = '05/27/2014', AMOUNT = '1.0', TRANSACTION_TYPE = 'credit', CATEGORY = 'Parking' WHERE ID = 1")
                    #st.write('ireach here')
                    #st.write(query)
                    cur.execute(query)
                    #pd.read_sql(query,conn)
                    conn.commit()
                    conn.close()
                    st.write('Update has been made to the database')
                except:
                    st.write('erro establishing a connection to the database')
            except:
                st.write("index not exist")
            
    
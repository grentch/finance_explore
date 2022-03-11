import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime


yer = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec']
df = pd.read_csv('sample1.csv')
col = df.columns
categories = [] 
transact_type = []
for j in df['CATEGORY'].unique():
    categories.append(j)
    
for j in df['TRANSACTION_TYPE'].unique():
    transact_type.append(j)

df[col[0]] = pd.to_datetime(df[col[0]],errors="coerce")
df['Month'] = df[col[0]].dt.month
df['Day'] = df[col[0]].dt.day
df['Year'] = df[col[0]].dt.year
df = df.drop(['DESCRIPTION', 'ORIGINAL_DESCRIPTION'],axis=1)
bins = [0,10,20,30,40,50,60,70,80,90]
df['binned'] = pd.cut(df[col[3]],bins)


year = []
for i in df.Year.unique():
    yaer = str(i)
    if yaer != 'nan':
        year.append(int(float(yaer)))
year = tuple(sorted(year))

# Text/Title
st.title("Interactive Dashboard")

# Create a page dropdown 
#page = st.sidebar.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3","Page 4"]) 

menu = st.sidebar.radio(
     'Select Menu:', ['Main','Explore Categories','Explore raw data','Load Data into Database'],index=0)

if menu == "Main":
    selected_year = st.selectbox(
         'Select Year:',
         year)
    
    selected_month = st.select_slider(
     'Select a color of the rainbow',
     options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sept','Oct','Nov','Dec'])
    
    month = yer.index(selected_month)+1
    
     
    yar = selected_year
    current_date_start = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'01', '%Y-%m-%d')
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
        difference = round(last_two_a/two_a,2)
        st.metric(label='Total Credit',value=two_a,delta=f"{difference}")
    with col2:   
        two_b = lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='debit'].shape[0]
        last_two_b = last_month_df[last_month_df['TRANSACTION_TYPE']=='debit'].shape[0]
        difference = last_two_b - two_b
        st.metric(label='Total Number of Debit Transaction',value=two_b,delta=f"{difference}")
    with col3:
        two_c = lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='debit']['AMOUNT'].max()
        st.metric(label="Highest Debit", value=two_c)
    with col4:
        two_d = lastest_month_df[lastest_month_df['TRANSACTION_TYPE']=='debit']['AMOUNT'].mean()
        last_two_d = last_month_df[last_month_df['TRANSACTION_TYPE']=='debit']['AMOUNT'].mean()
        difference = round(last_two_d - two_d,2)
        st.metric(label='Average Debit Transaction',value=two_d,delta=f"{difference}")
        
    #print(yar,month)
    #print(yar)
    if yar !="All":
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
        print(five_months)
        #print(five_months[-1][-1],five_months[-1][-0])
        start_date = datetime.datetime.strptime(str(selected_year) +'-' + str(yer.index(selected_month)+1) + '-'+'01', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(str(five_months[-1][-1]) +'-' +str(five_months[-1][-0]) + '-'+'01', '%Y-%m-%d')
        #print(start_date)
        #print(end_date)
        try:
            mask = df[(df['DATE'] > end_date) & (df['DATE'] <= start_date)]
            mask = mask[mask['TRANSACTION_TYPE']=='debit']
            later_mask = mask[mask['Month']== yer.index(selected_month)+1]
            new_mask = mask[['Month','Year','AMOUNT']]
            new_mask['Month'] = new_mask['Month'].astype(int)
            new_mask['Year'] = new_mask['Year'].astype(int)
            fd = new_mask.groupby(['Month','Year']).sum()
            fd.plot(kind="bar")
            st.pyplot(fig=plt)
            col1, col2 = st.columns(2)
            new_mask = mask[['CATEGORY','AMOUNT']]
            fd = new_mask.groupby(['CATEGORY']).sum().sort_values(by='AMOUNT',ascending=False)
            #fd.sort_values(by=['AMOUNT'],ascending=True)

            fd.plot(kind="bar")
            st.pyplot(fig=plt)
            new_mask = later_mask[['CATEGORY','AMOUNT']]
            fd = new_mask.groupby(['CATEGORY']).sum().sort_values(by='AMOUNT',ascending=False)
            #st.write(later_mask)
            fd.plot(kind="bar")
            st.pyplot(fig=plt)
 
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
    #print(yar,month)
    #print(yar)
    if yar !="All":
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
        #print(five_months)
        #print(five_months[-1][-1],five_months[-1][-0])
        start_date = datetime.datetime.strptime(str(selected_year) +'-' + str(yer.index(selected_month)+1) + '-'+'01', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(str(five_months[-1][-1]) +'-' +str(five_months[-1][-0]) + '-'+'01', '%Y-%m-%d')
        #print(start_date)
        #print(end_date)
        try:
            new_df = df[df['CATEGORY'].isin(cate)]
            page_mask = new_df[(new_df['DATE'] > end_date) & (new_df['DATE'] <= start_date)]
            page_mask = page_mask[page_mask['TRANSACTION_TYPE']=='debit']

            page_mask = page_mask[['Month','Year','AMOUNT','CATEGORY']]
            #st.write(page_mask)
            page_mask['Month'] = page_mask['Month'].astype("Int64")
            page_mask['Year'] = page_mask['Year'].astype("Int64")
            combined_date = [ ]
            two = page_mask[['Month','Year']].values.tolist()
            #st.write(two)
            for i,j in two:
                combined_date.append(f'{yer[i]} {j}')
            page_mask['period'] = combined_date

            page_mask = page_mask[['period','AMOUNT','CATEGORY']]
            dff = page_mask.groupby(['period','CATEGORY']).sum()
            dff = dff.reset_index().pivot_table(index='period',columns='CATEGORY',values='AMOUNT')#.plot(kind="bar",stacked=True)
            #plt.legend(bbox_to_anchor=(1.04,1),loc="upper left")
            ax = dff.plot.bar(stacked=True)
            for p in ax.patches:
                width, height = p.get_width(), p.get_height()
                x, y = p.get_xy() 
                ax.text(x+width/2, 
                        y+height/2, 
                        '{:.0f} '.format(height), 
                        horizontalalignment='center', 
                        verticalalignment='center')

            plt.legend(bbox_to_anchor=(1.04,1),loc="upper left")
            st.pyplot(fig=plt)
            #st.write(pd.crosstab(index=page_mask['period'],columns=['AMOUNT']).plot(kind='bar',stacked=True))
    #         page_mask.set_index('period')
    #         page_mask.plot(kind='bar', stacked=True)
            #st.write(page_mask)
            #fd = page_mask.groupby(['Month','Year']).sum('AMOUNT')
            #st.write(fd)
    #         fd.plot(kind="bar")
    #         st.pyplot(fig=plt)
    #         st.write(df)
    #         st.write(cate)
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
    
    month = yer.index(selected_month)+1
    
     
    yar = selected_year
    current_date_start = datetime.datetime.strptime(str(yar) +'-' + str(month) + '-'+'01', '%Y-%m-%d')
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
            
            
    new_df = df[(df['DATE'] > current_date_start) & (df['DATE'] <= current_date_end)].sort_values(by='AMOUNT',ascending=False)
    st.write(new_df)
    
    
if menu =="Load Data into Database":
    
    st.subheader("Load CSV")
    csv_file = st.file_uploader("Upload file", type=["csv"])

    if csv_file is not None:

        # To See details
        file_details = {"filename":csv_file.name, "filetype":csv_file.type,
                      "filesize":csv_file.size}
        st.write(file_details)
        
        load_df = pd.read_csv(file_details['filename'])
        st.write(load_df)

        

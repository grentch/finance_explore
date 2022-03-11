import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv('transactions.csv')
col = df.columns
categories = ['All'] 
transact_type = ['All']
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
year = tuple(['All']+sorted(year))

# Text/Title
st.title("Interactive Dashboard")

def show_day_chart(day):
    #print(day)
    day_plot = day.astype(int).value_counts().plot(kind='bar')
    plt.xlabel('Days',labelpad=7)
    plt.ylabel('Number of Transactions',labelpad=7)
    plt.title('Day Plot')
    st.pyplot(fig=plt)
    
    return None

def show_transaction_type_chart(transaction_type,is_all):
    if is_all == 'All':
        plt.clf()
        plt.pie(transaction_type.value_counts(),autopct='%1.1f%%',explode=(0,0.1),startangle=0,labels=['debit','credit'])
        plt.title('Transaction Type')
        st.pyplot(fig=plt)
    else:
        pass
    
    return None

def show_amount_plot(binned_amount):
    binned_amount.value_counts().plot(kind='bar')
    plt.xlabel('Amount Ranges',labelpad=7)
    plt.ylabel('Number of Transactions',labelpad=7)
    plt.title('Amount Plot')
    st.pyplot(fig=plt)
    
    return None
 
def show_transaction_chart(transaction,is_all):
    if is_all == 'All':
        transaction.value_counts().plot(kind='bar')
        plt.xlabel('Transaction Categories',labelpad=14)
        plt.ylabel('Number of Transactions',labelpad=14)
        plt.title('Transaction Plot')
        st.pyplot(fig=plt)
    else:
        pass
    
    return None


def parse_amount_column(column):
    
    mean = column.mean()
    minimum = column.min()
    maximum = column.max()
    length = len(column)
    
    return mean,minimum,maximum,length

def write_amount_details(mean,minimum,maximum,length):
    st.write('The minimum transaction amount is ',minimum)
    st.write('The average transaction amount is ',round(mean,2))
    st.write('The maximum transaction amount is ',maximum)
    st.write('Total number of transaction is ',length)

def get_months():
    selected = []
    if option_all:
        for i in range(1,13):
            selected.append(i)
        return selected
    if option_jan:
        selected.append(1)
    if option_feb:
        selected.append(2)
    if option_mar:
        selected.append(3)
    if option_apr:
        selected.append(4)
    if option_may:
        selected.append(5)
    if option_jun:
        selected.append(6)
    if option_jul:
        selected.append(7)
    if option_aug:
        selected.append(8)
    if option_sept:
        selected.append(9)
    if option_oct:
        selected.append(10)
    if option_nov:
        selected.append(11)
    if option_dec:
        selected.append(12)
    
    return selected

def refresh_all_year_some_month():
    #st.write(option_transaction_category)
    selected_month = get_months()
    if len(selected_month)<1:
        st.write('select month')
    else:
        if option_transaction_category == 'All' and  option_transaction_type == 'All':
            #st.write('all both')
            new_df = df[df['Month'].isin(selected_month)]
        elif option_transaction_category == 'All' and  option_transaction_type != 'All':
            #st.write(option_transaction_type)
            new_df = df[df['Month'].isin(selected_month)]
            new_df = new_df[new_df['TRANSACTION_TYPE']==option_transaction_type]
        elif option_transaction_category != 'All' and  option_transaction_type == 'All':
            new_df = df[df['Month'].isin(selected_month)]
            new_df = new_df[new_df['CATEGORY']==option_transaction_category]
        elif option_transaction_category != 'All' and  option_transaction_type != 'All':
            new_df = df[df['Month'].isin(selected_month)]
            new_df = new_df[(new_df['TRANSACTION_TYPE']==option_transaction_type) & (new_df['CATEGORY']==option_transaction_category)]
            
        #run the visualization
        #st.write(selected_month)
        #st.write(new_df)
        minimum,average,maximum,length = parse_amount_column(new_df['AMOUNT'])
        write_amount_details(minimum,average,maximum,length)
        show_day_chart(new_df['Day'].head())
        show_amount_plot(new_df['binned'])
        is_all_cat = option_transaction_category
        is_all_type = option_transaction_type
        show_transaction_chart(new_df[col[5]],is_all_cat)
        show_transaction_type_chart(df[col[4]],is_all_type)
    
    
def refresh_specific_year():
    selected_month = get_months()
    if len(selected_month) <1:
        st.write('select month')
    else:
        if option_transaction_category == 'All' and  option_transaction_type == 'All':
            new_df = df[df['Month'].isin(selected_month)]
        elif option_transaction_category == 'All' and  option_transaction_type != 'All':
            new_df = df[df['Month'].isin(selected_month)]
            new_df = new_df[new_df['TRANSACTION_TYPE']==option_transaction_type]
        elif option_transaction_category != 'All' and  option_transaction_type == 'All':
            new_df = df[df['Month'].isin(selected_month)]
            new_df = new_df[new_df['CATEGORY']==option_transaction_category]
        elif option_transaction_category != 'All' and  option_transaction_type != 'All':
            new_df = df[df['Month'].isin(selected_month)]
            new_df = new_df[(new_df['TRANSACTION_TYPE']==option_transaction_type) & (new_df['CATEGORY']==option_transaction_category)]
            
        #run the visualization
        #st.write(selected_month)
        #st.write(new_df)
        minimum,average,maximum,length = parse_amount_column(new_df['AMOUNT'])
        write_amount_details(minimum,average,maximum,length)
        show_day_chart(new_df['Day'].head())
        show_amount_plot(new_df['binned'])
        is_all_cat = option_transaction_category
        is_all_type = option_transaction_type
        show_transaction_chart(new_df[col[5]],is_all_cat)
        show_transaction_type_chart(df[col[4]],is_all_type)
#         new_df = df[df['Month'].isin(selected_month)]
#         #run the visualization
#         #st.write(selected_month)
#         #st.write(new_df)
#         minimum,average,maximum,length = parse_amount_column(new_df['AMOUNT'])
#         write_amount_details(minimum,average,maximum,length)
#         show_day_chart(new_df['Day'].head())
#         show_amount_plot(new_df['binned'])
#         show_transaction_chart(new_df[col[5]])
#         show_transaction_type_chart(df[col[4]])
          




def refresh_all_month():
    selected_year = option_year
    #st.write('showing data for all months')
    
def refresh_specific_month():
    selected_year = option_year
    #st.write('showing data for some months')
    months =['option_jan','option_feb','option_mar','option_apr','option_may','option_jun','option_jul','option_aug','option_sept','option_oct','option_nov','option_dec']
    
      
    
    
option_year = st.sidebar.selectbox(
     'Select Year:',
     year)


option_transaction_type = st.sidebar.radio(
     'Select Transaction Type:', transact_type,index=0)


option_transaction_category = st.sidebar.radio(
     'Select Category:', categories,index=0)

st.sidebar.write('Select Month:')
option_all = st.sidebar.checkbox('All')
option_jan = st.sidebar.checkbox('January')
option_feb = st.sidebar.checkbox('Febuary')
option_mar = st.sidebar.checkbox('March')
option_apr = st.sidebar.checkbox('April')
option_may = st.sidebar.checkbox('May')
option_jun = st.sidebar.checkbox('June')
option_jul = st.sidebar.checkbox('July')
option_aug = st.sidebar.checkbox('August')
option_sept = st.sidebar.checkbox('September')
option_oct = st.sidebar.checkbox('October')
option_nov = st.sidebar.checkbox('November')
option_dec = st.sidebar.checkbox('December')


if option_year:
    if option_year == 'All':
        refresh_all_year_some_month()
    else:
        refresh_specific_year()
        
    #st.write(option_year)
    #st.write(df.head())
    
#  option_jan and option_feb and option_mar and option_apr and option_may and option_jun and option_jul and option_aug and option_sept and option_oct and option_nov and option_dec
if option_all:
    refresh_all_month()
if option_jan or option_feb or option_mar or option_apr or option_may or option_jun or option_jul or option_aug or option_sept or option_oct or option_nov or option_dec:  
    refresh_specific_month()
    
    
  

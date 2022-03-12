from sqlalchemy import create_engine
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas


#stores the csv data into a database

#connecting to database using sqlalchemy
#mysql/mariadb
#engine = create_engine("mysql+pymysql://root@localhost/test")

#postgress
#engine = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"


#file name
#file_name = 'sample1.csv'
#df = pd.read_csv(file_name)
#df.to_sql(con=engine, index_label='id', name='sample4', if_exists='replace')

conn = snowflake.connector.connect(
 user='ididntdoit',
 password='Odunayo0',
 account='pp47726.us-east-2.aws',
 database='test',
 #schema= "test_schema"
)
print("success in connecting", conn)

query = "USE DATABASE TEST"
cur.execute(query)

query = "USE SCHEMA PUBLIC"
cur.execute(query)

query = """create table sample2(DATE varchar , DESCRIPTION varchar, ORIGINAL_DESCRIPTION varchar, AMOUNT varchar,
       TRANSACTION_TYPE varchar, CATEGORY varchar, ACCOUNT_NAME varchar, LABELS varchar, NOTES varchar)"""
cur.execute(query)
print('created table')

df = pd.read_csv(r'C:\Users\DELL\Desktop\Code\Streamlit\upwork\upworkGit\finance_explore\sample_file_big.csv')


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

with open('env.txt','r') as r:
    details = r.read()
    
details = eval(details)

conn = snowflake.connector.connect(
                             user= details['user'],
                             password=details['password'],
                             account=details['account'],
                             database="TEST",
                             schema= "PUBLIC"
                            )
print("success in connecting", conn)
cur = conn.cursor()
query = "USE DATABASE TEST"
cur.execute(query)

query = "USE SCHEMA PUBLIC"
cur.execute(query)

query = "DROP TABLE IF EXISTS sample1"
cur.execute(query)


print('about creating the table')
query = """create table sample1(DATE varchar(10) , DESCRIPTION varchar(200), ORIGINAL_DESCRIPTION varchar(200), AMOUNT varchar(30),
       TRANSACTION_TYPE varchar(10), CATEGORY varchar(100), ACCOUNT_NAME varchar(100), LABELS varchar (100), NOTES varchar(100),index varchar(100))"""
cur.execute(query)
print('created table')

df = pd.read_csv('sample_file_big.csv')

df['INDEX'] = df.index

df = df.head(1000)

#SAMPLE1 is the table name
write_pandas( conn,df,'SAMPLE1',database='TEST',schema='PUBLIC')
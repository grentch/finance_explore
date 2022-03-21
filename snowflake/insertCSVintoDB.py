from sqlalchemy import create_engine
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import configparser

parser = configparser.ConfigParser()
parser.read('DBcredentials.ini')

    
conn = snowflake.connector.connect(
                             user= parser.get('SNOWFLAKE DATABASE Details','user'),
                             password=parser.get('SNOWFLAKE DATABASE Details','password'),
                             account=parser.get('SNOWFLAKE DATABASE Details','account'),
                             database=parser.get('SNOWFLAKE DATABASE Details','database'),
                             schema= parser.get('SNOWFLAKE DATABASE Details','schema')
                            )

print("success in connecting", conn)
cur = conn.cursor()
query = "USE DATABASE TEST"
cur.execute(query)

query = "USE SCHEMA PUBLIC"
cur.execute(query)

query = "DROP TABLE IF EXISTS sample2"
cur.execute(query)


print('about creating the table')
query = """create table sample2(DATE varchar(10) , DESCRIPTION varchar(200), ORIGINAL_DESCRIPTION varchar(200), AMOUNT varchar(30),
       TRANSACTION_TYPE varchar(10), CATEGORY varchar(100), ACCOUNT_NAME varchar(100), LABELS varchar (100), NOTES varchar(100),index varchar(100))"""
cur.execute(query)
print('created table')

df = pd.read_csv('sample_file_big.csv')

df['INDEX'] = df.index

df = df.head(1000)

#SAMPLE1 is the table name
write_pandas( conn,df,'SAMPLE2',database='TEST',schema='PUBLIC')
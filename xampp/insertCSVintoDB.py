from sqlalchemy import create_engine
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import configparser
import pymysql

parser = configparser.ConfigParser()
parser.read('DBcredentials.ini')

    
def connectdb():
    
    conn =pymysql.connect(
        user = 'root',
        password = '',
        db = parser.get('MARIADB DATABASE Details','database'),
        host = 'localhost',


    )

   
   
    print("success in connecting", conn)
    return conn

conn = connectdb()
cur = conn.cursor()

print('about creating the table')
query = """
create or replace TABLE sample1 (
    DATE VARCHAR(10),
    DESCRIPTION VARCHAR(200),
    ORIGINAL_DESCRIPTION VARCHAR(200),
    AMOUNT VARCHAR(30),
    TRANSACTION_TYPE VARCHAR(10),
    CATEGORY VARCHAR(100),
    ACCOUNT_NAME VARCHAR(100),
    LABELS VARCHAR(100),
    NOTES VARCHAR(100)
);
"""
cur.execute(query)
print('created table')

df = pd.read_csv('sample_file_big.csv')
df['DATE'] = [i.replace("'",'') for i in df['DATE']]
df['DESCRIPTION'] = df['DESCRIPTION'].str.replace("'",'')
df['ORIGINAL_DESCRIPTION'] = df['ORIGINAL_DESCRIPTION'].str.replace("'",'')
df['ACCOUNT_NAME'] = df['ACCOUNT_NAME'].str.replace("'",'')
df['TRANSACTION_TYPE'] = [i.replace("'",'') for i in df['TRANSACTION_TYPE']]
df['CATEGORY'] = [i.replace("'",'') for i in df['CATEGORY']]
df = df.fillna('N/A')
#st.write(df)

conn = connectdb()
cur = conn.cursor()

for l in df.values:
    val = list(l)
    val = str(val).replace('[','(').replace(']',')')
    print(val.replace('nan',' '))
    query = f"INSERT INTO sample1 (`DATE`, `DESCRIPTION`, `ORIGINAL_DESCRIPTION`, `AMOUNT`, `TRANSACTION_TYPE`, `CATEGORY`, `ACCOUNT_NAME`, `LABELS`, `NOTES`) VALUES{val}"
    #print(query)
    cur.execute(query)
    conn.commit()

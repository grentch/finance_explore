import snowflake.connector
import configparser

parser = configparser.ConfigParser()
parser.read('DBcredentials.ini')

def connectdb():
    
    conn = snowflake.connector.connect(
                                 user= parser.get('SNOWFLAKE DATABASE Details','user'),
                                 password=parser.get('SNOWFLAKE DATABASE Details','password'),
                                 account=parser.get('SNOWFLAKE DATABASE Details','account'),
                                 database=parser.get('SNOWFLAKE DATABASE Details','database'),
                                 schema=parser.get('SNOWFLAKE DATABASE Details','schema'),
                                 #table=parser.get('SNOWFLAKE DATABASE Details','table')
                                )
    print("success in connecting", conn)
   
    return conn
import pandas as pd
from sqlalchemy import create_engine


#stores the csv data into a database

#connecting to database using sqlalchemy
#mysql/mariadb
engine = create_engine("mysql+pymysql://root@localhost/test")

#postgress
#engine = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"


#file name
file_name = 'sample1.csv'
df = pd.read_csv(file_name)
df.to_sql(con=engine, index_label='id', name='sample4', if_exists='replace')


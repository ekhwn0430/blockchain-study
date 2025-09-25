import pandas as pd
import sqlite3


# create connection to file 'sample.db' ('sample.db' created actual folder)
conn =sqlite3.connect('sample.db')

# create DataFrame
df = pd.DataFrame()
df['seller'] = pd.Series(['tom', 'james', 'kaka'])
df['buyer'] = pd.Series(['pepe', 'alex', 'mike'])
df['amount'] = pd.Series([10, 30, 20])

# save test_transaction of connection(sample.db) by using to_sql()
df.to_sql('test_transaction', conn)

# test_transaction of connection(sample.db) fetches data into SQL statement
df = pd.read_sql_query("SELECT * FROM test_transaction", conn)

print(df)

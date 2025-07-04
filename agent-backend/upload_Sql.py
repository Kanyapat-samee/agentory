import pandas as pd
from sqlalchemy import create_engine, types, text
import urllib

#Connection config
server = 'XXXXXXX'
database = 'XXXXXXX'
username = 'XXXXXXX'
password = 'XXXXXXX'
driver = 'ODBC Driver 18 for SQL Server'

#Connection string
params = urllib.parse.quote_plus(
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

#Load and clean CSV
df = pd.read_csv('ForcastSingapore.csv')
df = df.drop(columns=['Unnamed: 0'])

#Convert Date
df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

#SQL Data Types
sql_dtypes = {
    'Date': types.DATE(),
    'Total_Cap': types.Integer(),
    'Predicted_Outbound_KT': types.FLOAT(),
    'Predicted_Inventory_KT': types.Integer(),
    'Inventory_Ratio': types.String(),
    'PreINVmiOUT_ratio': types.String(),
}


#Upload
df.to_sql('ForecastSingapore', con=engine, if_exists='replace', index=False, dtype=sql_dtypes)

print(f"Uploaded {len(df)} rows to 'ForecastSingapore' table in database '{database}'.")
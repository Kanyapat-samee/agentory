# query_executor.py
import os
import pandas as pd
import urllib
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

#เชื่อมต่อ SQL Server
server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DATABASE")
username = os.getenv("AZURE_SQL_USERNAME")
password = os.getenv("AZURE_SQL_PASSWORD")
driver = "ODBC Driver 18 for SQL Server"

#Create connection string
params = urllib.parse.quote_plus(
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def execute_sql(sql_query: str) -> list[dict]:
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]

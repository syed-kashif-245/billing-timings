
import pyodbc

def getconnection():
    con = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=ACU-HYD-LT-2012\\SQLEXPRESS;"
        "DATABASE=SubscriptionBilling;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return con

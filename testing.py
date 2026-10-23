
from db import getconnection

con = getconnection()
print("Database connected successfully!")

con.close()

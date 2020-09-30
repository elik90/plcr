import pyodbc


for driver in pyodbc.drivers():
    print(driver)

con = pyodbc.connect('Trusted_Connection=yes', driver = '{SQL Server}',server = 'localhost', database = 'dbtesttest')
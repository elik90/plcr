import pyodbc


for driver in pyodbc.drivers():
    print(driver)

# define server name and database name
#server = "J-IK02\ikhwan"
#database = "elliotdb1"

#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=testdb;Trusted_Connection=yes')

# define our connection string
cnxn = pyodbc.connect('DRIVER={SQL Server};'
                       'SERVER=localhost;'
                       'DATABASE=elliotdb1;'
                       'UID=ikhwan;'
                       'PWD=jooTinho10;'
                       'Trusted_Connection=yes;')

# create the conenction cursor
cursor = cnxn.cursor()

if cursor.tables(table='People').fetchone():
    print('yes it does')

    
# cursor.execute('''

#                 CREATE TABLE People
#                 (
#                 Name nvarchar(50),
#                 Age int,
#                 City nvarchar(50)
#                 )

#                 ''')



cnxn.commit()

cursor.execute('''
                
                INSERT INTO elliotdb1.dbo.People (Name, Age, City)
                VALUES
                ('Jade', 20, 'London'),
                ('Mary', 47, 'Boston'),
                ('Jon', 35, 'Paris')
                
                ''')

cnxn.commit()


for row in cursor.tables(table='People'):
    print(row.table_name)



 
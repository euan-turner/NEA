import sqlite3

connection = sqlite3.connect("Connect4.db")
cursor = connection.cursor()

##Define the table store within Connect4.db
create_store = """
CREATE TABLE store
(
fileID INTEGER,
filetype INTEGER,
data TEXT,
primary key (fileID)
)
"""
##sqlite3 will autoincrement integer primary keys

cursor.execute(create_store)
connection.commit()
connection.close()
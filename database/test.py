import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="DB7WS"
)

cursorInsert = mydb.cursor()


consulta = "INSERT INTO user(username, password, fullname, user_type) VALUES ('Admin', 'admin', 'Juan Garcia', 'admin');"

cursorInsert.execute(consulta)

mydb.commit()
cursorInsert.close()
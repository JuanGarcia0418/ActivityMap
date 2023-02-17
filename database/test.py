import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="DB7WS"
)

cursorInsert = mydb.cursor()


consulta = "INSERT INTO User(username, password, fullname) VALUES ('Admin', 'pbkdf2:sha256:260000$XGxePWC6QrcswbeY$61e59403515d39ca72e944ec1da6366eecb3bea50d3a511d6af30695570f5471', 'Juan Andres Garcia');"

cursorInsert.execute(consulta)

mydb.commit()
cursorInsert.close()
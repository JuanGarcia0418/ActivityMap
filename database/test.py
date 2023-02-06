import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="Activity"
)

cursorInsert = mydb.cursor()


consulta = "INSERT INTO Activity(name, created_at ,description, evidence, projectid, userid, imageid) VALUES ('jdka', NOW(), 'jksndja', 'Mc', '5', '9', 'jkanadsf');"

cursorInsert.execute(consulta)

mydb.commit()
cursorInsert.close()
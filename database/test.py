import mysql.connector
import uuid

# Establecer conexión con la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="DB7WS"
)


# Crear cursor
cursor = mydb.cursor()

# Generar UUID
id = uuid.uuid4()

# Insertar datos con UUID
consulta = "INSERT INTO user(id, username, password, fullname, user_type) VALUES (%s,%s,%s,%s,%s)"
values = (str(id),'Test', 'test', 'User test', 'test')
cursor.execute(consulta, values)

# Hacer commit y cerrar conexión
mydb.commit()
mydb.close()




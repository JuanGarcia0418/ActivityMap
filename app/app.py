from flask import Flask, jsonify, request, render_template
import mysql.connector
import datetime
import json
from config import config

app = Flask(__name__)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Activity"
)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/projectsuser')
def projects_user():
    return render_template('projectsuser.html')

@app.route('/actividad', methods=['GET'])
def listar_actividades():
    try:
        cursor = conexion.cursor()
        sql="SELECT activity_id, name, description, evidence, projectid, userid, imageid FROM Activity"
        cursor.execute(sql)
        datos=cursor.fetchall()
        actividades=[]
        for fila in datos:
            actividad = {'activity_id':fila[0],'name':fila[1], 'description':fila[2], 'evidence':fila[3], 'projectid':fila[4], 'userid':fila[5], 'imageid':fila[6]}
            actividades.append(actividad)
        return jsonify({'actividades':actividades, 'mensaje': "Actividades"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})



@app.route('/actividad/<activity_id>', methods=['GET'])
def leer_actividad(activity_id):
    try:
        cursor = conexion.cursor()
        sql="SELECT activity_id, name, created_at, description, evidence, projectid, userid, imageid FROM Activity WHERE activity_id = '{0}'".format(activity_id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            actividad = {'activity_id':datos[0],'name':datos[1], 'created_at':datos[2], 'description':datos[3], 'evidence':datos[4], 'projectid':datos[5], 'userid':datos[6], 'imageid':datos[7]}
            return jsonify({'actividad':actividad, 'mensaje': "Actividad encontrada"})
        else:
            return jsonify({'mensaje':"curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/actividad', methods=['POST'])
def registrar_actividad():
    try:
        cursor = conexion.cursor()
        sql="""INSERT INTO Activity(name, description, evidence, projectid, userid, imageid) 
        VALUES ('{0}', '{1}', '{2}', {3}, {4}, '{5}')""".format(request.json['name'], request.json['description'], request.json['evidence'], request.json['projectid'], request.json['userid'], request.json['imageid'])
        cursor.execute(sql)
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': "Curso Registrado"})
    except Exception as ex:
        return jsonify({'messaje':"Error"})

def pagina_no_encontrada(error):
    return "<h1>La pagina no existe</h1>", 404

if __name__ == "__main__" :
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)

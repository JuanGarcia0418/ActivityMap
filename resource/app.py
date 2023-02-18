from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-node', methods=['POST'])
# route for processor data of the form
def create_node():
    # get data of the from
    cnn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cytoscape_db"
    )
    name = request.form['name']
    date = request.form['date']
    description = request.form['description']
    # create cursor for execute query
    cursor = cnn.cursor()
    # consult for create a new node
    insert_query = "INSERT INTO nodes (name, date, description) VALUES (%s, %s, %s)"
    values = (name, date, description)
    cursor.execute(insert_query, values)
    cnn.commit()
    # close cursor
    cursor.close()
    # redirect the user to a form page
    return redirect('/')


@app.route('/graph-data')
# route for get the nodes and edges data
def graph_data():
    # Execute cursor for SQL query
    cnn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cytoscape_db"
    )
    cursor = cnn.cursor()
    # create query for get nodes data
    nodes_query = "SELECT name, date, description FROM nodes"
    cursor.execute(nodes_query)
    nodes_data = cursor.fetchall()
    # create query fir get edges data
    edges_query = "SELECT id, source, target FROM edges"
    cursor.execute(edges_query)
    edges_data = cursor.fetchall()
    # close cursor
    cursor.close()
    # genere json with the data
    graph_data = {
        "nodes": [{"data": {"name": node[0], "date": node[1], "description": node[2]}}
                  for node in nodes_data],
        "edges": [{"data": {"id": edge[0], "source": edge[1], "target": edge[2]}}
                  for edge in edges_data]
    }
    # return JSON
    return jsonify(graph_data)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, request, render_template, url_for
from flask_mysqldb import MYSQL
from config import config

app = Flask(__name__)

db = MYSQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['user'])
        print(request.form['password'])
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/projectsuser')
def projects_user():
    return render_template('projectsuser.html')

def pagina_no_encontrada(error):
    return "<h1>La pagina no existe</h1>", 404

if __name__ == "__main__" :
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)

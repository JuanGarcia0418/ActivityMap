from flask import Flask, redirect, request, render_template, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)

db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['user'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('projects'))
            else:
                flash("Contraseña invalida")
                return render_template('index.html')
        else:
            flash("Usuario no encontrado")
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

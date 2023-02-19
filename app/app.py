from flask import Flask, redirect, request, render_template, url_for, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import mysql.connector
from flask_cors import CORS
from models.User import User
from config import config
from model import db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/DB7WS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# conecction for the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DB7WS"
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
# login management
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
# login section for the user
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
# render login data
def login():
    if request.method == 'POST':
        # get information from the form
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        # verification the correct password
        if user and user.password == password:
            login_user(user)
            session['user_id'] = user.id
            return redirect('/view')
    # return to login page if the password is wrong
        else:
            return render_template('index.html', error='invalid username or password')
    else:
        return render_template('index.html')


@app.route('/logout')
@login_required
# logout function and return to login page
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/view')
# function for visualization for different user
def view():
    if current_user.user_type == 'admin':
        return redirect(url_for('create_node'))
    else:
        return render_template('view.html')


@app.route('/form')
# form for create and see a projects
def form():
    return render_template('projectsTable.html')


@app.route('/table',  methods=['GET', 'POST'])
# render information for input to Database
def projects_user():
    if request.method == 'POST':
        # get information from the form
        name = request.form['projectName']
        company_name = request.form['nameCompany']
        date = request.form['date']
        requirements = request.form['requirements']
        user_id = session['user_id']
        # create query for insert data
        cursor = mydb.cursor()
        project_query = "INSERT INTO projects(name, date, description, user_id, company_name) VALUES (%s, %s, %s, %s, %s)"
        values = (name, date, requirements, user_id, company_name)
        cursor.execute(project_query, values)
        mydb.commit()
        # close cursor
        cursor.close()
        # render
    return render_template('projectsTable.html')


@app.route('/create_activity_nodes', methods=['POST', 'GET'])
def create_node():
    if request.method == 'POST':
        # get information from the form
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        user_id = session['user_id']
        # create cursor for execute query
        cursor = mydb.cursor()
        # consult for create a new node
        node_query = "INSERT INTO activities(name, date, description, user_id) VALUES (%s, %s, %s, %s)"
        values = (name, date, description, user_id)
        cursor.execute(node_query, values)
        mydb.commit()
        # close cursor
        cursor.close()
        # redirect the user to a form page
    return render_template('managementActivity.html')


def pagina_no_encontrada(error):
    return "<h1>La pagina no existe</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)

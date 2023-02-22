from flask import Flask, redirect, request, render_template, url_for, session, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import uuid
import mysql.connector
from mysql.connector import connect, Error
from flask_cors import CORS
from models.User import User
# from models.Project import Projects
# from models.Activity import Activity
# from models.UserProjects import UserProjects
from config import config
from model import db

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/DB7WS"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# conecction for the database
mydb = mysql.connector.connect(
    host="localhost", user="root", password="root", database="DB7WS"
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
# login management
def load_user(user_id):
    return User.query.get(str(user_id))


@app.route("/")
# login section for the user
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
# render login data
def login():
    if request.method == "POST":
        # get information from the form
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        # verification the correct password
        if user and user.password == password:
            login_user(user)
            session["user_id"] = user.id
            return redirect("/view")
        # return to login page if the password is wrong
        else:
            return render_template("index.html", error="invalid username or password")
    else:
        return render_template("index.html")


@app.route("/logout")
@login_required
# logout function and return to login page
def logout():
    logout_user()
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/view")
# function for visualization for different user
def view():
    if current_user.user_type == "admin":
        return redirect(url_for("create_projects"))
    else:
        return redirect(url_for("form_projects"))


@app.route("/form_project")
# form for create and see a projects
def form_projects():
    # create query for show data
    if current_user.user_type == "admin":
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        cursor.close()
        return render_template("projectsTable.html", users=users, projects=projects)
    # get the loged user_id
    # create query for show data
    user_id = session["user_id"]
    cursor = mydb.cursor()
    projects_query = "SELECT projects.name, projects.date, projects.description, projects.company_name FROM projects INNER JOIN user_projects ON projects.id = user_projects.project_id WHERE user_projects.user_id = %s"
    cursor.execute(projects_query, (user_id,))
    projects = cursor.fetchall()
    cursor.close()
    # render table
    return render_template("tableUser.html", projects=projects)


# @app.route("/form_activities")
# def form_activities():
#     cursor = mydb.cursor()
#     cursor.execute("SELECT * FROM projects")
#     projects = cursor.fetchall()
#     cursor.close()
#     return render_template("managementActivity.html", projects=projects)


@app.route("/create_project", methods=["GET", "POST"])
# render information for input to projects table
def create_projects():
    if request.method == "POST":
        # # get information from the form
        project_id = str(uuid.uuid4())
        name = request.form["name"]
        date = request.form["date"]
        requirements = request.form["requirements"]
        company_name = request.form["company_name"]
        # create query for insert data
        cursor = mydb.cursor()
        project_query = "INSERT INTO projects(id, name, date, description, company_name) VALUES (%s,%s, %s, %s, %s)"
        values = (project_id, name, date, requirements, company_name)
        cursor.execute(project_query, values)
        mydb.commit()
        cursor.close()
        return redirect(url_for("form_projects"))
    #render
    return redirect(url_for("form_projects"))
        
@app.route('/assign_project', methods=['GET', 'POST'])
# assigne project for the client
def assign_project():
    if request.method == 'POST':
        assign_id = str(uuid.uuid4())
        user_id = request.form['user_id']
        project_id = request.form['project_id']
        cursor = mydb.cursor()
        assign_query = "INSERT INTO user_projects (id, user_id, project_id) VALUES (%s,%s,%s)"
        values = (assign_id, user_id, project_id)
        cursor.execute(assign_query, values)
        mydb.commit()
        return redirect(url_for('form_projects'))
        
    if current_user.user_type == "cliente":
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        cursor.close()
    return redirect(url_for('form_projects'))



@app.route("/delete_project/", methods=["POST"])
def delete_project():
    if request.method == "POST":
        # get information fron the form
        project_id = request.form["project_id"]
        # create query for insert data
        cursor = mydb.cursor()
        delete_user_projects_query = "DELETE FROM user_projects WHERE project_id = %s"
        cursor.execute(delete_user_projects_query, (project_id,))
        delete_actitivity_query = "DELETE FROM activities WHERE project_id = %s"
        cursor.execute(delete_actitivity_query, (project_id,))
        delete_project_query = "DELETE FROM projects WHERE id = %s"
        cursor.execute(delete_project_query, (project_id,))
        mydb.commit()
        cursor.close()
    # rediret after delte project
    return redirect(url_for("form_projects"))


@app.route('/user_project', methods=["POST"])
def user_project():
    if request.method == 'POST':
        return render_template('projectsUser.html')



@app.route('/create_activities/<project_id>', methods=["GET", "POST"])
# render information for input to activities table
def create_activities(project_id):
    if request.method == 'POST':
        activity_id = str(uuid.uuid4())
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        cursor = mydb.cursor()
        query = "INSERT INTO activities (id, name, date, description, project_id) VALUES (%s, %s, %s, %s,%s)"
        values = (activity_id, name, date, description, project_id)
        cursor.execute(query, values)
        mydb.commit()
        return redirect(url_for('create_activities', project_id=project_id))

    return render_template('createActivities.html', project_id=project_id)

def pagina_no_encontrada(error):
    return "<h1>La pagina no existe</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)


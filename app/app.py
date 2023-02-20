from flask import (
    Flask,
    redirect,
    request,
    render_template,
    url_for,
    session,
    abort,
    jsonify,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import uuid
import mysql.connector
from flask_cors import CORS
from models.User import User
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
        projects_query = "SELECT * FROM projects"
        cursor.execute(projects_query)
        project = cursor.fetchall()
        return render_template("projectsTable.html", projects=project)
    # get the loged user_id
    # create query for show data
    user_id = session["user_id"]
    cursor = mydb.cursor()
    projects_query = "SELECT * FROM projects WHERE user_id = %s "
    cursor.execute(projects_query)
    project = cursor.fetchall()
    # render table
    return render_template("projectsTable.html", projects=project)


@app.route("/form_activity")
def form_activities():
    return render_template("managementActivity.html")


@app.route("/create_project", methods=["GET", "POST"])
# render information for input to projects table
def create_projects():
    if request.method == "POST":
        # get information from the form
        id = uuid.uuid4()
        name = request.form["name"]
        company_name = request.form["company_name"]
        date = request.form["date"]
        requirements = request.form["requirements"]
        # create query for insert data
        cursor = mydb.cursor()
        project_query = "INSERT INTO projects(id, name, date, description, company_name) VALUES (%s,%s, %s, %s, %s)"
        values = (str(id), name, date, requirements, company_name)
        cursor.execute(project_query, values)
        mydb.commit()
        # close cursor
        cursor.close()
        return redirect(url_for("form_projects"))
            # render

@app.route("/delete_project/", methods=["POST"])
def delete_project():
    if request.method == "POST":
        # get information fron the form
        project_id = request.form["project_id"]
        # create query for insert data
        cursor = mydb.cursor()
        delete_query = "DELETE FROM projects WHERE id = %s"
        cursor.execute(delete_query, (project_id,))
        mydb.commit()
        cursor.close()
    # rediret after delte project
    return redirect(url_for("form_projects"))

@app.route('/userproject', methods=["POST"])
def projectsUser():
    if request.method == 'POST':
        return render_template('projectsUser.html')

# @app.route('/add_activity')
# # asigne project for one activity
# def add_activity():
#     # get information fron the form
#     project_id = request.form['project_id']
#     # redirect to activity
#     return render_template("/managementActivity", project_id=project_id)


@app.route("/create_activity", methods=["GET", "POST"])
# render information for input to activities table
def create_activities():
    if request.method == "GET":
        project_id = request.args.get("project_id")
        return redirect(url_for("form_activities", project_id=project_id))

    if request.method == "POST":
        # get information from the form
        id = uuid.uuid4()
        name = request.form["name"]
        date = request.form["date"]
        description = request.form["description"]
        user_id = session["user_id"]
        project_id = request.form["project_id"]
        # create cursor for execute query
        cursor = mydb.cursor()
        # consult for create a new node
        node_query = "INSERT INTO activities(id, name, date, description, user_id, project_id) VALUES (%s,%s, %s, %s, %s,%s)"
        values = (str(id), name, date, description, user_id, project_id)
        cursor.execute(node_query, values)
        mydb.commit()
        # close cursor
        cursor.close()
        # redirect the user to a form page
    return redirect(url_for("form_activities"))


@app.route("/get_activities")
# generate JSON response about the activites and relations
def get_activities():
    # get the loged user_id
    user_id = session.get("user_id")
    # crete cursor for excute query
    cursor = mydb.cursor()
    # create query for get activities data
    nodes_query = "SELECT * FROM activities WHERE user_id = %s"
    cursor.execute(nodes_query, (user_id,))
    nodes_data = cursor.fetchall()
    # create query for get relations data
    # edges_query = 'SELECT * FROM relations WHERE user_id = %s'
    # cursor.execute(edges_query, (user_id,))
    # edges_data = cursor.fetchall()
    # close cursor
    cursor.close()
    # generate JSON with the all data
    graph_data = {
        "nodes": [
            {"data": {"name": node[1], "date": node[2], "description": node[3]}}
            for node in nodes_data
        ]
        # "edges": [{"data": {"id": edge[0], "source": edge[1], "target": edge[2]}}
        #           for edge in edges_data]
    }

    return jsonify(graph_data)


def pagina_no_encontrada(error):
    return "<h1>La pagina no existe</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)

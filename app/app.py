from flask import Flask, redirect, request, render_template, url_for, session, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from uuid import uuid4
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
def load_user(user_id):
    """get user_id for the login"""
    return User.query.get(str(user_id))


@app.route("/")
def index():
    """login section for the user"""
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """render login data"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            session['user_id'] = user.id
            return redirect('/view')
        else:
            return render_template('index.html', error="invalid username or password")
    else:
        return render_template('index.html')


@app.route("/logout")
@login_required
def logout():
    """logout function and return to login page"""
    logout_user()
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/view")
def view():
    """function for visualization for different user"""
    if current_user.user_type == "admin":
        return redirect(url_for('create_projects'))
    else:
        return redirect(url_for('form_projects'))


@app.route("/form_project")
def form_projects():
    """reate query for show data"""
    if current_user.user_type == "admin":
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        return render_template('projectsTable.html', users=users, projects=projects)
    user_id = session["user_id"]
    projects_query = "SELECT projects.name, projects.date, " \
        "projects.description, projects.company_name " \
        "FROM projects " \
        "INNER JOIN user_projects " \
        "ON projects.id = user_projects.project_id " \
        "WHERE user_projects.user_id = %s"
    cursor = mydb.cursor()
    cursor.execute(projects_query, (user_id,))
    projects = cursor.fetchall()
    cursor.close()
    # render table
    return render_template('tableUser.html', projects=projects)


@app.route('/user_project', methods=['POST'])
def user_project():
    """view for the user"""
    if request.method == 'POST':
        return render_template('projectsUser.html')


@app.route("/create_project", methods=['GET', 'POST'])
def create_projects():
    """get information from the form"""
    if request.method == "POST":
        project_id = str(uuid4())
        name = request.form['name']
        date = request.form['date']
        requirements = request.form['requirements']
        company_name = request.form['company_name']
        cursor = mydb.cursor()
        project_query = "INSERT INTO projects(id, name, date, " \
            "description, company_name) " \
            "VALUES (%s, %s, %s, %s, %s)"
        values = (project_id, name, date, requirements, company_name)
        cursor.execute(project_query, values)
        mydb.commit()
        cursor.close()
        return redirect(url_for("form_projects"))
    return redirect(url_for("form_projects"))


@app.route('/assign_project', methods=['GET', 'POST'])
def assign_project():
    """assigne project for the client"""
    if request.method == 'POST':
        assign_id = str(uuid4())
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
    return redirect(url_for('form_projects', users=users, projects=projects))


@app.route("/delete_project/", methods=['POST'])
def delete_project():
    """get information fron the form"""
    if request.method == 'POST':
        project_id = request.form['project_id']
        # create query for insert data
        cursor = mydb.cursor()
        delete_relations_query = "DELETE FROM relations " \
            "WHERE source_id IN (SELECT id " \
            "FROM activities " \
            "WHERE project_id = %s) " \
            "OR target_id IN (SELECT id " \
            "FROM activities " \
            "WHERE project_id = %s)"
        cursor.execute(delete_relations_query, (project_id, project_id))
        delete_user_projects_query = "DELETE FROM user_projects WHERE project_id = %s"
        cursor.execute(delete_user_projects_query, (project_id,))
        delete_actitivity_query = "DELETE FROM activities WHERE project_id = %s"
        cursor.execute(delete_actitivity_query, (project_id,))
        delete_project_query = "DELETE FROM projects WHERE id = %s"
        cursor.execute(delete_project_query, (project_id,))
        mydb.commit()
        cursor.close()
    return redirect(url_for('form_projects'))


@app.route('/create_activities/<project_id>', methods=['GET', 'POST'])
def create_activities(project_id):
    """render information for input to activities table"""
    if request.method == 'POST':
        activity_id = str(uuid4())
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        create_activities_query = "INSERT INTO activities" \
            "(id, name, date, description, project_id) " \
            "VALUES (%s, %s, %s, %s, %s)"
        cursor = mydb.cursor()
        values = (activity_id, name, date, description, project_id)
        cursor.execute(create_activities_query, values)
        mydb.commit()

        return redirect(url_for('create_activities', project_id=project_id))
    else:
        cursor = mydb.cursor()
        show_activities_query = "SELECT id, name FROM activities WHERE project_id = %s"
        cursor.execute(show_activities_query, (project_id,))
        activities = cursor.fetchall()
        mydb.commit()
        cursor.close()
        return render_template('createActivities.html', activities=activities, project_id=project_id)


@app.route('/create_relations', methods=['POST'])
def create_relations():
    """create relations for the activites table"""
    if request.method == 'POST':
        source_id = request.form['source_id']
        target_id = request.form['target_id']
        project_id = request.form['project_id']
        reation_id = str(uuid4())
        create_relations_query = "INSERT INTO relations (id, source_id, target_id) " \
            "VALUES (%s, %s, %s)"
        relation_values = (reation_id, source_id, target_id)
        cursor = mydb.cursor()
        cursor.execute(create_relations_query, relation_values)
        mydb.commit()
        cursor.close()
        return redirect(url_for('create_activities', project_id=project_id))


@app.route('/graph/<project_id>')
def create_graph(project_id):
    """get data for create a graph"""
    cursor = mydb.cursor()

    cursor.execute(
        f"SELECT * FROM activities WHERE project_id = '{project_id}'")
    data_activities = cursor.fetchall()
    cursor.execute(f"SELECT * FROM relations "
                   f"WHERE source_id IN (SELECT id FROM activities "
                   f"WHERE project_id = '{project_id}')")
    data_relations = cursor.fetchall()
    nodes = [{
        "data": {"id": activity[0], "name": activity[1], "date": activity[2].strftime('%y-%m-%d'),
                 "description": activity[3]}} for activity in data_activities]
    edges = [{"data": {"id": relation[0], "source": relation[1],
                       "target": relation[2]}} for relation in data_relations]
    graph = {"nodes": nodes, "edges": edges}
    cursor.close()
    return jsonify(graph)


def pagina_no_encontrada(error):
    """show error message"""
    return "<h1>La pagina no existe</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)

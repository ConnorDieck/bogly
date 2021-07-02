"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def redirect_users():
    """Redirect to users page"""

    return redirect("/users")

@app.route("/users")
def list_users():
    """List users and show form"""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.route('/users/new')
def show_add_user():
    """Show an add form for users"""

    return render_template("new-user.html")

@app.route('/users/new', methods=["POST"])
def process_add():
    """Processes the add form, adding a new user and going back to /users"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    url = request.form["img-url"]
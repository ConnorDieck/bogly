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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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
def show_add():
    """Show an add form for users"""

    return render_template("new-user.html")

@app.route('/users/new', methods=["POST"])
def process_add():
    """Processes the add form, adding a new user and going back to /users"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    url = request.form["img-url"]

    user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows information about given user"""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """Show the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit(user_id):
    """Process the edit form and return to users page"""

    user = User.query.get_or_404(user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    url = request.form["img-url"]

    print(f"HERE'S THE URL: {url}!!!!")

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = url

    # db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete the user"""
    
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')
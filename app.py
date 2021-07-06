"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

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
def show_add_user():
    """Show an add form for users"""

    return render_template("new-user.html")

@app.route('/users/new', methods=["POST"])
def process_add_user():
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
    posts = user.posts
    return render_template("detail.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_user_edit(user_id):
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

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows form to add post for given user"""

    user = User.query.get_or_404(user_id)

    return render_template("post-form.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def process_newpost(user_id):
    """Calculates form data to add post"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show specified post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post-detail.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit_form(post_id):
    """Show the edit page for a post"""

    post = Post.query.get_or_404(post_id)

    return render_template("edit-post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Process information from edit form and edit the post"""

    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.commit()    

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    user_id = post.user.id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')

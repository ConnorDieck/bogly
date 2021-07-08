"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag

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

    return render_template("add-user.html")

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
    return render_template("user-detail.html", user=user, posts=posts)

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
def add_post(user_id):
    """Shows form to add post for given user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("add-post.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def process_newpost(user_id):
    """Calculates form data to add post"""

    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")

    # Use .getlist() to extract list of tag ids from inputs with name "tags" and then form a list of associated tags 
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show specified post"""

    post = Post.query.get_or_404(post_id)

    tags = post.tags

    return render_template("post-detail.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit_form(post_id):
    """Show the edit page for a post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit-post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Process information from edit form and edit the post"""

    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    # Use .getlist() to extract list of tag ids from inputs with name "tags" and then form a list of associated tags 
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.tags = tags

    db.session.commit()    

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes given post"""

    post = Post.query.get_or_404(post_id)

    user_id = post.user.id

    # Currently no way to delete a post associated with a tag. If this is tried, flash an error message and redirect to the tag detail page
    try:
        Post.query.filter(Post.id == post_id).delete()
        db.session.commit()
    except:
        flash('This post is associated with a tag(s). Try removing it from its posts and then deleting.')
        return redirect(f'/posts/{post_id}')

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def show_tags():
    """Shows all tags"""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Shows details of one tag"""

    tag = Tag.query.get(tag_id)

    return render_template('tag-detail.html', tag=tag)

@app.route('/tags/new')
def add_tag():
    """Shows add tag form"""

    tags = Tag.query.all()

    return render_template('add-tag.html', tags=tags)

@app.route('/tags/new', methods=["POST"])
def process_tag_add():
    """Sends new tag to the database and redirects to tag list"""

    name = request.form["name"]

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Shows edit tag form"""

    tag = Tag.query.get(tag_id)

    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def process_tag_edit(tag_id):
    """Processes edit tag form and redirects to tags list"""

    name = request.form["name"]
    tag = Tag.query.get(tag_id)

    tag.name = name

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Deletes given tag"""

    # Currently no way to delete a tag associated with a post. If this is tried, flash an error message and redirect to the tag detail page
    try:
        Tag.query.filter(Tag.id == tag_id).delete()
        db.session.commit()
    except:
        flash('This tag is associated with a post(s). Try removing it from its posts and then deleting.')
        return redirect(f'/tags/{tag_id}')

    return redirect(f'/tags/{tag_id}')
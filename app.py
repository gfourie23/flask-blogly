"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

debug = DebugToolbarExtension(app)


db.create_all()

@app.route('/')
def root():
    """Homepage redirect to users list."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 error"""

    return render_template("404.html"), 404

@app.route('/users')
def users_list():
    """Show page with users"""
    users = User.query.order_by(User.last_name, User.first_name).all
    return render_template('users/users.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show new user form"""
    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def users_new():
    """Form submission to create a new user"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def user_show(user_id):
    """Show page with user info"""
    user = User.query.gett_or_404(user_id)
    return render_template('users/details.html', user=user)

@app.route('users/int:user_id>/edit')
def users_edit(user_id):
    """Show form to edit a user's details"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission to update user details."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get_ot_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# >>>>>>>>>>>> Blogly Part 2 >>>>>>>>>>>>>>>>>>>>>>>>

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Display form for user to add a new post."""
    user = User.query.get_or_404(user_id)
    return render_template("post/post-form.html", user=user)

@app.route('users/<int:user_id>/posts/new', methods=["POST"])
def add_post_to_user(user_id):
    """Handle add form, add post, redirect to user details page."""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form["title"],      content=request.form["content"], user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post with buttons to edit and delete."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/new.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit post and cancel it"""
    post = User.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_update(post_id):
    """Handle editing of post and redirect to post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


############### Part 3 #####################################

@app.route('/tags')
def list_tags():
    """List all tags with links to tag detail page."""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
    """Shows a form to add a new tag."""
    posts = Post.query.all()
    return render_template('tags/tag-create.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def add_tag_form():
    """Process add form, add tag, and redirect to tag list."""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show detail about a tag with links to edit or delete form."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag-details.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    
    return render_template('tags/tag-edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):
    """Process edit form, edit tag, and redirect to tags list."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
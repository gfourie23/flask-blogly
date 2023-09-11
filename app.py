"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

debug = DebugToolbarExtension(app)


db.create_all()

@app.route('/')
def homepage():
    """Homepage redirect to users list."""
    return redirect("/users")

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
    return render_template('users/show.httml', user=user)

@app.route('users/int:user_id>/edit')
def users_edit(user_id):
    """Show form to edit a user's details"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:users_id>/edit', methods=["POST"])
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

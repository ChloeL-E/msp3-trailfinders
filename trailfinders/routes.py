from flask import render_template, request, redirect, url_for
from trailfinders import app, db
from trailfinders.models import User, Hike, Category
import flask_login as fl

login_manager = fl.LoginManager(app)


# load current user
@login_manager.user_loader
def get_user(id):
    """
    Function to load the current user.

    Arguments:
        id- the primary key on the User table.

    Returns:
        A user object from a query on user table.
    """
    return User.query.get(int(id))


# home page
@app.route("/")
def home():
    """
    Home function

    Returns:
        Renders the template for the home page.
    """
    return render_template("index.html")


# register.html
def register():
    """
    Registers new user

    Checks user not already registered by checking 
    that the username and email not already stored in db.
    Flashed messages will keep the user informed.

    Returns:
        If user is already registered, redirect to login page.
        Else will add new user in db and redirect to profile page.
    """


# login.html
def login():
    """
    Login user

    Checks user is registered by checking username exists and if it does,
    check that password is correct.

    Returns:
        If both correct, will redirect to profile page.
        If incorrect, will redirect to login page with flashed message.
        If username does not exist will redirect to register page with flashed message.
    """


# logout
def logout():
    """
    Function which clears the session user.
    Flashed message to inform user they are logged out
    """
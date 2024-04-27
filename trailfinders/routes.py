from flask import render_template, request, redirect, url_for
from trailfinders import app, db
from trailfinders.models import User, Hike, Category
import flask_login as fl

login_manager = fl.LoginManager(app)

@login_manager.user_loader
def get_user(id):
    """
    Loads the current user

    Arguments: 
        id- the primary key on the User table

    Returns:
        A user object from a query on user table
    """
    return User.query.get(int(id))



@app.route("/")
def home():
    return render_template("index.html")

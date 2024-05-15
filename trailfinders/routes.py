from flask import (render_template, request, redirect, url_for, flash, session)
from werkzeug.security import generate_password_hash, check_password_hash
from trailfinders import app, db
from trailfinders.models import User, Hike, Category
import flask_login as fl
from flask_login import LoginManager


# Flask_Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# load current user
@login_manager.user_loader
def load_user(user_id):
    """
    Function to load the current user.

    Arguments:

        id- the primary key on the User table.

    Returns:
        A user object from a query on user table.
        Flask stores the data in session.
    """
    return User.query.get(int(user_id))


# index.html
@app.route("/")
def home():
    """
    Home function.

    Returns:
        Renders the template for the home page.
    """
    return render_template("index.html")


# register.html
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Function to register a new user.

    Checks username not already in use.
    Flashed messages will keep the user informed.
    If username not already in use will create new user instance

    Returns:
        Registers new user.
    """

    if request.method == "POST":
        # Checking to see if username already exists
        username = request.form.get('username').lower()
        user_exists = User.query.filter_by(username=username).first()
        # is username exists, redirect user to register
        if user_exists:
            flash("This username already exists")
            return redirect(url_for("register"))
        # Create a new instance of a user
        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'))
        )

        # Add new user instance into db
        db.session.add(new_user)
        db.session.commit()

        # Inform user that the registration was successful,
        # Redirect to login page
        flash("Fantastic! You're now registered, please login")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Function to login the user
    Checks user is registered by checking username exists and if it does,
    check that password is correct.

    Returns:
       If both correct, will redirect to profile page.
       If incorrect, will redirect to login page with flashed message.
       If username does not exist will redirect to register page with flashed
       message.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("Received username:", username)
        print("Received password:", password)

        if not (username and password):
            # Username &/or password is missing
            flash("Please enter a username and password")
            return redirect(url_for("login"))  # Redirect to login page

        existing_user = User.query.filter_by(username=username.lower()).first()

        if existing_user:
            if check_password_hash(existing_user.password, password):
                # Storing username in lowercase
                session["user"] = username.lower()
                flash(f"{username}, you're now logged in. Happy Hiking")
                return redirect(url_for("home", username=session["user"]))
            else:
                # Incorrect password, redirect to login
                flash("Invalid username and/or password, please try again")
                return redirect(url_for("login"))  # redirect to login
        else:
            # Username does not exist
            flash("Username not found, please register")
            return redirect(url_for("register"))  # Redirect to register page

    return render_template("login.html")


# logout.html
@app.route("/signout")
@fl.login_required
def logout():
    """
    Function which clears the session user.
    Redirect logged out user to home page.
    """
    fl.logout_user()  # logout user
    flash("You have successfully logged out. Come visit us again soon!")
    return render_template("logout.html")  # Redirect to home

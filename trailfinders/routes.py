from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
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
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registers new user

    Checks username not already in use.
    Flashed messages will keep the user informed.

    Returns:
        Registers new user.
    """

    if request.method == "POST":
        # Checking to see if username already exists
        existing_user = User.query.filter(User.username == request.form.get
                                          ('username').lower().all())

        if existing_user:
            flash("This username already exisits")
            return redirect(url_for("register.html"))
        # Create a new instance of a user
        new_user = User(
            username=request.form('username'),
            email=request.form('email'),
            pwd=generate_password_hash(request.form('password'))
        )

        # Add new user instance into db
        db.session.add(new_user)
        db.session.commit()

        # Inform user that the registration was successful,
        # Redirect to login page
        flash("Fantastic! You're now registered, please login")
        return render_template(url_for("login.html"))

    return render_template(url_for("register.html"))


# login.html
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login user

    Checks user is registered by checking username exists and if it does,
    check that password is correct.

    Returns:
        If both correct, will redirect to profile page.
        If incorrect, will redirect to login page with flashed message.
        If username does not exist will redirect to register page with flashed
        message.
    """
    if request.method == "POST":
        username = request.form('username')
        pwd = generate_password_hash(request.form('password'))
        user = User.query.filter(User.username == request.form.get('username')
                                 .lower().all())
        if username and pwd:
            fl.login_user(user)
            flash(f"Welcome {'username'}, you're logged in. Happy Hiking!")
            return redirect(url_for("home"))
        else:
            flash()
            return render_template("login.html")
    else:
        return render_template("login.html")


# logout
def logout():
    """
    Function which clears the session user.
    Redirect logged out user to home page.
    """
    session.clear()
    return redirect(url_for("home"))

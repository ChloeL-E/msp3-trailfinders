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
        Flask stores the data in session.
    """
    return User.query.get(int(id))


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
    Registers new user.

    Checks username not already in use.
    Flashed messages will keep the user informed.

    Returns:
        Registers new user.
    """

    if request.method == "POST":
        # Checking to see if username already exists
        existing_user = User.query.filter(User.username == request.form.get
                                          ('username').lower().all())
        # is username exists, redirect user to register
        if existing_user:
            flash("This username already exists")
            return redirect(url_for("register"))
        # Create a new instance of a user
        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            pwd=generate_password_hash(request.form.get('password'))
        )

        # Add new user instance into db
        db.session.add(new_user)
        db.session.commit()

        # Inform user that the registration was successful,
        # Redirect to login page
        flash("Fantastic! You're now registered, please login")
        return render_template(url_for("login"))

    return render_template("register.html")


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
        # Get username and password from request form
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username.lower()).first()
        # Check if username and password are correct
        if username and check_password_hash(user.password, password):
            fl.login_user(user)  # login user
            flash(f"Welcome {username}, you're logged in. Happy Hiking!")
            return redirect(url_for("home"))
        else:
            # Incorrect, redirect to login
            flash("Invalid username and/or password, please try again")
            return render_template("login.html")
    else:
        return render_template("login.html")


# logout.html
@app.route("/logout")
@fl.login_required
def logout():
    """
    Function which clears the session user.
    Redirect logged out user to home page.
    """
    fl.logout_user()  # logout user
    flash("You have successfully logged out. Come visit us again soon!")
    return redirect(url_for("home"))  # Redirect to home

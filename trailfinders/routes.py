from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from trailfinders import app, db
from trailfinders.models import User, Hike, Category
import flask_login as fl

login_manager = fl.LoginManager(app)


# index.html
@app.route("/")
def home():
    """
    Home function.

    Returns:
        Renders the template for the home page.
    """
    return render_template("index.html")


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
        existing_user = User.query.filter(User.username == request.form.get('username').lower()).first()
        
        # If username exists, redirect user to register
        if existing_user:
            flash("This username already exists")
            return redirect(url_for("register"))
        
        try:
            # Create a new instance of a user
            new_user = User(
                username=request.form.get('username'),
                email=request.form.get('email'),
                pwd=generate_password_hash(request.form.get('password'))
            )

            # Add new user instance into db session
            db.session.add(new_user)
            db.session.commit()  # Commit changes to persist them

            # Inform user that the registration was successful,
            # Redirect to login page
            flash("Fantastic! You're now registered, please login")
            return redirect(url_for("login"))

        except Exception as e:
            # Rollback changes in case of error
            db.session.rollback()
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for("register"))

    return render_template("register.html")



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

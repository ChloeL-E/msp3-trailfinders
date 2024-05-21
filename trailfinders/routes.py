from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from trailfinders import app, db
from trailfinders.models import User, Hike, Category


# index.html
@app.route("/")
def home():
    """
    Home function.

    Returns:
        Renders the template for the home page.
    """
    hikes = list(Hike.query.order_by(Hike.hike_title).all())
    return render_template("index.html", hikes=hikes)


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

        if not (username and password):
            # Username &/or password is missing
            flash("Please enter a username and password")
            return redirect(url_for("login"))  # Redirect to login page

        existing_user = User.query.filter_by(username=username.lower()).first()
        if existing_user and check_password_hash(existing_user.password,
                                                 password):
            # Storing username in lowercase
            flash(f"{username}, you're now logged in. Happy Hiking")
            return redirect(url_for("home", username=username))  # ['user']
        else:
            # Incorrect password, redirect to login
            flash("Invalid username and/or password, please try again")
            return redirect(url_for("login"))  # redirect to login

    return render_template("login.html")


# logout.html
@app.route("/logout")
def logout():
    """
    Function which clears the session user.
    Redirect logged out user to home page.
    """
    session.clear()
    return redirect(url_for("home"))  # Redirect to home


#  category.html
@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


# add a new category
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        # Get the current user
        current_user = User.query.filter_by(username=session["user"]).first()
        # Get the category name from the form
        category_name = request.form.get("category_name")
        # Create a new category with the current user's ID
        category = Category(category_name=category_name,
                            created_by=current_user.id)
        # Add new category instance into db
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


#  edit a category
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


#  delete a category
@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"])
def delete_category(category_id):
    current_user = User.query.filter_by(username=session["user"]).first()
    category = Category.query.get_or_404(category_id)
    #  defensive programming to prevent other users deleting category
    if current_user.id != category.created_by:
        flash("You do not have permission to delete this category")
        return redirect(url_for("categories"))
    else:
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted successfully!")
        return redirect(url_for("categories"))


#  my_hikes
@app.route("/my_hikes")
def my_hikes():
    hikes = list(Hike.query.order_by(Hike.hike_title).all())
    return render_template("my_hikes.html", hikes=hikes)


#  add a new hike
@app.route("/add_hike", methods=["GET", "POST"])
def add_hike():
    # list of all the categories from the db
    categories = list(Category.query.order_by(Category.category_name).all())
    # Get the current user
    current_user = User.query.filter_by(username=session["user"]).first()
    if request.method == "POST":
        # Create a new Hike object using form data and existing category
        category_id = request.form.get("category_id")
        category = Category.query.get(category_id)
        if category is None:
            flash("Selected category does not exist.")
            return redirect(url_for("add_hike"))  # Redirect back to add_hike
        # Create a new Hike object using form data and existing category
        hike = Hike(
            hike_title=request.form.get("hike_title"),
            image_url=request.form.get("image_url"),
            distance=request.form.get("distance"),
            elevation=request.form.get("elevation"),
            difficulty=request.form.get("difficulty"),
            description=request.form.get("description"),
            category_id=category_id,
            user_id=current_user.id  # Assign the current user's ID
        )
        # Add new category instance into db
        db.session.add(hike)
        db.session.commit()
        return redirect(url_for("my_hikes"))
    return render_template("add_hike.html", categories=categories)


#  edit a hike
@app.route("/edit_hike/<int:hike_id>", methods=["GET", "POST"])
def edit_hike(hike_id):
    # list of all the categories from the db
    categories = list(Category.query.order_by(Category.category_name).all())
    # Get the current user
    current_user = User.query.filter_by(username=session["user"]).first()
    hike = Hike.query.get_or_404(hike_id)
    if request.method == "POST":
        hike.hike_title = request.form.get("hike_title")
        hike.image_url = request.form.get("image_url")
        hike.distance = request.form.get("distance")
        hike.elevation = request.form.get("elevation")
        hike.difficulty = request.form.get("difficulty")
        hike.description = request.form.get("description")
        hike.category_id = request.form.get("category_id")
        hike.user_id = current_user.id  # Assign the current user's ID
        db.session.commit()
        return redirect(url_for("my_hikes"))
    return render_template("edit_hike.html",
                           hike=hike, categories=categories)


#  delete a hike
@app.route("/delete_hike/<int:hike_id>", methods=["GET", "POST"])
def delete_hike(hike_id):
    current_user = User.query.filter_by(username=session["user"]).first()
    hike = Hike.query.get_or_404(hike_id)
    #  defensive programming to prevent other users deleting category
    if current_user.id != hike.user.id:
        flash("You do not have permission to delete this category")
        return redirect(url_for("my_hikes"))
    else:
        hike = Hike.query.get_or_404(hike_id)
        db.session.delete(hike)
        db.session.commit()
        flash("Hike deleted successfully!")
        return redirect(url_for("my_hikes"))

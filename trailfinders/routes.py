from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from trailfinders import app, db
from trailfinders.models import User, Hike, Category


# Home
@app.route("/")
def home():
    """
    Home function

    Returns:
    Renders the template for the home page
    """
    hikes = list(Hike.query.order_by(Hike.hike_title).all())
    return render_template("index.html", hikes=hikes)


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Function to register a new user

    Checks username not already in use
    Flashed messages will keep the user informed
    If username not already in use will create new user instance

    Returns:
        Registers new user
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
            #  username=request.form.get('username'),
            username=username,
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


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Function to login the user
    Checks user is registered by checking username exists and if it does,
    check that password is correct

    Returns:
       If both correct, will redirect to profile page
       If incorrect, will redirect to login page with flashed message
       If username does not exist will redirect to register page with flashed
       message
    """
    if request.method == "POST":
        # Get username and password inputs from form
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            # Username &/or password is missing
            flash("Please enter a username and password")
            return redirect(url_for("login"))  # Redirect to login page
        # Checks for existing user with username
        existing_user = User.query.filter_by(username=username.lower()).first()
        if existing_user and check_password_hash(existing_user.password,
                                                 password):
            # Storing username in session
            session['user'] = username
            session['user_id'] = existing_user.id
            # Storing username in lowercase
            return redirect(url_for("home", username=username))
        else:
            # Incorrect password, redirect to login
            flash("Invalid username and/or password, please try again")
            return redirect(url_for("login"))

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    """
    Function which clears the session user
    Redirect logged out user to home page
    """
    session.clear()
    return redirect(url_for("home"))  # Redirect to home


#  Category
@app.route("/categories")
def categories():
    """
    Gets the list of categories by name
    Renders the category template
    """
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


# Add a new category
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    Function to add a category
    Gets the current user, the category name from the form and creates a new
    category with the users id
    Adds to the Category db
    Redirects user to categories page
    """
    if request.method == "POST":
        # Get the current user and the catgeory name from the form
        current_user = User.query.filter_by(username=session["user"]).first()
        category_name = request.form.get("category_name")
        # Create a new category with the current user's ID
        category = Category(category_name=category_name,
                            created_by=current_user.id)
        # Add new category instance into db
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


#  Edit a category
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """
    Function to edit a category
    Gets the category by category id and requests the category name from the
    form
    Commits to db
    Redirect logged out user to categories
    """
    category = Category.query.get_or_404(category_id)
    current_user = User.query.filter_by(username=session["user"]).first()
    # Defensive programming- only creator of post can edit
    if current_user.id != category.created_by:
        flash("You do not have permission to edit this category")
        return redirect(url_for("categories"))
    if request.method == "POST":
        # get the catgeory name from the form, update category name and commit
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


#  Delete a category
@app.route("/delete_category/<int:category_id>", methods=["GET", "POST"])
def delete_category(category_id):
    """
    Function to delete a category
    Defines variables for current user-username and category-category id
    Flash message if user trying to delete another users post
    Requests the category name from the form
    Commits to db
    Redirect user to Categories page
    """
    current_user = User.query.filter_by(username=session["user"]).first()
    category = Category.query.get_or_404(category_id)
    #  defensive programming to prevent other users deleting category
    # if current user did not create post, unable to delete, flash message
    if current_user.id != category.created_by:
        flash("You do not have permission to delete this category")
        return redirect(url_for("categories"))
    else:
        # get the category, delete it and commit changes to db
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted successfully!")
        return redirect(url_for("categories"))


#  Hikes
@app.route("/my_hikes")
def my_hikes():
    """
    Function to get a list of hikes
    Renders Hikes page
    """
    hikes = list(Hike.query.order_by(Hike.hike_title).all())
    return render_template("my_hikes.html", hikes=hikes)


#  Add a new hike
@app.route("/add_hike", methods=["GET", "POST"])
def add_hike():
    """
    Function to add a hike
    Gets the current user, a list of the category names from the db,
    gets the category id and name from the form
    Creates a new Hike object and commits to db
    Renders Hikes page
    """
    # list of all the categories from the db
    categories = list(Category.query.order_by(Category.category_name).all())
    # Get the current user
    current_user = User.query.filter_by(username=session["user"]).first()
    if request.method == "POST":
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


#  Edit a hike
@app.route("/edit_hike/<int:hike_id>", methods=["GET", "POST"])
def edit_hike(hike_id):
    """
    Function to edit a hike
    Gets a list of the categories and gets hike_id from db
    Gets the current user
    Handles POST request, updates hike details and commits chanegs to db
    Redirects user to Hike page
    """
    # list of all the categories from the db
    categories = list(Category.query.order_by(Category.category_name).all())
    # Get the current user
    current_user = User.query.filter_by(username=session["user"]).first()
    hike = Hike.query.get_or_404(hike_id)
    if request.method == "POST":
        # get the data from the form inputs
        hike.hike_title = request.form.get("hike_title")
        hike.image_url = request.form.get("image_url")
        hike.distance = request.form.get("distance")
        hike.elevation = request.form.get("elevation")
        hike.difficulty = request.form.get("difficulty")
        hike.description = request.form.get("description")
        hike.category_id = request.form.get("category_id")
        hike.user_id = current_user.id  # Assign the current user's ID
        db.session.commit()  # commit changes to DB
        return redirect(url_for("my_hikes"))
    return render_template("edit_hike.html",
                           hike=hike, categories=categories)


#  Delete a hike
@app.route("/delete_hike/<int:hike_id>", methods=["GET", "POST"])
def delete_hike(hike_id):
    """
    Function to delete a hike
    Defines variables for current user(username) and category(category id)
    Flash message if user trying to delete another users hike post
    Requests the hike name from the form
    Commits to db
    Redirect logged out user to Hikes page
    """
    current_user = User.query.filter_by(username=session["user"]).first()
    hike = Hike.query.get_or_404(hike_id)
    #  defensive programming to prevent other users deleting hike
    if current_user.id != hike.user.id:
        flash("You do not have permission to delete this Hike")
        return redirect(url_for("my_hikes"))
    else:
        # get the hike by ID if available, delete and commit to DB
        hike = Hike.query.get_or_404(hike_id)
        db.session.delete(hike)
        db.session.commit()
        flash("Hike deleted successfully!")
        return redirect(url_for("my_hikes"))


# Guidance on Error handlers taken from Geeks for Geeks
# 404
@app.errorhandler(404)
def handle_404(e):
    """
    Handles 404 error, Page not Found
    """
    return render_template("404.html"), 404


# 500
@app.errorhandler(500)
def handle_500(e):
    """
    Handles 500 error, Internal server error
    """
    return render_template("500.html"), 500

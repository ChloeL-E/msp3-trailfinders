from trailfinders import db


class User(db.Model):
    """
    schema for User model
    """
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)


class Hike(db.Model):
    """
    schema for Category model
    """ 
    hike_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    distance = db.Column(db.String, nullable=False)
    elevation = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category_id = db.Column(db.String, nullable=False, foreign_key=True)

    class Category(db.Model):
        """
        schema for Category model
        """
        category_id = db.Column(db.Integer, primary_key=True)
        type = db.Column(db.String, nullable=False)

from trailfinders import db


class User(db.Model):
    """
    schema for User model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    hike_id = db.Column(db.Integer, db.ForeignKey(
        "hike.id", ondelete="CASCADE"), nullable=False)
    hike = db.relationship(
        'Hike', backref='user', cascade="all, delete")

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.user


class Hike(db.Model):
    """
    schema for Category model
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    distance = db.Column(db.String, nullable=False)
    elevation = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Title: {1} | Distance: {2}" | "Difficulty:{3}".format(
            self.id, self.title, self.distance, self.difficulty
        )


class Category(db.Model):
    """
    schema for Category model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.name

from trailfinders import db


class User(db.Model):
    """
    schema for User model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(63), nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    hikes = db.relationship('Hike', backref='user', cascade="all, delete")

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.username


class Hike(db.Model):
    """
    schema for Hike model
    """
    id = db.Column(db.Integer, primary_key=True)
    hike_title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String(255))  # store the url of the image
    distance = db.Column(db.String, nullable=False)
    elevation = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    #  foreign key to link users- refer to user pk
    user_id = db.Column(db.Integer, db.ForeignKey
                        ("user.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey
                            ("category.id", ondelete="CASCADE"),
                            nullable=False)
    category = db.relationship('Category', backref=db.backref
                               ('hikes', lazy=True))

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Title: {1} | Distance: {2} | Difficulty: {3}".format(
            self.id, self.title, self.distance, self.difficulty)


class Category(db.Model):
    """
    schema for Category model
    """
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    hike = db.relationship(
        'Hike', backref='categories', cascade="all, delete")

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.category_name

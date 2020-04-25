"""This is an example of a model, containing a few fields. Use this as a blueprint of your future models.

The tablename tag is used for defining the name of the model in the database. The fields contains the information that
you want to store in the model.

The __init__ function is used by flask to initialize each model instance when you create it. It will be transform the
values you send to the model blueprint into a model instance.

The __repr__ function wil return the ID of the model instance, useful for queries and sorting

The serialize function is needed for placing the now created model instance into the database. It wil give the output
too the flask framework, which will handle the database actions."""

from app import db


class ViewPoint(db.Model):
    __tablename__ = 'ViewPoint'

    ID = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    rating = db.Column(db.Float)
    image = db.Column(db.String)
    numberOfRatings = db.Column(db.Integer)
    type = db.Column(db.String)

    def __init__(self, title, lat, long, type, image=None):
        self.title = title
        self.lat = lat
        self.long = long
        self.image = image
        self.rating = 0
        self.numberOfRatings = 0
        self.type = type

    def __repr__(self):
        return '<ID {}>'.format(self.ID)

    def serialize(self):
        return {
            'ID': self.ID,
            'title': self.title,
            'lat': self.lat,
            'long': self.long,
            'rating': self.rating,
            'numberOfRatings': self.numberOfRatings,
            'type': self.type,
            'image_name': self.image
        }


class ViewPointInfo():

    ID = 1
    title = "hei"
    lat = 432
    long = 432
    rating = 3
    numberOfRatings = 1
    type = 'Natur'

    def __init__(self, ID, title, lat, long, rating, numberOfRatings, type):
        self.ID = ID
        self.title = title
        self.lat = lat
        self.long = long
        self.rating = rating
        self.numberOfRatings = numberOfRatings
        self.type = type

    def __repr__(self):
        return '<id {}>'.format(self.ID)

    def serialize(self):
        return {
            'ID': self.ID,
            'title': self.title,
            'lat': self.lat,
            'long': self.long,
            'rating': self.rating,
            'numberOfRatings': self.numberOfRatings,
            'type': self.type,
        }


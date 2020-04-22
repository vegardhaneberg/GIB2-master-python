"""This is an example of a model, containing a few fields. Use this as a blueprint of your future models.

The tablename tag is used for defining the name of the model in the database. The fields contains the information that
you want to store in the model.

The __init__ function is used by flask to initialize each model instance when you create it. It will be transform the
values you send to the model blueprint into a model instance.

The __repr__ function wil return the ID of the model instance, useful for queries and sorting

The serialize function is needed for placing the now created model instance into the database. It wil give the output
too the flask framework, which will handle the database actions."""

from app import db


class Model(db.Model):
    __tablename__ = 'Model'

    ID = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    startdate = db.Column(db.TIMESTAMP)
    enddate = db.Column(db.TIMESTAMP)

    def __init__(self, title, description, startdate, enddate):
        self.title = title
        self.description = description
        self.startdate = startdate
        self.enddate = enddate

    def __repr__(self):
        return '<ID {}>'.format(self.ID)

    def serialize(self):
        return {
            'ID': self.ID,
            'title': self.title,
            'description': self.description,
            'startdate': self.startdate,
            'enddate': self.enddate,
        }


class ViewPoint(db.Model):
    __tablename__ = 'ViewPoint'

    ID = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    date = db.Column(db.TIMESTAMP)
    rating = db.Column(db.Float)
    image = db.Column(db.String)
    numberOfRatings = db.Column(db.Integer)

    def __init__(self, title, lat, long, date=None, image=None):
        self.title = title
        self.lat = lat
        self.long = long
        self.date = date
        self.image = image
        self.rating = 0
        self.numberOfRatings = 0

    def __repr__(self):
        return '<ID {}>'.format(self.ID)

    def serialize(self):
        return {
            'ID': self.ID,
            'title': self.title,
            'lat': self.lat,
            'long': self.long,
            'date': self.date,
            'image_name': self.image,
            'rating': self.rating,
            'numberOfRatings': self.numberOfRatings
        }

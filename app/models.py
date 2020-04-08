"""This is an example of a model, containing a few fields. Use this as a blueprint of your future models.

The tablename tag is used for defining the name of the model in the database. The fields contains the information that
you want to store in the model.

The __init__ function is used by flask to initialize each model instance when you create it. It will be transform the
values you send to the model blueprint into a model instance.

The __repr__ function wil return the ID of the model instance, useful for queries and sorting

The serialize function is needed for placing the now created model instance into the database. It wil give the output
too the flask framework, which will handle the database actions."""

from app import db


class model(db.Model):
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


class veiwPoint(db.Model):
    __tablename__ = 'veiwPoint'

    ID = db.Column(db.Integer, primary_key=True, index=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    date = db.Column(db.TIMESTAMP)

    def __init__(self, lat, long, date):
        self.lat = lat
        self.long = long
        self.date = date

    def __repr__(self):
        return '<ID {}>'.format(self.ID)

    def serialize(self):
        return {
            'ID': self.ID,
            'title': self.title,
            'lat': self.lat,
            'long': self.long
        }

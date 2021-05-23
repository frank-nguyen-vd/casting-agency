from flask_sqlalchemy import SQLAlchemy

from database import db


class Movies(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime(120))

    def __repr__(self):
        return "<Movies: {}, {}, {}>".format(self.id, self.title, self.release_date)

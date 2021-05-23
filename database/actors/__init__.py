from flask_sqlalchemy import SQLAlchemy

from database import db


class Actors(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    gender = db.Column(db.String)

    def __repr__(self):
        return "<Actors: {}, {}, {}, {}>".format(
            self.id, self.name, self.age, self.gender
        )

import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import json

db = SQLAlchemy()


def setup_db(app, database_path=None):
    testdb_url = "postgres://postgres:postgres@localhost:5432/testdb"

    load_dotenv()
    if database_path is not None:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    elif "DATABASE_URL" in os.environ:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    elif "DEFAULT_DATABASE_URL" in os.environ:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DEFAULT_DATABASE_URL"]
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = testdb_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)
    db.create_all()

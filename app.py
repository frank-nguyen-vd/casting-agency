from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS


from database import setup_db
from database.movies import Movies
from database.actors import Actors
from auth import requires_auth


def create_app():
    load_dotenv()
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route("/")
    def index():
        return "Welcome to API"

    @app.route("/movies")
    @requires_auth("read:movies")
    def get_movies(payload):
        obj_list = Movies.query.all()
        str_list = [str(obj) for obj in obj_list]
        return jsonify({"success": True, "data": str_list})

    @app.route("/actors")
    def get_actors():
        obj_list = Actors.query.all()
        str_list = [str(obj) for obj in obj_list]
        return jsonify({"success": True, "data": str_list})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

from flask import Flask, jsonify, redirect, request
from dotenv import load_dotenv
from flask_cors import CORS
from flasgger import Swagger, swag_from
from icecream import ic


from database import setup_db
from database.movies import Movies
from database.actors import Actors
from auth import requires_auth, AuthError


class ResourceError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def paginate(itemsList=[], page=1, size=10):
    startIndex = (page - 1) * size
    endIndex = startIndex + size
    if startIndex >= len(itemsList):
        raise ResourceError(
            {
                "code": "resource_not_found",
                "description": "The requested page does not contain any record",
            },
            404,
        )
    selectedItems = [item.format() for item in itemsList[startIndex:endIndex]]
    return selectedItems


def create_app(database_path=None):
    load_dotenv()
    app = Flask(__name__)
    setup_db(app, database_path)
    CORS(app)
    swagger = Swagger(app)

    @app.route("/")
    def index():
        return redirect("/apidocs")

    @app.route("/movies")
    @requires_auth("read:movies")
    @swag_from("api_doc/get_movies.yml")
    def get_movies(payload):
        page = request.args.get("page", 1, type=int)
        size = request.args.get("size", 10, type=int)
        itemsList = Movies.query.order_by(Movies.id).all()
        selectedItems = paginate(itemsList, page, size)
        return jsonify(
            {
                "success": True,
                "movies": selectedItems,
                "page": page,
                "total": len(itemsList),
            }
        )

    @app.route("/actors")
    @requires_auth("read:actors")
    @swag_from("api_doc/get_actors.yml")
    def get_actors(payload):
        page = request.args.get("page", 1, type=int)
        size = request.args.get("size", 10, type=int)
        itemsList = Actors.query.order_by(Actors.id).all()
        selectedItems = paginate(itemsList, page, size)
        return jsonify(
            {
                "success": True,
                "actors": selectedItems,
                "page": page,
                "total": len(itemsList),
            }
        )

    @app.route("/actors", methods=["POST"])
    @requires_auth("create:actors")
    @swag_from("api_doc/create_actors.yml")
    def create_actors(payload):
        pass

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return (
            jsonify({"success": False, "error": error.error}),
            error.status_code,
        )

    @app.errorhandler(ResourceError)
    def handle_resource_error(error):
        return (
            jsonify({"success": False, "error": error.error}),
            error.status_code,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

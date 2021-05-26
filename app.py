from flask import Flask, jsonify, redirect, request, abort
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


class RequestError(Exception):
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
        reqBody = request.get_json()
        if reqBody is None:
            raise RequestError(
                {"code": "empty_content", "description": "No actor details provided"},
                400,
            )

        name = reqBody.get("name")
        age = reqBody.get("age")
        gender = reqBody.get("gender")

        if name is None or age is None or gender is None:
            raise RequestError(
                {"code": "missing_field", "description": "Missing actor details"},
                400,
            )

        if type(name) is not str or type(age) is not int or type(gender) is not str:
            raise RequestError(
                {"code": "invalid_format", "description": "Invalid actor details"},
                400,
            )
        try:
            actor = Actors(name, age, gender)
            actor.insert()
        except:
            abort(500)

        return jsonify({"success": True, "actor": actor.format()})

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("update:actors")
    @swag_from("api_doc/update_actors.yml")
    def update_actors(payload, id):
        reqBody = request.get_json()
        if reqBody is None:
            raise RequestError(
                {"code": "empty_content", "description": "No actor details provided"},
                400,
            )

        name = reqBody.get("name")
        age = reqBody.get("age")
        gender = reqBody.get("gender")

        if name is None and age is None and gender is None:
            raise RequestError(
                {"code": "empty_content", "description": "No actor details provided"},
                400,
            )

        try:
            actor = Actors.query.get(id)
        except:
            raise RequestError(
                {"code": "not_found", "description": "No such an actor found"},
                404,
            )

        if name is not None:
            if type(name) is not str:
                raise RequestError(
                    {"code": "invalid_format", "description": "Invalid actor details"},
                    400,
                )
            actor.name = name
        if age is not None:
            if type(age) is not int:
                raise RequestError(
                    {"code": "invalid_format", "description": "Invalid actor details"},
                    400,
                )
            actor.age = age
        if gender is not None:
            if type(gender) is not str:
                raise RequestError(
                    {"code": "invalid_format", "description": "Invalid actor details"},
                    400,
                )
            actor.gender = gender

        try:
            actor.update()
        except:
            abort(500)

        return jsonify({"success": True, "actor": actor.format()})

    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    @swag_from("api_doc/delete_actors.yml")
    def delete_actors(payload, id):
        actor = Actors.query.get(id)
        if actor is None:
            raise RequestError(
                {"code": "not_found", "description": "Actor not found"},
                404,
            )

        try:
            actor.delete()
        except:
            abort(500)

        return jsonify({"success": True, "deleted": id})

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

    @app.errorhandler(RequestError)
    def handle_request_error(error):
        return (
            jsonify({"success": False, "error": error.error}),
            error.status_code,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal server error"}
            ),
            500,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

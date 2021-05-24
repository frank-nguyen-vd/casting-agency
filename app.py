from flask import Flask, jsonify, redirect, request
from dotenv import load_dotenv
from flask_cors import CORS
from flasgger import Swagger
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
    def get_movies(payload):
        """Get a paginated list of movies
        ---
        tags:
            - Movies

        definitions:
            Movies:
                type: object
                properties:
                    title:
                        type: string
                    release_date:
                        type: string
        parameters:
            -   in: query
                name: page
                type: integer
                default: 1
                description: the page number of the paginated result
            -   in: query
                name: size
                type: integer
                default: 10
                description: the number of items per page
        responses:
            200:
                description: A list of movies
                schema:
                    type: object
                    properties:
                        success:
                            type: boolean
                        movies:
                            type: array
                            items:
                                $ref: '#/definitions/Movies'
                        total:
                            type: number
                        page:
                            type: number
        """
        obj_list = Movies.query.all()
        str_list = [str(obj) for obj in obj_list]
        return jsonify({"success": True, "data": str_list})

    @app.route("/actors")
    @requires_auth("read:actors")
    def get_actors(payload):
        """Get a paginated list of actors
        ---
        tags:
            - Actors

        definitions:
            Actors:
                type: object
                properties:
                    name:
                        type: string
                    age:
                        type: integer
                    gender:
                        type: string
        parameters:
            -   in: query
                name: page
                type: integer
                default: 1
                description: the page number of the paginated result
            -   in: query
                name: size
                type: integer
                default: 10
                description: the number of items per page
        responses:
            200:
                description: A list of actors
                schema:
                    type: object
                    properties:
                        success:
                            type: boolean
                        actors:
                            type: array
                            items:
                                $ref: '#/definitions/Actors'
                        total:
                            type: number
                        page:
                            type: number
        """
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

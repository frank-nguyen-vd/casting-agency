from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
from flask_cors import CORS
from flasgger import Swagger


from database import setup_db
from database.movies import Movies
from database.actors import Actors
from auth import requires_auth, AuthError


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
        obj_list = Actors.query.all()
        str_list = [str(obj) for obj in obj_list]
        return jsonify({"success": True, "actors": str_list, "page": 1, "total": 10})

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return (
            jsonify({"success": False, "error": error.description}),
            error.status_code,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

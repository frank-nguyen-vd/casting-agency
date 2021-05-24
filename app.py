from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
from flask_cors import CORS
from flasgger import Swagger


from database import setup_db
from database.movies import Movies
from database.actors import Actors
from auth import requires_auth


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
                    release_data:
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
                        totalItems:
                            type: number
                        currentPage:
                            type: number
        """
        obj_list = Movies.query.all()
        str_list = [str(obj) for obj in obj_list]
        return jsonify({"success": True, "data": str_list})

    @app.route("/actors")
    def get_actors():
        obj_list = Actors.query.all()
        str_list = [str(obj) for obj in obj_list]
        return jsonify({"success": True, "data": str_list})

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

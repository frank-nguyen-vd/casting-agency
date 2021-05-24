import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from icecream import ic
import argparse

from app import create_app
from database.movies import Movies
from database.actors import Actors

token = "Bearer "
role = ""
roleList = ["casting_assistant", "casting_director", "executive_producer"]
testdb_path = "postgres://postgres:postgres@localhost:5432/testdb"


def mock_testdb():
    sample_movies = [
        {"title": "Dragon Age", "release_date": "01/01/2008"},
        {"title": "Jurassic Park", "release_date": "01/01/2002"},
        {"title": "Toys Story", "release_date": "01/01/2006"},
        {"title": "Golden Flower", "release_date": "01/01/2015"},
        {"title": "Sherlock Holme", "release_date": "01/01/2020"},
        {"title": "Transformer", "release_date": "01/01/2018"},
        {"title": "Inquisition", "release_date": "01/01/2007"},
        {"title": "Inception", "release_date": "01/01/2015"},
        {"title": "Matrix", "release_date": "01/01/2001"},
        {"title": "Doraemon", "release_date": "01/01/1990"},
        {"title": "How I met your mother", "release_date": "01/01/2012"},
        {"title": "Big Bang Theory", "release_date": "01/01/2011"},
    ]

    sample_actors = [
        {"name": "Tom Hanks", "age": 35, "gender": "male"},
        {"name": "Robert De Niro", "age": 55, "gender": "male"},
        {"name": "Katharine Hepburn", "age": 45, "gender": "female"},
        {"name": "Humphrey Bogart", "age": 58, "gender": "female"},
        {"name": "Meryl Streep", "age": 43, "gender": "male"},
        {"name": "Kate Spade", "age": 39, "gender": "female"},
        {"name": "Daniel Day-Lewis", "age": 76, "gender": "female"},
        {"name": "Clark Gable", "age": 28, "gender": "female"},
        {"name": "Sidney Poitier", "age": 19, "gender": "male"},
        {"name": "Ingrid Bergman", "age": 69, "gender": "female"},
        {"name": "Elizabeth Taylor", "age": 90, "gender": "male"},
    ]

    for movies in sample_movies:
        Movies(movies["title"], movies["release_date"]).insert()

    for actor in sample_actors:
        Actors(actor["name"], actor["age"], actor["gender"]).insert()


class MoviesTestCase(unittest.TestCase):
    def setUp(self):
        database_path = "postgres://postgres:postgres@localhost:5432/testdb"
        self.app = create_app(database_path)
        self.client = self.app.test_client()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }

    def tearDown(self):
        pass

    def test_get_paginated_movies(self):
        res = self.client.get("/movies", headers=self.headers)
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    for arg in sys.argv:
        parts = arg.split("=")

        if len(parts) == 2:
            if parts[0] == "--token":
                token += parts[1]

            elif parts[0] == "--role" and parts[1] in roleList:
                role = parts[1]

    for i in range(1, len(sys.argv)):
        del sys.argv[1]

    unittest.main()

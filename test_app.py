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

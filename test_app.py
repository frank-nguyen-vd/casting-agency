import os
import unittest
import json
from dotenv import load_dotenv
from icecream import ic


from app import create_app
from database import db
from database.movies import Movies
from database.actors import Actors

load_dotenv()

role = ""
roleList = ["casting_assistant", "casting_director", "executive_producer"]
if "TEST_ROLE" in os.environ:
    role = os.environ["TEST_ROLE"]

token = "Bearer "
if "TEST_TOKEN" in os.environ:
    token += os.environ["TEST_TOKEN"]

testdb_path = "postgres://postgres:postgres@localhost:5432/testdb"
if "TEST_DB" in os.environ:
    testdb_path = os.environ["TEST_DB"]


def mock_testdb():
    db.create_all()
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
        self.app = create_app(testdb_path)
        self.client = self.app.test_client()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        mock_testdb()

    def tearDown(self):
        db.drop_all()

    def test_get_paginated_movies(self):
        res = self.client.get("/movies", headers=self.headers)
        if role in roleList:
            assert res.status_code == 200


class ActorsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testdb_path)
        self.client = self.app.test_client()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        mock_testdb()

    def tearDown(self):
        db.drop_all()

    def test_200_get_paginated_actors(self):
        page = 1
        size = 10
        res = self.client.get(
            "/actors?page={}&size={}".format(page, size), headers=self.headers
        )

        if role in roleList:
            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True

            assert type(data["actors"][0]["name"]) is str
            assert type(data["actors"][0]["age"]) is int
            assert type(data["actors"][0]["gender"]) is str

            assert data["total"] > 0
            assert data["page"] == page

    def test_401_unauthorized_get_actors(self):
        page = 1
        size = 10
        res = self.client.get(
            "/actors?page={}&size={}".format(page, size), headers=self.headers
        )

        if role not in roleList:
            assert res.status_code == 401

    def test_404_request_beyond_valid_page(self):
        page = 100000
        size = 100000
        res = self.client.get(
            "/actors?page={}&size={}".format(page, size), headers=self.headers
        )

        if role in roleList:
            assert res.status_code == 404


if __name__ == "__main__":
    unittest.main()
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

public = ""
casting_assistant = "casting_assistant"
casting_director = "casting_director"
executive_producer = "executive_producer"

role = public


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

    def test_200_create_new_resource(self):
        if role in [executive_producer]:
            movies = {
                "title": "Alan The Best",
                "release_date": "12 Dec 2022 00:00:00 GMT",
            }
            res = self.client.post(
                "/movies",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("movies") is not None
            assert data["movies"].get("title") == movies["title"]
            assert movies["release_date"] in data["movies"].get("release_date")

    def test_400_create_with_empty_data(self):
        if role in [executive_producer]:
            movies = {}
            res = self.client.post(
                "/movies",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data["success"] == False

    def test_400_create_with_missing_field(self):
        if role in [executive_producer]:
            movies = {"title": "Alan The Best"}
            res = self.client.post(
                "/movies",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data["success"] == False

    def test_400_create_with_invalid_format(self):
        if role in [executive_producer]:
            movies = {"title": 0, "release_date": True}
            res = self.client.post(
                "/movies",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data["success"] == False

    def test_200_get_paginated_resource(self):
        if role in [casting_assistant, casting_director, executive_producer]:
            page = 1
            size = 10
            res = self.client.get(
                "/movies?page={}&size={}".format(page, size), headers=self.headers
            )

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data.get("success") == True
            assert data.get("movies") is not None
            assert type(data["movies"]) is list
            assert type(data["movies"][0]["title"]) is str
            assert type(data["movies"][0]["release_date"]) is str

            assert data["total"] > 0
            assert data["page"] == page

    def test_200_get_resource_by_id(self):
        if role in [casting_assistant, casting_director, executive_producer]:
            id = 1
            res = self.client.get(f"/movies/{id}", headers=self.headers)

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data.get("success") == True
            assert data.get("movie") is not None
            assert type(data["movie"].get("title")) is str
            assert type(data["movie"].get("release_date")) is str

    def test_404_get_not_existing_resource(self):
        if role in [casting_assistant, casting_director, executive_producer]:
            id = 1
            res = self.client.get(f"/movies/{id}", headers=self.headers)

            data = json.loads(res.data)
            assert res.status_code == 404
            assert data.get("success") == False

    def test_404_request_beyond_valid_page(self):
        if role in [casting_assistant, casting_director, executive_producer]:
            page = 100000
            size = 100000
            res = self.client.get(
                "/movies?page={}&size={}".format(page, size), headers=self.headers
            )

            assert res.status_code == 404

    def test_200_update_resource(self):
        if role in [casting_director, executive_producer]:
            movies = {"title": "Worried Tom"}
            res = self.client.patch(
                "/movies/1",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("movies") is not None
            assert data["movies"].get("title") == movies["title"]

    def test_400_update_with_empty_data(self):
        if role in [casting_director, executive_producer]:
            movies = {}
            res = self.client.patch(
                "/movies/1",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data["success"] == False

    def test_400_update_with_invalid_format(self):
        if role in [casting_director, executive_producer]:
            movies = {"title": 0}
            res = self.client.patch(
                "/movies/1",
                headers=self.headers,
                data=json.dumps(movies),
            )

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data["success"] == False

    def test_200_delete_resource(self):
        if role in [executive_producer]:
            id = 1
            res = self.client.delete(f"/movies/{id}", headers=self.headers)

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("deleted") == id

    def test_404_delete_not_existing_resource(self):
        if role in [executive_producer]:
            id = 10000000
            res = self.client.delete(f"/movies/{id}", headers=self.headers)

            data = json.loads(res.data)
            assert res.status_code == 404
            assert data["success"] == False


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

    def test_200_get_paginated_resource(self):
        if role in [casting_assistant, casting_director, executive_producer]:
            page = 1
            size = 10
            res = self.client.get(
                "/actors?page={}&size={}".format(page, size), headers=self.headers
            )

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("actors") is not None
            assert type(data["actors"][0]["name"]) is str
            assert type(data["actors"][0]["age"]) is int
            assert type(data["actors"][0]["gender"]) is str

            assert data["total"] > 0
            assert data["page"] == page

    def test_401_unauthorized_get_resource(self):
        if role not in [casting_assistant, casting_director, executive_producer]:
            page = 1
            size = 10
            res = self.client.get(
                "/actors?page={}&size={}".format(page, size), headers=self.headers
            )

            assert res.status_code == 401

    def test_404_request_beyond_valid_page(self):
        page = 100000
        size = 100000
        res = self.client.get(
            "/actors?page={}&size={}".format(page, size), headers=self.headers
        )

        if role in [casting_assistant, casting_director, executive_producer]:
            assert res.status_code == 404

    def test_200_create_new_resource(self):
        if role in [casting_director, executive_producer]:
            actor = {"name": "Scary Hamlet", "age": 21, "gender": "male"}
            res = self.client.post(
                "/actors",
                headers=self.headers,
                data=json.dumps(actor),
            )

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("actor") is not None
            assert data["actor"].get("name") == actor["name"]
            assert data["actor"].get("age") == actor["age"]
            assert data["actor"].get("gender") == actor["gender"]

    def test_400_create_with_empty_data(self):
        if role in [casting_director, executive_producer]:
            actor = {}
            res = self.client.post(
                "/actors",
                headers=self.headers,
                data=json.dumps(actor),
            )
            data = json.loads(res.data)
            assert res.status_code == 400
            assert data.get("success") == False
            assert data.get("actor") is None

    def test_400_create_with_invalid_format(self):
        if role in [casting_director, executive_producer]:
            actor = {"name": 12, "age": "hello", "gender": "male"}
            res = self.client.post(
                "/actors",
                headers=self.headers,
                data=json.dumps(actor),
            )
            data = json.loads(res.data)
            assert res.status_code == 400
            assert data.get("success") == False
            assert data.get("actor") is None

    def test_400_create_with_missing_field(self):
        if role in [casting_director, executive_producer]:
            actor = {"name": "John", "age": 31}
            res = self.client.post(
                "/actors",
                headers=self.headers,
                data=json.dumps(actor),
            )
            data = json.loads(res.data)
            assert res.status_code == 400
            assert data.get("success") == False
            assert data.get("actor") is None

    def test_200_update_resource(self):
        if role in [casting_director, executive_producer]:
            actor = {"name": "Scary Hamlet", "age": 21, "gender": "male"}
            res = self.client.patch(
                "/actors/1",
                headers=self.headers,
                data=json.dumps(actor),
            )

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("actor") is not None
            assert data["actor"].get("name") == actor["name"]
            assert data["actor"].get("age") == actor["age"]
            assert data["actor"].get("gender") == actor["gender"]

    def test_400_update_with_empty_data(self):
        if role in [casting_director, executive_producer]:
            actor = {}
            res = self.client.patch(
                "/actors/1",
                headers=self.headers,
                data=json.dumps(actor),
            )
            data = json.loads(res.data)
            assert res.status_code == 400
            assert data.get("success") == False
            assert data.get("actor") is None

    def test_400_update_with_invalid_format(self):
        if role in [casting_director, executive_producer]:
            actor = {"name": 12, "age": "hello", "gender": "male"}
            res = self.client.patch(
                "/actors/1",
                headers=self.headers,
                data=json.dumps(actor),
            )
            data = json.loads(res.data)
            assert res.status_code == 400
            assert data.get("success") == False
            assert data.get("actor") is None

    def test_200_delete_resource(self):
        if role in [casting_director, executive_producer]:
            id = 1
            res = self.client.delete(f"/actors/{id}", headers=self.headers)

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data["success"] == True
            assert data.get("deleted") == id

    def test_404_delete_not_existing_resource(self):
        if role in [casting_director, executive_producer]:
            id = 10000000
            res = self.client.delete(f"/actors/{id}", headers=self.headers)

            data = json.loads(res.data)
            assert res.status_code == 404
            assert data["success"] == False


if __name__ == "__main__":
    unittest.main()

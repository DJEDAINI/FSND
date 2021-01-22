
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random

from .app import create_app
from .models import setup_db, Actor, Movie


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(os.getenv("TEST_DB_USERNAME"), os.getenv("TEST_DB_PASSWD"), os.getenv("TEST_DB_HOST"), os.getenv("TEST_DB_PORT"), os.getenv("TEST_DB_NAME"))
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        """Test list movies endpoint """
        res = self.client().get('/api/v1/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_405_get_movies(self):
        """Test list movies Error handling endpoint """
        res = self.client().put('/api/v1/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_create_movie(self):
        """Test create movie endpoint """
        res = self.client().get('/api/v1/movies')
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_create_movie(self):
        """Test create movie Error handling endpoint """

        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_patch_movie(self):
        """Test patch movie endpoint """
        res = self.client().get('/api/v1/movies')
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().put("/api/v1/movies/{}".format( random.choice(movies['movies'])['id']), json={'title': 'Movie title updated - unittest', 'release_date': '10/12/2020' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_patch_movie(self):
        """Test patch movie Error handling endpoint """

        res = self.client().put("/api/v1/movies", json={'title': 'Movie title updated - unittest' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_delete_movie(self):
        """Test delete movie endpoint """
        movie = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' } )
        res = self.client().get('/api/v1/movies')
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete("/api/v1/movies/{}".format( random.choice(movies['movies'])['id']))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_404_delete_movie(self):
        """Test delete movie Error handling endpoint """
        res = self.client().delete("/api/v1/movies/200")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)

    def test_get_actors(self):
        """Test list actors endpoint """
        res = self.client().get('/api/v1/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_405_get_actors(self):
        """Test list actors Error handling endpoint """
        res = self.client().put('/api/v1/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_create_actor(self):
        """Test create actor endpoint """
        res = self.client().get('/api/v1/actors')
        actors = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest', 'age': 40, gender: 'male' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_create_actor(self):
        """Test create actor Error handling endpoint """

        res = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_patch_actor(self):
        """Test patch actor endpoint """
        res = self.client().get('/api/v1/actors')
        actors = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().put("/api/v1/actors/{}".format( random.choice(actors['actors'])['id']), json={'name': 'Actor name updated - unittest', 'age': 30, gender: 'female' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_patch_actor(self):
        """Test patch actor Error handling endpoint """

        res = self.client().put("/api/v1/actors", json={'title': 'Actor name updated - unittest' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_delete_actor(self):
        """Test delete actor endpoint """
        actor = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest', 'age': 40, gender: 'male' } )
        res = self.client().get('/api/v1/actors')
        actors = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete("/api/v1/actors/{}".format( random.choice(actors['actors'])['id']))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_404_delete_actor(self):
        """Test delete actor Error handling endpoint """
        res = self.client().delete("/api/v1/actors/200")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
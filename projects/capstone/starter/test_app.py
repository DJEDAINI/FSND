
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
        # get your Auth Bearer token from somewhere
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFVXdNMEZHTlVWQ09FSkNPVEkwTURsQlJqVkdPVFpDTmtZd1F6YzVNVFkyTmtFNVJUaERSQSJ9.eyJpc3MiOiJodHRwczovL2EtZGplZGFpbmkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjYyZTQ4OWU5YWFkMDA3NjFkOTcwZCIsImF1ZCI6ImZzbmQiLCJpYXQiOjE2MTEzODg3NTcsImV4cCI6MTYxMTQ3NTE1NywiYXpwIjoiMVhpQlhCRUVDZmlRZjZqSnBOME9FNjB3dkxkcndGc08iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.OAMe-TPFxxGn-4gQcydqNC6jnUYJalZa_36fW2g8cEBq658WQG7QUKApPP3j_wpxqOWWnf9y4mUKj5nutux8HeK5Mx9HedO4CKY-dWsWQhGs8KogyC341elzuuflAskBSMkrjI1uWG-UZQtwLs9bqTRqvr0rbKz9E1i3iPLE-I2F7z7nGoSWWxx9xnO89IojeJtqoLDSkvtnPEWaOWMTCTGSwu6j8pOAaUqBwylT2TRCFkUjmjyPlSS6UgUsQ07wNJwd6poSl7z2um6MltzZXFfix7KDTOXxazS7OL8He1DAtHJXgpDN4OjGE5KL5hGdu6wL1khnwvg4_iQdFeKwCA'}
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
        res = self.client().get('/api/v1/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_405_get_movies(self):
        """Test list movies Error handling endpoint """
        res = self.client().put('/api/v1/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_create_movie(self):
        """Test create movie endpoint """
        res = self.client().get('/api/v1/movies', headers=self.headers)
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_create_movie(self):
        """Test create movie Error handling endpoint """

        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_patch_movie(self):
        """Test patch movie endpoint """
        res = self.client().get('/api/v1/movies', headers=self.headers)
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().put("/api/v1/movies/{}".format( random.choice(movies['movies'])['id']), json={'title': 'Movie title updated - unittest', 'release_date': '10/12/2020' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_patch_movie(self):
        """Test patch movie Error handling endpoint """

        res = self.client().put("/api/v1/movies", json={'title': 'Movie title updated - unittest' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_delete_movie(self):
        """Test delete movie endpoint """
        movie = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' }, headers=self.headers )
        res = self.client().get('/api/v1/movies', headers=self.headers)
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete("/api/v1/movies/{}".format( random.choice(movies['movies'])['id']), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_404_delete_movie(self):
        """Test delete movie Error handling endpoint """
        res = self.client().delete("/api/v1/movies/200", headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)

    def test_get_actors(self):
        """Test list actors endpoint """
        res = self.client().get('/api/v1/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_405_get_actors(self):
        """Test list actors Error handling endpoint """
        res = self.client().put('/api/v1/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_create_actor(self):
        """Test create actor endpoint """
        res = self.client().get('/api/v1/actors', headers=self.headers)
        actors = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest', 'age': 40, 'gender': 'male' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_create_actor(self):
        """Test create actor Error handling endpoint """

        res = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_patch_actor(self):
        """Test patch actor endpoint """
        res = self.client().get('/api/v1/actors', headers=self.headers)
        actors = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().put("/api/v1/actors/{}".format( random.choice(actors['actors'])['id']), json={'name': 'Actor name updated - unittest', 'age': 30, 'gender': 'female' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_422_patch_actor(self):
        """Test patch actor Error handling endpoint """

        res = self.client().put("/api/v1/actors", json={'title': 'Actor name updated - unittest' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)

    def test_delete_actor(self):
        """Test delete actor endpoint """
        actor = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest', 'age': 40, 'gender': 'male' }, headers=self.headers )
        res = self.client().get('/api/v1/actors', headers=self.headers)
        actors = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete("/api/v1/actors/{}".format( random.choice(actors['actors'])['id']), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_404_delete_actor(self):
        """Test delete actor Error handling endpoint """
        res = self.client().delete("/api/v1/actors/200", headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)


    # Test RBAC roles
    def test_view_movies_for_casting_assitant(self):
        """Test list movies endpoint as casting assitant """
        res = self.client().get('/api/v1/movies', headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFVXdNMEZHTlVWQ09FSkNPVEkwTURsQlJqVkdPVFpDTmtZd1F6YzVNVFkyTmtFNVJUaERSQSJ9.eyJpc3MiOiJodHRwczovL2EtZGplZGFpbmkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjYyZTcxOWU5YWFkMDA3NjFkOTcyZSIsImF1ZCI6ImZzbmQiLCJpYXQiOjE2MTEzODYyNTUsImV4cCI6MTYxMTQ3MjY1NSwiYXpwIjoiMVhpQlhCRUVDZmlRZjZqSnBOME9FNjB3dkxkcndGc08iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.EYQ1XyGZL9NvqE8ZYGudh-GFESn1W5Cv1u1WF0PYtKXmV6HCAhZRurMmvybCAZSEAp6OjBxILF2BsISHdSNHYVaM4DdeOAtaImmcLPzwoCXG1ugY7fHjICs2m6TodhhhXRzZcP4bEeCyqJDylgHPS5xKlUOcDU44wBXkk7ox25dk9V7cOiW0RHqr-lNSotgbG_e8lhAVWQzCbXQZDkkotcKpv9A03kMVgtxoAyUIWNBGbznVXZVoRJmYn6139NVIbFGBtP_WgUMMLiu1zvTe41JvQB4GyjLT3FeyMWTkI9420SRWTEEOi3gApW7b3PG6IUOoOPSplu2V1K34LS1z9A'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_create_movie_for_casting_assitant(self):
        """Test create movie endpoint as casting assitant """
        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' }, headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFVXdNMEZHTlVWQ09FSkNPVEkwTURsQlJqVkdPVFpDTmtZd1F6YzVNVFkyTmtFNVJUaERSQSJ9.eyJpc3MiOiJodHRwczovL2EtZGplZGFpbmkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjYyZTcxOWU5YWFkMDA3NjFkOTcyZSIsImF1ZCI6ImZzbmQiLCJpYXQiOjE2MTEzODYyNTUsImV4cCI6MTYxMTQ3MjY1NSwiYXpwIjoiMVhpQlhCRUVDZmlRZjZqSnBOME9FNjB3dkxkcndGc08iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.EYQ1XyGZL9NvqE8ZYGudh-GFESn1W5Cv1u1WF0PYtKXmV6HCAhZRurMmvybCAZSEAp6OjBxILF2BsISHdSNHYVaM4DdeOAtaImmcLPzwoCXG1ugY7fHjICs2m6TodhhhXRzZcP4bEeCyqJDylgHPS5xKlUOcDU44wBXkk7ox25dk9V7cOiW0RHqr-lNSotgbG_e8lhAVWQzCbXQZDkkotcKpv9A03kMVgtxoAyUIWNBGbznVXZVoRJmYn6139NVIbFGBtP_WgUMMLiu1zvTe41JvQB4GyjLT3FeyMWTkI9420SRWTEEOi3gApW7b3PG6IUOoOPSplu2V1K34LS1z9A'} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_create_actor_for_casting_director(self):
        """Test create actor endpoint as casting director """
        res = self.client().post("/api/v1/actors", json={'name': 'Actor name - unittest', 'age': 40, 'gender': 'male' }, headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFVXdNMEZHTlVWQ09FSkNPVEkwTURsQlJqVkdPVFpDTmtZd1F6YzVNVFkyTmtFNVJUaERSQSJ9.eyJpc3MiOiJodHRwczovL2EtZGplZGFpbmkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjYxYTc4OWU5YWFkMDA3NjFkOGQ1ZiIsImF1ZCI6ImZzbmQiLCJpYXQiOjE2MTEzODg5OTEsImV4cCI6MTYxMTQ3NTM5MSwiYXpwIjoiMVhpQlhCRUVDZmlRZjZqSnBOME9FNjB3dkxkcndGc08iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.kDntaoEAfoJbVheC8RJOc_ydUwD8LpbzAYFB1dNzR0aF4Qlm6Xpr8lJsz3DVPuIKQyUIAlwsLd52fdo4tqhYENOdon_t5K-fF9ggJcWKTVc6TB46_C5VAPOgf1P1S9R6BXaQuptLQFKV9du5jEWP2yxjJlxuOXO9lIzztBNbTWC_ctrKGl-PfkggF3vYjiROjWjfI7kybEMSplZoN_0BOaixMoBDKrSJsZ6T2vHbRwJFJixdBB2iho2WHSc0dlADYrAOJuOgcY52JDks-B6j002mYtUfhCCU-Cxdd8sRBZFAVG-9E6a9PajDQ6jvfRc6UiKN86ufOULCufmlfluqGQ'} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_create_movie_for_casting_director(self):
        """Test create movie endpoint as casting director """
        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' }, headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFVXdNMEZHTlVWQ09FSkNPVEkwTURsQlJqVkdPVFpDTmtZd1F6YzVNVFkyTmtFNVJUaERSQSJ9.eyJpc3MiOiJodHRwczovL2EtZGplZGFpbmkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjYxYTc4OWU5YWFkMDA3NjFkOGQ1ZiIsImF1ZCI6ImZzbmQiLCJpYXQiOjE2MTEzODg5OTEsImV4cCI6MTYxMTQ3NTM5MSwiYXpwIjoiMVhpQlhCRUVDZmlRZjZqSnBOME9FNjB3dkxkcndGc08iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.kDntaoEAfoJbVheC8RJOc_ydUwD8LpbzAYFB1dNzR0aF4Qlm6Xpr8lJsz3DVPuIKQyUIAlwsLd52fdo4tqhYENOdon_t5K-fF9ggJcWKTVc6TB46_C5VAPOgf1P1S9R6BXaQuptLQFKV9du5jEWP2yxjJlxuOXO9lIzztBNbTWC_ctrKGl-PfkggF3vYjiROjWjfI7kybEMSplZoN_0BOaixMoBDKrSJsZ6T2vHbRwJFJixdBB2iho2WHSc0dlADYrAOJuOgcY52JDks-B6j002mYtUfhCCU-Cxdd8sRBZFAVG-9E6a9PajDQ6jvfRc6UiKN86ufOULCufmlfluqGQ'} )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_create_movie_for_executive_producer(self):
        """Test create actor endpoint as executive producer """
        res = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest', 'release_date': '12/12/2020' }, headers=self.headers )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_for_executive_producer(self):
        """Test delete actor endpoint as executive producer """
        movie = self.client().post("/api/v1/movies", json={'title': 'Movie title - unittest executive producer', 'release_date': '12/12/2020' }, headers=self.headers )
        res = self.client().get('/api/v1/movies', headers=self.headers)
        movies = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete("/api/v1/movies/{}".format( random.choice(movies['movies'])['id']), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
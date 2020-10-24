import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

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

    def test_get_questions(self):
        """Test list questions endpoint """
        res = self.client().get('/api/v1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_get_categories(self):
        """Test list categories endpoint """
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_create_question(self):
        """Test create question endpoint """
        res = self.client().get('/api/v1/questions')
        questions = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().post("/api/v1/questions", json={'question': 'Unittest question', 'answer': 'Unittest answer', 'category': 1, 'difficulty': 1 } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')

        res = self.client().get('/api/v1/questions')
        after_insertion_questions = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(after_insertion_questions['total_questions'], questions['total_questions'] + 1)

    def test_422_create_question(self):
        """Test create question Error handling endpoint """

        res = self.client().post("/api/v1/questions", json={'question': 'Unittest question', 'answer': 'Unittest answer' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], 'failed')

    def test_delete_question(self):
        """Test delete question endpoint """
        res = self.client().get('/api/v1/questions')
        questions = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete("/api/v1/questions/{}".format( random.choice(questions['questions'])['id']))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')

        res = self.client().get('/api/v1/questions')
        after_delete_questions = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(after_delete_questions['total_questions'], questions['total_questions'] - 1)

    def test_404_delete_question(self):
        """Test delete question Error handling endpoint """
        res = self.client().delete("/api/v1/questions/200")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 'failed')

    def test_search_questions(self):
        """Test search questions endpoint """

        res = self.client().post("/api/v1/questions/search", json={'searchTerm': 'unit' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['total_questions'], 3)

        res = self.client().post("/api/v1/questions/search", json={'searchTerm': 'notfound' } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['total_questions'], 0)

    def test_get_questions_by_category(self):
        """Test list questions related to specific category endpoint """
        res = self.client().get('/api/v1/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['total_questions'], 0)

        res = self.client().get('/api/v1/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['total_questions'], 3)

    def test__404_get_questions_by_category(self):
        """Test list questions related to specific category Erro handling endpoint """
        res = self.client().get('/api/v1/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 'failed')


    def test_play_quiz(self):
        """Test list categories endpoint """
        res = self.client().post('/api/v1/quizzes', json={ 'previous_questions': [1,2], 'quiz_category': {'id': 1, 'type': 'science'} })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['question'])

        # Play quiz when all categories selected
        res = self.client().post('/api/v1/quizzes', json={ 'previous_questions': [1,2], 'quiz_category': {'id': 0} })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['question'])

    def test_400_play_quiz(self):
        """Test list categories Bad request endpoint """
        res = self.client().post('/api/v1/quizzes', json={ 'previous_questions': 'not array', 'quiz_category': 'not a dict' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 'failed')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
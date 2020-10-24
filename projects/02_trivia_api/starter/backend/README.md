# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Initialise environment variables
From the backend folder in terminal run:
```bash
cp .sample .env
```
Then change the env varibles with your database configuration to make sure that connection to your database with be succeeded

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Or you can initialise these FLASK env variables directly within the dot-file: .falskenv

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
BASE_URL = http://127.0.0.1:5000/api/v1

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/:id/questions'
POST '/questions/'
POST '/questions/search'
DELETE 'questions/:id'
POST '/quizzes'

GET '/categories'
- Fetches a list of categories objects, has the id attribute and the name of the category
- Request Arguments: None
- Returns: An object with a two keys, id and type of a category, that contains a object of id: category id and type: cateogry name . 
- Sample request: curl http://127.0.0.1:5000/api/v1/categories
{
    "status": "success",
    "categories": {
        {
            id: 1,
            type: "Science",
        },
        {
            id: 2,
            type: "Art",
        },
        {
            id: 3,
            type: "Geography",
        },
        {
            id: 4,
            type: "History",
        },
        {
            id: 5,
            type: "Entertainment",
        },
        {
            id: 5,
            type: "Sports",
        }
    }
}

GET '/questions'
- Fetches a list of paginated questions objects, also identifying the total of questions and the categories list
- Request Arguments: Optional query parameter: page: to identifiy the specified page of questioned to be returned
- Returns: An list of questions object, categories list object, and the total_questions attribute. 
- Sample request: curl http://127.0.0.1:5000/api/v1/questions
{
    "status": "success",
    "questions": {
        {
            "answer": "A1",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "Q1"
        }
        {
            "answer": "A2",
            "category": 2,
            "difficulty": 1,
            "id": 2,
            "question": "Q2"
        },
    },
    "total_questions": 2,
    "categories": {
        {
            id: 1,
            type: "Science",
        },
        {
            id: 2,
            type: "Art",
        },
        {
            id: 3,
            type: "Geography",
        },
        {
            id: 4,
            type: "History",
        },
        {
            id: 5,
            type: "Entertainment",
        },
        {
            id: 5,
            type: "Sports",
        }
    }
}

GET '/categories/:id/questions'
- Fetches a list of questions related to specific category
- Request Arguments: id: identify the cateogry id, and optional parameter page: to paginate to questions list
- Returns: An list of questions object, current_category identified by the category id specified in request parameter, and the total_questions attribute. 
- Sample request: curl http://127.0.0.1:5000/api/v1/categories/1/questions
{
    "status": "success",
    "current_category": {
        {
            id: 1,
            type: "Science",
        }
    },
    "questions": {
        {
            "answer": "A1",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "Q1"
        }
    },
    "total_questions": 1,
}

POST '/questions'
- Create a new question
- Body Arguments: question: question string, answer: the answer string of the question, category: category id related to the question to be inserted, difficulty: integer to specify the difficulty degree of the question from 1 to 5.
- Returns: message attribute to inform the user that to question has been inserted with success, message: question created with success. 
- Sample request: curl -X POST -H "Content-Type: application/json" -d '{ "question": "Q1", "answer": "A1", "category": 1, "difficulty": 1}' http://127.0.0.1:5000/api/v1/questions
{
    "status": "success",
    "message": "question created with success"
}

POST '/questions/search'
- Search for questions by any phrase. The questions list will include only question that include that string within their question
- Body Arguments: searchTerm: to specifiy the search phrase to search with in the questions list.
- Returns: a list of questions that contain that string within the question. 
- Sample request: curl -X POST -H "Content-Type: application/json" -d '{ "searchTerm": "title"} ' http://127.0.0.1:5000/api/v1/questions/search
{
    "status": "success",
    "questions": {
        {
            "answer": "answer title",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "title of the question"
        }
    },
    "total_questions": 1,
}

DELETE '/questions/:id'
- Delete a question with a specific id attribute
- Request Arguments: id: the id of the question to be removed.
- Returns: message attribute to inform the user that to question has been deleted with success, message: question created with success. 
- Sample request: curl -X DELETE http://127.0.0.1:5000/api/v1/questions/1
{
  "status": "success",
  "message": "question deleted with success"
}

POST '/quizzes'
- Play the quiz, return a random question related to specific category, and ensure that the id of the returned question is not appeared in the previous questions list.
- Body Arguments: previous_questions: array of ids of previous returned questions, quiz_category: category object of questions that you want to play the quiz with Or you can set the id equal to 0 if you want to select all the categories.
- Returns: the next question of the quiz within the specified category. 
- Sample request: curl -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [1,2], "quiz_category": { "id": 1, "type": "science"}}' http://127.0.0.1:5000/api/v1/quizzes
- Another Sample request: curl -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [1,2], "quiz_category": { "id": 0}}' http://127.0.0.1:5000/api/v1/quizzes
{
  "status": "success",
  "question": {
    "answer": "Answer-3",
    "category": 1,
    "difficulty": 2,
    "id": 3,
    "question": "Question-3"
  }
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
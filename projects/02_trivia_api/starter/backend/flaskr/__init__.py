import os
from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

  '''
  Get all available categories.
  '''
  @app.route("/api/v1/categories")
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return jsonify({
      'status': 'success',
      'categories': formatted_categories
    })


  '''
  Paginate questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/api/v1/questions")
  def get_questions():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page, QUESTIONS_PER_PAGE, False)
    formatted_questions = [question.format() for question in questions.items]
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return jsonify({
      'status': 'success',
      'total_questions': questions.total,
      'questions': formatted_questions,
      'categories': formatted_categories
    })
  
  '''
  DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/api/v1/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'status': 'success',
        'message': 'question deleted with success',
      })
    except:
      abort(422)

  '''
  POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/api/v1/questions", methods=['POST'])
  def create_question():
    data = request.get_json(force=True)

    question = data.get('question', None)
    answer = data.get('answer', None)
    category = data.get('category', None)
    difficulty = data.get('difficulty', None)

    try:
      question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      question.insert()

      return jsonify({
        'status': 'success',
        'message': 'question created with success',
      })
    except:
      abort(422)

  '''
  POST request to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/api/v1/questions/search", methods=['POST'])
  def search_questions():
    page = request.args.get('page', 1, type=int)
    data = request.get_json(force=True)
    search_for = data.get('searchTerm', None)
    questions = Question.query.filter(Question.question.ilike('%' + search_for + '%')).paginate(page, QUESTIONS_PER_PAGE, False)
    formatted_questions = [question.format() for question in questions.items]
    return jsonify({
      'status': 'success',
      'total_questions': questions.total,
      'questions': formatted_questions,
    })

  '''
  GET questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/api/v1/categories/<int:category_id>/questions")
  def questions_by_category(category_id):
    page = request.args.get('page', 1, type=int)
    try:
      category = Category.query.get(category_id)
      if category is None:
        abort(404)

      questions = Question.query.filter(Question.category==category_id).paginate(page, QUESTIONS_PER_PAGE, False)
      formatted_questions = [question.format() for question in questions.items]

      return jsonify({
        'status': 'success',
        'total_questions': questions.total,
        'questions': formatted_questions,
        'current_category': category.format()
      })
    except:
      abort(404)


  '''
  POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route("/api/v1/quizzes", methods=['POST'])
  def play_quiz():
    page = request.args.get('page', 1, type=int)
    data = request.get_json(force=True)
    previous_questions = data.get('previous_questions', None)
    category = data.get('quiz_category', None)
    if category['id'] != 0:
      questions = Question.query.filter(Question.category==category['id']).paginate(page, QUESTIONS_PER_PAGE, False)
    else:
      questions = Question.query.paginate(page, QUESTIONS_PER_PAGE, False)
    formatted_questions = [question.format() for question in questions.items if question.id not in previous_questions]
    return jsonify({
      'status': 'success',
      'question': random.choice(formatted_questions + [None])
    })

  '''
  Error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  
  return app

    
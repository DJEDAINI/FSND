import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS MUST BE UNCOMMENTED ONLY ON FIRST RUN
'''
# db_drop_and_create_all()

'''
Use the after_request decorator to set Access-Control-Allow
'''
@app.after_request
def after_request(response):
  response.headers['Access-Control-Allow-Origin']      = 'http://localhost:4200'
  response.headers['Access-Control-Allow-Headers']     = 'Content-Type,Authorization'
  response.headers['Access-Control-Allow-Methods']     = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  return response

## ROUTES
'''
GET /drinks
    - public endpoint
    - contain only the drink.short() data representation
    - returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
def get_short_repr_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]
    return jsonify({
      'status': True,
      'drinks': formatted_drinks
    })

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_long_repr_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]
    return jsonify({
      'status': True,
      'drinks': formatted_drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        - it should create a new row in the drinks table
        - it should require the 'post:drinks' permission
        - it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    data = request.get_json(force=True)
    try:
        title = data.get('title', None)
        recipe = data.get('recipe', None)
        if None in [title, recipe] or type(recipe) != list:
            abort(422)
        for item in recipe:
            color = item['color']
            name = item['name']
            parts = item['parts']
            if (None in [color, name, parts]):
                abort(422)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            'status': True,
            'drinks': [drink.long()],
        })
    except:
        abort(422)

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    data = request.get_json(force=True)
    try:
        drink = Drink.query.get(drink_id)
        if drink is None:
            abort(404)

        title = data.get('title', None)
        recipe = data.get('recipe', None)
        if None in [title, recipe] or type(recipe) != list:
            abort(422)

        for item in recipe:
            color = item['color']
            name = item['name']
            parts = item['parts']
            if (None in [color, name, parts]):
                abort(422)

        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            'status': True,
            'drinks': [drink.long()],
        })
    except:
        abort(422)

'''
    DELETE /drinks/<id> where <id> is the existing model id
        - respond with a 404 error if <id> is not found
        - delete the corresponding row for <id>
        - require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    try:
        drink = Drink.query.get(drink_id)
        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
        'status': True,
        'drink': drink_id,
        'message': 'drink deleted with success',
        })
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
Error handling for resource not found
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

'''
Error handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error_handling(error):
    print(error.error['description'])
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

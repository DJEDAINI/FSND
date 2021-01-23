import os
from flask import (
  Flask,
  request,
  jsonify,
  abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import (
    db_drop_and_create_all,
    setup_db,
    Actor,
    Movie
)
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

app = create_app()

DATA_PER_PAGE = 10


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
GET /movies
    - public endpoint
    - contain only the movie.short() data representation
    - returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/movies")
@requires_auth('view:movies')
def get_long_repr_movies():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page, DATA_PER_PAGE, False)
    formatted_movies = [movie.long() for movie in movies]
    return jsonify({
      'status': True,
      'movies': formatted_movies
    })

'''
    POST /movies
        - it should create a new row in the movies table
        - it should require the 'create:movies' permission
        - it should contain the movie.long() data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/movies", methods=['POST'])
@requires_auth('create:movies')
def create_movie():
    data = request.get_json(force=True)
    try:
        title = data.get('title')
        release_date = data.get('release_date')
        if None in [title, release_date]:
            abort(422)
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'status': True,
            'movies': [movie.long()],
        })
    except Exception:
        abort(422)

'''
    PATCH /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:movies' permission
        it should contain the movie.long() data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/movies/<int:movie_id>", methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(movie_id):
    data = request.get_json(force=True)

    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404)

    title = data.get('title', movie.title)
    release_date = data.get('release_date', movie.release_date)

    movie.title = title
    movie.release_date = release_date

    movie.update()
    return jsonify({
        'status': True,
        'movies': [movie.long()],
    })
    # except:
    #     abort(422)

'''
    DELETE /movies/<id> where <id> is the existing model id
        - respond with a 404 error if <id> is not found
        - delete the corresponding row for <id>
        - require the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    try:
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
        'status': True,
        'movie': movie_id,
        'message': 'movie deleted with success',
        })
    except Exception:
        abort(422)

'''
GET /actors
    - public endpoint
    - contain only the actor.short() data representation
    - returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/actors")
@requires_auth('view:actors')
def get_long_repr_actors():
    page = request.args.get('page', 1, type=int)
    actors = Actor.query.paginate(page, DATA_PER_PAGE, False)
    formatted_actors = [actor.long() for actor in actors]
    return jsonify({
      'status': True,
      'actors': formatted_actors
    })

'''
    POST /actors
        - it should create a new row in the actors table
        - it should require the 'create:actors' permission
        - it should contain the actor.long() data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/actors", methods=['POST'])
@requires_auth('create:actors')
def create_actor():
    data = request.get_json(force=True)
    try:
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        if None in [name, age, gender]:
            abort(422)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'status': True,
            'actors': [actor.long()],
        })
    except Exception:
        abort(422)

'''
    PATCH /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actors' permission
        it should contain the actor.long() data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/actors/<int:actor_id>", methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(actor_id):
    data = request.get_json(force=True)

    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404)

    name = data.get('name', actor.name)
    age = data.get('age', actor.age)
    gender = data.get('gender', actor.gender)

    actor.name = name
    actor.age = age
    actor.gender = gender

    actor.update()
    return jsonify({
        'status': True,
        'actors': [actor.long()],
    })
    # except:
    #     abort(422)

'''
    DELETE /actors/<id> where <id> is the existing model id
        - respond with a 404 error if <id> is not found
        - delete the corresponding row for <id>
        - require the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/api/v1/actors/<int:actor_id>", methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(actor_id):
    try:
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
        'status': True,
        'actor': actor_id,
        'message': 'actor deleted with success',
        })
    except Exception:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "status": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
Example error handling for unprocessable entity
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "status": False, 
        "error": 400,
        "message": "bad_request "
    }), 400

'''
Error handling for resource not found
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "status": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

'''
Error handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error_handling(error):
    return jsonify({
        "status": False, 
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

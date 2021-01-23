# Casting Agency Backend API:

## About
The Casting Agency a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.
What motivate me to do this project ?
I developed this project to make use and proof of the knowledge i acquired in the Full stack Nanodegree course and hence gain confidence in these skills.

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the capstone/starter directory, run the following to install all necessary dependencies:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://u-capstone.herokuapp.com

The live application can only be used after generation tokens from Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are three tables created: Movie, Actor, and Movies_Actors
- The Movie table is used to add new movies specifying their title and release dates, and also retrieve these movies.
- Each movie has a list of actors, I use the table Movies_Actors to keep track of these actors who participating in a given movie.
- You can also find a list of movies which a given actor participate on, we can find this information in the pivot table Movies_Actors
- The Actor table is used to add new actors specifying their names and genders, and also retrieve these actors.
Each table has an insert, update, delete, and format helper functions.

## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Three roles are assigned to this API: 'Casting assistant' and 'Casting director' and also 'Executive producer'.

The 'Casting assistant' role is assigned by default when someone creates an account
from the login page, has only view the list of actors and movies.


The 'Casting director' can also view movies and actors,
In addition to that, he can modify actors and movies, create and delete an actor from the app.

While the 'Executive producer' has a full control on the resources of the app, he can view, create, modify and delete actors and movies.

this is a well-detailed list that show the predefined permissions of each role:

    - Role-01:
        Casting Assistant:
            Permissions:
                - view:movies
                - view:actors
    - Role-02:
        Casting Director:
            Permissions:
                - view:movies
                - view:actors
                - patch:movies
                - patch:actors
                - create:actors
                - delete:actors
    - Role-03:
        Executive Producer:
            Permissions:
                - view:movies
                - view:actors
                - patch:movies
                - patch:actors
                - create:actors
                - create:movies
                - delete:actors
                - delete:movies


A token needs to be passed to each endpoint. 
The following only works for /actors endpoints:
The token can be retrived by following these steps:
1. Go to: http://a-djedaini.auth0.com/authorize?
        audience=fsnd&response_type=token&
        client_id=1XiBXBEECfiQf6jJpN0OE60wvLdrwFsO
        &redirect_uri=http://localhost:5000
2. Click on Login and enter the credentials into the Auth0 login page. 
   three accounts with each permission has already been created:
   - Email: assistant@udacity.com
   - Password: password

   - Email: director@udacity.com
   - Password: password

   - Email: executive@udacity.com
   - Password: password

#### GET '/movies'
Description: Show movies list.
Return: a list of all available movies, status value and the number of total movies, the movies list is paginated, use 'page' parameter to paginate data.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/movies?page=1
Sample response output:
{
  "movies": [
    {
        "id": 1,
        "title": "Harry poter",
        "release_date": "01/01/2000"
    },
    {
        "id": 2,
        "title": "Titanik",
        "release_date": "01/01/2010"
    }
  ],
  "status": true,
  "total_movies": 2
}

#### POST '/movies'
Description: Create a new movie
Return: Returns a the created resource, a success value.
Sample curl: 
curl http://localhost:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"Harry poter", "release_date": "01/01/2000"}'
Sample response output:
{
  "movies": [
    {
        "id": 1,
        "title": "Harry poter",
        "release_date": "01/01/2000"
    }
  ],
  "status": true
}

#### PATCH '/movies/{movie_id}'
Description: Update a specified movie using a given ID.
Return: a the updated movie, a status value.
Sample curl:
curl http://localhost:5000/movies/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"Harry poter (updated value)", "release_date": "01/01/2000"}'
{
  "movies": [
    {
        "id": 1,
        "title": "Harry poter (updated value)",
        "release_date": "01/01/2000"
    }
  ],
  "status": true
}

#### DELETE '/movies/{movie_id}'
Description: Delete a movie using the given ID.
Return: a list of status value, success message, and the ID of the deleted movie.
curl http://localhost:5000/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
    "movie_id": 1,
    "status": true,
    "message": "movie deleted with success"
}

#### GET '/actors'
Description: Show actors list.
Return: a list of all available actors, status value and the number of total actors, the actors list is paginated, use 'page' parameter to paginate data.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:5000/actors?page=1
Sample response output:
{
  "actors": [
    {
        "id": 1,
        "name": "Jakie chan",
        "age": 50,
        "gender": "male"
    },
    {
        "id": 2,
        "name": "Jet lie",
        "age": 60,
        "gender": "male"
    }
  ],
  "status": true,
  "total_actors": 2
}

#### POST '/actors'
Description: Create a new movie
Return: Returns a the created resource, a success value.
Sample curl: 
curl http://localhost:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name": "Jakie chan", "age": 50, "gender": "male"}'
Sample response output:
{
  "actors": [
    {
        "id": 1,
        "name": "Jakie chan",
        "age": 50,
        "gender": "male"
    }
  ],
  "status": true
}

#### PATCH '/actors/{actor_id}'
Description: Update a specified actor using a given ID.
Return: a the updated actor, a status value.
Sample curl:
curl http://localhost:5000/actors/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Jakie chan (updated value)", "release_date": "01/01/2000"}'
{
  "actors": [
    {
      "id": 1,
      "title": "Jakie chan (updated value)",
      "release_date": "01/01/2000"
    }
  ],
  "status": true
}

#### DELETE '/actors/{actor_id}'
Description: Delete a actor using the given ID.
Return: a list of status value, success message, and the ID of the deleted actor.
curl http://localhost:5000/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
  "actor_id": 1,
  "status": true,
  "message": "actor deleted with success"
}

## Testing
There are 19 unittests in test_app.py. To run this file use:
```
dropdb capstone_test
createdb capstone_test
python test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'Casting assistant' and 'Casting director' and 'Executive producer' roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://u-capstone.herokuapp.com

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving an access token to use with curl or postman.


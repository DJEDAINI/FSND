Casting Agency mini-documentation:

Roles and Permissions used:
 Role-01:
    Casting Assistant:
        Permissions:
            - view:movies
            - view:actors
 Role-02:
    Casting Director:
        Permissions:
            - view:movies
            - view:actors
            - patch:movies
            - patch:actors
            - create:actors
            - delete:actors
 Role-03:
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

Auth0 configuration:

    Domain name: http://a-djedaini.auth0.com
    Client ID: 1XiBXBEECfiQf6jJpN0OE60wvLdrwFsO

Setting up authentification using this endpoint: 
    http://a-djedaini.auth0.com/authorize?
        audience=fsnd&response_type=token&
        client_id=1XiBXBEECfiQf6jJpN0OE60wvLdrwFsO
        &redirect_uri=http://localhost:5000
Test users:
    User1:
        Email: assistant@udacity.com
        Password: password
        Role: Casting assistant
    User2:
        Email: director@udacity.com
        Password: password
        Role: Casting director
    User3:
        Email: executive@udacity.com
        Password: password
        Role: Executive producer
    
Heroku deployment URL:
    https://u-capstone.herokuapp.com/

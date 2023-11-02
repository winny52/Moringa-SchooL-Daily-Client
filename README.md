# Overview

Their are two main files that is app.py and models.app.

## App.py

### Configuration:

It configures the session, jwt, sqlalchemy, migrate

### Front-End

Routes:

Name: http://127.0.0.1:5000/signup \
method: POST \
requirements: \
username, email, role

Name: http://127.0.0.1:5000/login \
method: POST \
requirements: \
username,
password

### Routes

In the routes you have index so it doesn't throw a error when
you login.

Signup Code

1. we grab the data from the form stuff that is given to us
   from a form
2. we check to see we have the username, pass and role and
   we make sure that it is a valid user admind and user and writer
3. we hash the pass so if the db is hacked than we protect the
   real password
4. than we add to db and save it
5. than we return that it works.

Login Code

1. we grab the data from the form stuff that is given to us
   from a form
2. we check to see that info we are given is good info
3. than we add the token if things are done will

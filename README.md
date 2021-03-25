# Introduction
For my final project of the [Full Stack Web Developer Udacity Course ](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) I built my clone of Instagram called **Onstagram**.
In Onstagram users can add groups and posts images related to these groups.

# Skills covered
* Relational database with **SQL Alchemy**
* Buildung and testing **Flask** application
* Authentication (RBAC) with **Auth0** and Flask
* Deployment on on **Heroku**

# How can I access the app?
## Access via Internet (Heroku)
Onstagram is deployed on Heroku and can be accessed under
https://udacityruben.herokuapp.com/


To **log in**, enter the following credentials:

Email: postimages@udacityruben.com
Password: Udacity1!

Email: postgroup@udacityruben.com
Password: Udacity1!


## Run and access the App locally


To run the app locally you need:
* a database like PostgreSQL from postgresql.org.
* a python3 virtual environment with dependencies installed
* environment variables set
* an account Auth0.com account

Step by Step (Linux):

1. create a virtual env and install dependencies:
    * sudo apt-get install python3-venv
    * python3 -m venv env
    * source env/bin/activate
    * pip3 install -r requirements.txt
2. Create a PostgreSQL database locally 
3. Create a .env file and fill out:
    AUTH0_CLIENT_ID=
    AUTH0_DOMAIN =
    AUTH0_CLIENT_SECRET=
    AUTH0_CALLBACK_URL=
    AUTH0_AUDIENCE=
    ALGORITHMS=
    SECRET_KEY=
    DATABASE_URL=
4. Start server:
$ export FLASK_APP=app.py 
$ export FLASK_ENV=development # enables debug mode  
$ flask run --reload


# Roles and Permissions

* post:images: User can CRUD posts
    Email: postimages@udacityruben.com
    Password: Udacity1!


* post:groups: User can CRUD groups
    Email: postgroup@udacityruben.com
    Password: Udacity1!


# API endpoints

## Home
* "/", GET: Home page. Returns all existing posts and the groups to filter the posts

## Login, Logout
* "/login", GET: Redirects to Auth0 login page 
* "/callback", GET: Handles login and returns user information like the access token for the session
* "/logout", GET: Clears session and logs user out
* "/profile", GET: redirects to profile page. Shows user information like JWT and permission

## Posts
* "/posts/<group_id>", GET: Returns all existing posts filtered by the selected group
* "/posts/create", GET, POST: GET redirects to the form to create a post. POST creates the post in database, permission: post:images
* "/posts/<post_id>/delete", DELETE: deletes the selected post, permission: post:images
* "/posts/<post_id>/edit", GET, POST: GET redirects to the form to edit the selected post. POST updates the record in the database, permission: post:images

## Groups
* "/groups/create", GET, POST: GET redirects to the form to create a new group. POST creates the record in the databas, permission: post:groups
* "/groups/<group_id>/edit", GET, POST: GET redirects to the form to edit the selected group. POST updates the record in the database, permission: post:groups

# Error handling
The error codes currently returned are:

400: Bad request
401: Unauthorized
404: Resource not found
405: Method not allowed
422: Unprocessable
500: Internal server error
AuthError: Auth0 error status code and description
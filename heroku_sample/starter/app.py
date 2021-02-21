import os
from flask import Flask, render_template
from flask.templating import Environment
from models import setup_db
from flask_cors import CORS
from forms import *

def create_app(test_config=None):

    app = Flask(__name__)
    app.config['SECRET_KEY']= 'formkey' #for form wtf TODO: env var
    setup_db(app)
    CORS(app)

#DUMMY POSTS DATA
    posts = [{
        "id":1,
        "author":"Ruben Simon",
        "Title":"Blog Post 1",
        "content":"This is the content",
        "date_posted":"April 20, 2020",
    },
    {
        "id":2,
        "author":"Ruben Simon",
        "Title":"Blog Post 2",
        "content":"This is the content",
        "date_posted":"May 20, 2020",
    },
    {
        "id":3,
        "author":"Ruben Simon",
        "Title":"Blog Post 3",
        "content":"This is the content",
        "date_posted":"June 20, 2020",
    }]

#ROUTES
    @app.route('/')
    @app.route('/index')
    @app.route('/home')
    def home():
       
        return render_template("index.html")

    @app.route('/posts')
    def blog():
        return render_template("blog.html", posts=posts)

    @app.route('/posts/create')
    def create_post():
        form = PostForm()
        return render_template("new_post.html", form=form)




    return app




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
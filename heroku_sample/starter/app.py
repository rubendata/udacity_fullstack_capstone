import os
from flask import Flask, render_template, abort, jsonify
from flask.globals import request
from flask.helpers import url_for
from flask.templating import Environment
from werkzeug.utils import redirect
from models import setup_db, db, Post
from flask_cors import CORS
from forms import *
from flask_migrate import Migrate

def create_app(test_config=None):

    app = Flask(__name__)
    app.config['SECRET_KEY']= os.environ['SECRET_KEY']
    setup_db(app)
    migrate = Migrate(app, db)
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
       
        posts = Post.query.all()
        return render_template("index.html", posts=posts)

   
    
    @app.route('/posts/create', methods=['POST', 'GET'])
    def create_post():
        form = PostForm(request.form)
        
        if request.method == "POST":
            try:
                post = Post()
                form.populate_obj(post)
                post.insert()
                return redirect (url_for("home"))
                
            except Exception as e:
                print(e)
                abort(400)
        return render_template("form.html", form=form)
    
    @app.route('/login')
    def login():
        return render_template("login.html")

    return app




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
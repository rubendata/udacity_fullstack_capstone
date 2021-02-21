import os
from flask import Flask, render_template
from flask.templating import Environment
from models import setup_db
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

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
    }]

    @app.route('/')
    def get_home():
       
        return render_template("home.html", posts=posts)

    @app.route('/about')
    def get_about():
        return render_template("about.html")

    return app




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
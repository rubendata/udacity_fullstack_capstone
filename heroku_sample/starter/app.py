import os
from flask import Flask, render_template, abort, jsonify, redirect, session
from flask.globals import request
from flask.helpers import url_for
from flask.templating import Environment
from werkzeug.utils import redirect
from models import setup_db, db, Post
from flask_cors import CORS
from forms import *
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)


def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = constants.SECRET_KEY
    app.debug = True
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    
    #Set up auth0
    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if constants.PROFILE_KEY not in session:
                return redirect('/login')
            return f(*args, **kwargs)

        return decorated


#API routes
    @app.route('/')
    def home():
       
        posts = Post.query.all()
        return render_template("index.html", posts=posts)

    #calback handling for Auth0
    @app.route('/callback')
    def callback_handling():
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session[constants.JWT_PAYLOAD] = userinfo
        session[constants.PROFILE_KEY] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/profile')
    
    @app.route('/profile')
    @requires_auth
    def profile():
        return render_template('profile.html',
                            userinfo=session[constants.PROFILE_KEY],
                            userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))
    
    @app.route('/posts/create', methods=['POST', 'GET'])
    @requires_auth
    def create_post():
        form = PostForm(request.form)
        userinfo=session[constants.PROFILE_KEY],
        if request.method == "POST":
            try:
                author = userinfo[0].get("name")
                post = Post()
                form.populate_obj(post)
                post.author = author
                post.insert()
                return redirect (url_for("home"))
                
            except Exception as e:
                print(e)
                abort(400)
        return render_template("form.html", form=form)
    
    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)
    
    @app.route('/logout')
    def logout():
        try:
            session.clear()
            params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
            return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
        except Exception as e:
            print (e)

#Error handlers
    #auth error handler
    @app.errorhandler(Exception)
    def handle_auth_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response


    return app




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
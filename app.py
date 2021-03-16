import os
from flask import Flask, render_template, abort, jsonify, redirect, session
from flask.globals import request
from flask.helpers import url_for
from flask.templating import Environment
from werkzeug.utils import redirect
from models import setup_db, db, Post
from flask_cors import CORS, cross_origin
from forms import *
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import asc, desc
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

import constants

from auth import requires_auth, get_permission, verify_decode_jwt,AuthError



def create_app(test_config=None):

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.debug = True
    setup_db(app)
    migrate = Migrate(app, db)
    
    # -------------------------------------------------------------------------#
    # Enable CORS
    # -------------------------------------------------------------------------#
    CORS(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

         
    # -------------------------------------------------------------------------#
    # Setup Auth0 and login
    # -------------------------------------------------------------------------#

    
    #load .env variables for Auth0
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_BASE_URL = 'https://'+str(AUTH0_DOMAIN)
    AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

    #Auth0 configuration
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

    #callback handling for Auth0
    @app.route('/callback')
    def callback_handling():
        token = auth0.authorize_access_token()
        session['token'] = token['access_token']
        print(session['token'])
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        
        session[constants.JWT_PAYLOAD] = userinfo
        session[constants.JWT] = token['access_token']
        session[constants.PROFILE_KEY] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        session[constants.SESSION_NAME] = userinfo['name']
        
        return redirect('/profile')
    
    @app.route('/login')
    def login():
        print('Audience: {}'.format(AUTH0_AUDIENCE))
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

    # -------------------------------------------------------------------------#
    # Application Routes
    # -------------------------------------------------------------------------#
    @app.route('/')
    def home():
        permission = get_permission()
        #posts = Post.query.all()
        posts = Post.query.order_by(Post.id.desc())
        
        return render_template("index.html", posts=posts, permission=permission)

    @app.route('/profile')
    def profile():
        return render_template('profile.html',
                            userinfo=session[constants.PROFILE_KEY],
                            userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4),
                            token=session['token'])
    
    @app.route('/posts/create', methods=['POST', 'GET'])
    @cross_origin()
    @requires_auth('post:images')
    def create_post(payload):
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
    
    
    @app.route('/logout')
    def logout():
        try:
            session.clear()
            params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
            return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
        except Exception as e:
            print (e)

    # -------------------------------------------------------------------------#
    # Error handling
    # -------------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 422

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
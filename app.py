import os
from flask import Flask, render_template, abort, jsonify, redirect, session
from flask.globals import request
from flask.helpers import url_for
from flask.templating import Environment
from werkzeug.utils import redirect
from models import setup_db, db, Post, Group
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


def create_app(test_config=None):
 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.debug = True
    setup_db(app)
    migrate = Migrate(app, db)

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

    @app.route('/logout')
    def logout():
        try:
            session.clear()
            params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
            return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
        except Exception as e:
            print (e)

    # -------------------------------------------------------------------------#
    # Application Routes
    # -------------------------------------------------------------------------#
    @app.route('/')
    @cross_origin()
    def home():
        groups = Group.query.all()
        permission = get_permission()
        posts = Post.query.order_by(Post.id.desc())
        return render_template("index.html", posts=posts, groups=groups, permission=permission), 200


    @app.route("/posts/<group_id>")
    def filter_posts(group_id):
        
        groups = Group.query.all()
        permission = get_permission()
        posts = Post.query.filter_by(group_id=group_id).order_by(Post.id.desc())
        return render_template("posts.html", posts=posts, groups=groups, permission=permission)

            

    @app.route('/profile')
    @cross_origin()
    @requires_auth()
    def profile(payload):
        print(payload)
        permission = get_permission()
        return render_template('profile.html',
                            userinfo=session[constants.PROFILE_KEY],
                            userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4),
                            token=session['token'],
                            permission = permission)

    # ----------- POSTS ENDPOINTS ------------
    @app.route('/posts/create', methods=['POST', 'GET'])
    @cross_origin()
    @requires_auth('post:images')
    def create_post(payload):
        form = PostForm(request.form)
        groups = Group.query.all()
        form.group.choices = [(g.id, g.name) for g in groups]
        userinfo=session[constants.PROFILE_KEY],
        if request.method == "POST":
            try:
                
                author = userinfo[0].get("name")
                post = Post()
                form.populate_obj(post)
                post.group_id= request.form.get("group")
                post.author = author
                post.insert()
                return redirect (url_for("home"))
                
            except Exception as e:
                print(e)
                abort(400)
        return render_template("new_post.html", form=form)

    @app.route('/posts/<post_id>/delete', methods=['DELETE'])
    @cross_origin()
    @requires_auth('post:images')
    def delete_post(payload, post_id):
        post = Post.query.filter_by(id=post_id).one_or_none()
        post.delete()
        print(f"post with id {post_id} successfully deleted")
        return redirect(url_for("home"))
            
        
    
    @app.route('/posts/<post_id>/edit', methods=['GET','POST']) 
    @cross_origin()
    @requires_auth('post:images')
    def edit_post(payload, post_id):
        post = Post.query.filter_by(id=post_id).one_or_none()
        if request.method == "POST":
            post.comment=request.form.get("comment")
            post.date=request.form.get("date")
            post.title=request.form.get("title")
            post.image=request.form.get("image")
            print(post)
            post.update()
            return redirect(url_for("home"))
        
        else:
            form = PostForm(request.form)
            return render_template("edit_post.html", post=post, form=form)
        
    # ----------- GROUPS ENDPOINTS ------------
    @app.route("/groups/create", methods=['POST', 'GET'])
    @cross_origin()
    @requires_auth("post:groups")
    def create_group():
        form = GroupForm(request.form)
        groups = Group.query.all()
        if request.method == "POST":
            try:
                group = Group()
                form.populate_obj(group)
                group.insert()
                return redirect (url_for("home")),200
                
            except Exception as e:
                print(e)
                abort(400)
        return render_template("new_group.html", form=form, groups=groups)

    @app.route('/groups/<group_id>/edit', methods=['GET','POST']) #TODO: add permission check
    @cross_origin()
    @requires_auth('post:groups')
    def edit_group(payload, group_id):
        group = Group.query.filter_by(id=group_id).one_or_none()
        if request.method == "POST":
            group.name=request.form.get("name")
            print(group)
            group.update()
            return redirect(url_for("home"))
        
        else:
            form = GroupForm(request.form)
            return render_template("edit_group.html", group=group, form=form)
    

    
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
    app.run(host='0.0.0.0', port=5000, debug=True)
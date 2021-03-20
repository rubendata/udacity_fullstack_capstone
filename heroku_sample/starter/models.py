import os
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



class Post(db.Model):  
  __tablename__ = 'posts'

  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(), nullable=False)
  comment = db.Column(db.String(), nullable=False)
  author = db.Column(db.String(), nullable=False)
  image = db.Column(db.String(), nullable=False)
  date = db.Column(db.Date(), nullable=False)

  def __init__(self, **kwargs):
    super(Post, self).__init__(**kwargs)
  
  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'comment': self.comment,
      'author': self.author,
      'date': self.date,
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    date = DateField('date', validators=[DataRequired()],default= datetime.today())
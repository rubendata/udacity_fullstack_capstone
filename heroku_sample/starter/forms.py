from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    image = URLField('image', validators=[DataRequired(), url()])
    date = DateField('date', validators=[DataRequired()],default= datetime.today())


from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    image = URLField('Image', validators=[DataRequired(), url()])
    date = DateField('Date', validators=[DataRequired()],default= datetime.today())


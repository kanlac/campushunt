from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired


class LaunchForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	desc = TextField('Description', validators=[DataRequired()])
	submit = SubmitField('Launch')
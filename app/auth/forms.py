from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in') # 「记住我」
	submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Old password', validators=[DataRequired()])
	new_password = PasswordField('New password', validators=[DataRequired(), EqualTo('new_password2', message="Passwords aren't identical.")])
	new_password2 = PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField('Submit')
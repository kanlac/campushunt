from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired


class NewUserForm(FlaskForm):
	role = RadioField('用户角色', choices=[('1', '学生'), ('2', '导师')], default='1')
	username = StringField('姓名', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired()])
	add = SubmitField('添加')
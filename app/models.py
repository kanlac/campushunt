from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db, login_manager

class User(UserMixin, db.Model): # UserMixin 为 flask-login 模块标示此表为用于用户认证的表
	__tablename__ = 'User'

	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	user_role = db.Column(db.SMALLINT, nullable=False) # 1:student 2:mentor 3:admin

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self): # debug 有效
		return '<User %r>' % self.username

	def get_id(self): # flask-login 回调函数只能识别名字'id'，因此这里需要手动定义
		return (self.user_id)


# flask-login 的回调函数
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Project(db.Model):
	__tablename__ = 'Project'

	project_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	mentor_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	desc = db.Column(db.Text, nullable=False)
	status = db.Column(db.SMALLINT, nullable=False) # 1: 招募中 2: 招募中止 3: 已完结

	def __repr__(self):
		return f'<Project: {self.title}>'


class Resume(db.Model):
	__tablename__ = 'Resume'

	resume_id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	desc = db.Column(db.Text, nullable=True)
	document = db.Column(db.Boolean)

	def __repr__(self):
		return f'<Resume: {self.resume_id}>'


class Application(db.Model):
	__tablename__ = 'Application'


	application_id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey("Project.project_id"), nullable=False)
	status = db.Column(db.SMALLINT, nullable=False) # 1: 申请中 2: 签约项目 3: 已拒绝

	def __repr__(self):
		return f'<Application: Student {self.student_id} apply to Project {self.project_id}>'




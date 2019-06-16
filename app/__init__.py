from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Factory function
def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)
	from .mentor import mentor as mentor_blueprint
	app.register_blueprint(mentor_blueprint)
	from .student import student as student_blueprint
	app.register_blueprint(student_blueprint)
	from .main.errors import page_not_found, internal_server_error
	app.register_error_handler(404, page_not_found)
	app.register_error_handler(500, internal_server_error)

	return app
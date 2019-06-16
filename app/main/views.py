from flask import render_template, flash, url_for, session, redirect, request, jsonify, current_app as app, send_from_directory
from flask_login import login_required, current_user

from . import main
from .. import db
from ..models import Project, Resume, User, Application

@main.route('/', methods=['GET'])
def index():
	return render_template('projects.html', projects=Project.query.all())

@main.route('/resume/<resume_id>', methods=['GET'])
@login_required
def view_resume(resume_id):
	return render_template('resume.html', resume=Resume.query.filter_by(resume_id=resume_id).one())

@main.route('/project/<project_id>')
def project(project_id):
	project = Project.query.filter_by(project_id=project_id).one()
	mentor = User.query.filter_by(user_id=project.mentor_id).one()

	apply_status = None
	if current_user.user_role == 1:
		application = Application.query.filter_by(student_id=current_user.user_id).first()
		if application is not None:
			apply_status = application.status

	return render_template('project.html', project=project, mentor=mentor, apply_status=apply_status)


def load_config(opt):
	val = None
	try:
		val = app.config[opt]
	except:
		if val is None:
			abort(400, "%s is not configured." % opt)
	return val
from flask import render_template, flash, url_for, session, redirect, request, current_app as app
from flask_login import current_user, login_required

from . import mentor
from .. import db
from ..models import Project, Resume, Application
from .forms import LaunchForm


@mentor.route('/projects/<mentor_id>/', methods=['GET'])
@mentor.route('/projects/<mentor_id>/<status>', methods=['GET'])
@login_required
def get_projects_for(mentor_id, status=None):
	print(f"status: {status}")
	if status is not None:
		return render_template('projects.html', projects=Project.query.filter_by(mentor_id=mentor_id, status=status).all())
	return render_template('projects.html', projects=Project.query.filter_by(mentor_id=mentor_id).all())

@mentor.route('/resumes', methods=['GET'])
@login_required
def resumes():
	if current_user.user_role != 2:
		flash("You don't have access to this page.")
		return redirect(url_for('main.index'))

	rows = db.session.execute('SELECT `User`.`user_id`,\
		`User`.`username` AS `name`,\
		`Resume`.`resume_id`, \
		`Resume`.`student_id`, \
		`Resume`.`desc`, \
		`Resume`.`document`\
		FROM User INNER JOIN Resume\
		ON User.user_id=Resume.student_id')
	return render_template('resumes.html', rows=rows)

@mentor.route('/launch', methods=['GET', 'POST'])
@login_required
def launch():
	if current_user.user_role != 2:
		flash('You have no access to this page.')
		return redirect(url_for('main.index'))

	form = LaunchForm()
	if form.validate_on_submit():
		project = Project(title=form.title.data, mentor_id=current_user.user_id, desc=form.desc.data, status=1)
		db.session.add(project)
		db.session.commit()
		flash(f'Successfully launched project {form.title.data}')
		return render_template('project.html', project=project, mentor=current_user)

	return render_template('mentor/launch.html', form=form)

@mentor.route('/project/<project_id>/markas/<mark>')
@login_required
def markas(project_id, mark):
	if current_user.user_role != 2:
		flash('You have no access to this page.')
		return redirect(url_for('main.index'))

	project = Project.query.filter_by(project_id=project_id).one()
	if current_user.user_role != 2 or current_user.user_id != project.mentor_id:
		flash('You have no access to this operation.')
		return redirect(url_for('main.index'))

	project.status = mark
	db.session.commit()

	flash("Success!")
	return redirect(url_for('main.project', project_id=project_id))

@mentor.route('/project/<project_id>/manage')
@login_required
def manage(project_id):
	if current_user.user_role != 2:
		flash('You have no access to this page.')
		return redirect(url_for('main.index'))

	rows = db.session.execute('SELECT `User`.`user_id` AS `student_id`, `User`.`username`, `Resume`.`desc`, `Application`.`status`, `Application`.`application_id`, `Application`.`project_id` \
		FROM User \
		INNER JOIN Application \
		on User.user_id = Application.student_id \
		INNER JOIN Resume \
		on Application.student_id = Resume.student_id \
		WHERE `Application`.`project_id` = :i', \
		{ 'i': project_id })

	return render_template('mentor/manage.html', rows=rows)

@mentor.route('/view-resume/<student_id>')
@login_required
def view_resume(student_id):
	return render_template('resume.html', resume=Resume.query.filter_by(student_id=student_id).one_or_none())

@mentor.route('/respond/project_id:<project_id>/application_id:<application_id>/value:<value>')
@login_required
def respond(project_id, application_id, value):
	print(f'value: {value}')
	if current_user.user_role == 2 and Project.query.get(project_id).mentor_id == current_user.user_id and value in ['2', '3']:
		application = Application.query.get(application_id)
		application.status = value
		db.session.add(application)
		db.session.commit()
		flash('Operation success!')
		return redirect(url_for('mentor.manage', project_id=project_id))

	flash('You have no access to this page.')
	return redirect(url_for('main.index'))










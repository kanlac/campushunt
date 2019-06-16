from flask import render_template, flash, url_for, session, redirect, request, current_app as app, send_from_directory
from flask_login import login_required, current_user

from . import admin
from .forms import NewUserForm
from .. import db
from ..models import Project, Resume, User, Application

@admin.route('/admin/manage/student')
@login_required
def manage_student():
	return manage(1)

@admin.route('/admin/manage/mentor')
@login_required
def manage_mentor():
	return manage(2)

def manage(role):
	if current_user.user_role != 3:
		flash('You have no access to this page.')
		return redirect('main.index')

	return render_template('admin/manage.html', role=role, users=User.query.filter_by(user_role=role).all())

@admin.route('/admin/remove/<user_id>')
@login_required
def remove(user_id):
	if current_user.user_role != 3:
		flash('You have no access to this page.')
		return redirect('main.index')

	user = User.query.get(user_id)
	role = user.user_role
	db.session.delete(user)
	db.session.commit()

	flash('Operation success.')
	if role == 1:
		return redirect(url_for('admin.manage_student'))
	return redirect(url_for('admin.manage_mentor'))

@admin.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add():
	form = NewUserForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data, user_role=int(form.role.data))
		db.session.add(user)
		db.session.commit()
		flash('Success!')
		return redirect(url_for('admin.add'))

	return render_template('admin/add.html', form=form)
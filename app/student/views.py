from flask import render_template, flash, url_for, session, redirect, request, current_app as app
from flask_login import login_required, current_user
from sqlalchemy import and_, or_

from . import student
from .forms import ResumeForm
from .. import db
from ..models import Project, Resume, User, Application


@student.route('/myresume', methods=['GET', 'POST'])
@login_required
def myresume():
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	form = ResumeForm()
	resume = Resume.query.get(current_user.user_id)

	if form.validate_on_submit():
		if resume is None:
			resume = Resume(student_id=current_user.user_id)
		resume.desc = form.desc.data
		file = form.document.data
		if file is not None:
			file.save(load_config('RESUME_DIR')+str(current_user.user_id)+'.pdf')
			resume.document = True
		db.session.add(resume)
		db.session.commit()
		flash('提交成功！')
		return redirect(url_for('student.myresume'))
	elif resume is not None:
		form.desc.data = resume.desc

	return render_template('student/myresume.html', form=form, resume=resume)

@student.route('/myprojects/', methods=['GET'])
@login_required
def myprojects():
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	applications = Application.query.filter_by(student_id=current_user.user_id).all()
	projects = Project.query.filter(Project.project_id.in_([i.project_id for i in applications])).all()
	return render_template('projects.html', projects=projects)

@student.route('/apply/<project_id>')
@login_required
def apply(project_id):
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	resume = Resume.query.get(current_user.user_id)
	if resume is None or not resume.document:
		flash('请先提交简历再进行申请！')
	elif Application.query.filter_by(student_id=current_user.user_id).first() is not None:
		flash('不能同时作多份申请，请先取消其他申请再来。')
	else:
		application = Application(student_id=current_user.user_id, project_id=project_id, status=1)
		db.session.add(application)
		db.session.commit()
		flash('成功提交申请！')

	return redirect(url_for('main.project', project_id=project_id))

@student.route('/cancel/apply/<project_id>')
@login_required
def cancel_apply(project_id):
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	db.session.delete(Application.query.filter_by(student_id=current_user.user_id).first())
	db.session.commit()
	flash('Success!')
	return redirect(url_for('main.project', project_id=project_id))

@student.route('/applying')
@login_required
def applying():
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	applying = Application.query.filter_by(student_id=current_user.user_id, status=1).one_or_none() # 注意 status 为 1 的记录只能有一条
	if applying is None:
		flash('没有正在投递的项目。')
		return redirect(url_for('student.myprojects'))

	return redirect(url_for('main.project', project_id=applying.project_id))

@student.route('/applied')
@login_required
def applied():
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	applied_list = Application.query.filter_by(student_id=current_user.user_id, status=2).all()
	print(f'applied_list: {applied_list}')
	if applied_list is not None:
		# 通过了申请的项目中，未完结的项目（status = 1 or 2）至多有一个
		project = Project.query.filter(and_(Project.project_id.in_([i.project_id for i in applied_list]), or_(Project.status == 1, Project.status == 2))).one_or_none()
		print(f'project: {project}')
		if project is not None:
			return redirect(url_for('main.project', project_id=project.project_id))

	flash('当前没有签约项目。')
	return redirect(url_for('student.myprojects'))

@student.route('/completions')
@login_required
def completions():
	if current_user.user_role != 1:
		flash('You are not a student.')
		return redirect('main.index')

	applied_list = Application.query.filter_by(student_id=current_user.user_id, status=2).all()
	if applied_list is not None:
		# 通过了申请的项目中，已完结的项目（status = 3）可以有多个
		projects = Project.query.filter(and_(Project.project_id.in_([i.project_id for i in applied_list]), Project.status == 3)).all()
		if len(projects) != 0:
			return render_template('projects.html', projects=projects)

	flash('还没有已完结项目。')
	return redirect(url_for('student.myprojects'))


def load_config(opt):
	val = None
	try:
		val = app.config[opt]
	except:
		if val is None:
			abort(400, "%s is not configured." % opt)
	return val
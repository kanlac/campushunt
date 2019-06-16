def init_data(db):
	from app.models import User, Project, Resume

	db.drop_all()
	db.create_all()

	sunfa_student = User(username='孙发', password='123456', user_role=1)
	zhuwei_student = User(username='朱玮', password='123456', user_role=1)
	zhouli_student = User(username='周立', password='123456', user_role=1)
	zhangming_student = User(username='张铭', password='123456', user_role=1)

	suyi_mentor = User(username='苏义', password='123456', user_role=2)
	guoya_mentor = User(username='郭亚', password='123456', user_role=2)
	hanqingde_mentor = User(username='韩清德', password='123456', user_role=2)

	huping_admin = User(username='胡萍', password='123456', user_role=3)

	db.session.add_all([sunfa_student, zhuwei_student, zhouli_student, zhangming_student, suyi_mentor, guoya_mentor, hanqingde_mentor, huping_admin])
	db.session.commit()

	ims = Project(mentor_id=suyi_mentor.user_id, title="企业信息管理系统", desc="本项目目的是为XX企业开发一套可以投入实际使用的信息管理系统，要求在两个月内交付可演示的成品。\r\n\r\n欢迎有意向的同学申请。", status=1)
	qs = Project(mentor_id=guoya_mentor.user_id, title="基于移动端的问卷调查", desc="开发一套便于移动设备使用的问卷系统，项目开发周期约为 90 天，至多不可超过 120 天。", status=2)
	op = Project(mentor_id=hanqingde_mentor.user_id, title="活动组织与信息发布平台", desc="设计一款以同城活动为核心的社交产品，使用户能够浏览平台上的活动信息，并允许提交申请书，对于活动的发起者，能够对申请人进行管理，决定是否通过申请。", status=3)

	db.session.add_all([ims, qs, op])
	db.session.commit()

	sunfa_resume = Resume(student_id=sunfa_student.user_id, desc="擅长 Java 开发，熟悉 SSM 框架。", document=True)
	zhangming_resume = Resume(student_id=zhangming_student.user_id, desc="了解 Python 编程语言，有过三次使用 Flask web 框架的开发经验。", document=True)

	db.session.add_all([sunfa_resume, zhangming_resume])
	db.session.commit()


if __name__ == '__main__':
	from app import db, create_app

	app = create_app('development')
	app.app_context().push()
	db.init_app(app)
	init_data(db)

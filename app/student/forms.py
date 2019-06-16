from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField
from wtforms.validators import DataRequired


class ResumeForm(FlaskForm):
	desc = TextField('一句话介绍你自己', validators=[DataRequired()], render_kw={"placeholder": "导师在审阅项目申请时将看到这段文字"})
	document = FileField('上传简历', validators=[FileAllowed(['pdf'], '仅允许上传 PDF 文档。')])
	save = SubmitField('保存')
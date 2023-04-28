from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class NewJobForm(FlaskForm):
    company = StringField(validators=[DataRequired()])
    company_img = FileField(validators=[FileRequired(), FileAllowed(['jpeg', 'png'], '.jpeg or .png files only!')])
    job_title = StringField(validators=[DataRequired()])
    job_description = CKEditorField(validators=[DataRequired()])

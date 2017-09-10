from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    upload_file = FileField('Select file', validators=[DataRequired()])
    submit = SubmitField('Upload')
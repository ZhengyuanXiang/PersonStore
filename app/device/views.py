from . import device
from .forms import UploadForm
from flask import flash, redirect, render_template, request, url_for

@device.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        print(form.upload_file.data)
        flash('Upload success')
    return render_template('device/upload.html', form=form)
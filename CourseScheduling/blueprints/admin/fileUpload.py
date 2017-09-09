import os

from flask import flash, request, redirect, url_for
from flask_admin import BaseView, expose

from database.loadHelper import load_course

# file upload in admin
UPLOAD_FOLDER = '/CourseScheduling/database/txt_files/'
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FileUploadView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(path)
                load_course(path)
                return redirect(url_for('admin.index'))

        return self.render('admin/fileUpload.html')


# admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from flask_app.models.post_model import UserPosts

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/dashboard')
def route_dashboard():

    userPosts = UserPosts.get_all()

    return render_template("pages/post_feed.html", userPosts=userPosts)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## API ROUTE!!!
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    print("UPLOAD <==================")
    print(request.form['description'])
    print(request.form['file_name_url'])

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print("-- no file part")
            return 415 #UNSUPPORTED_MEDIA_TYPE   #redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print("-- No selected file")
            return 415 #UNSUPPORTED_MEDIA_TYPE  #redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data = {
                "user_id": "1",
                "description": request.form['description'],
                "image_path": url_for('static', filename='uploaded_images/' + filename)
            }
            post_id = UserPosts.save(data)
            post = UserPosts.get_by_id(post_id)
            new_post_HTML = render_template("partials/post.html", post=post)

            return {'newPostElem': new_post_HTML}, 200
    return 405 #METHOD_NOT_ALLOWED

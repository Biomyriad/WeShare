from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from flask_app.models.post_model import UserPosts

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/dashboard')
def route_dashboard():
    if not 'logged_in' in session: return redirect("/")
    
    userPosts = UserPosts.get_all()
    return render_template("pages/post_feed.html", userPosts=userPosts)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## API ROUTE!!!
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if not 'logged_in' in session: return {"errorMessages": {"auth": "unauthorized"}}, 401
    # print("UPLOAD <==================")
    # print(request.form['description'])
    # print(request.form['file_name_url'])

    if not request.form['description']:
        return {"errorMessages": {"description": "Must provide a description."}} , 400 #400 Bad Request

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print("-- no file part")
            return {"errorMessages": {"file": "No file Selected"}} , 415 #UNSUPPORTED_MEDIA_TYPE
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print("-- No selected file")
            return {"errorMessages": {"file": "No selected file"}}, 415 #UNSUPPORTED_MEDIA_TYPE
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            data = {
                "user_id": session["user"].id,
                "description": request.form['description'],
                "image_path": url_for('static', filename='uploaded_images/' + filename)
            }
            post_id = UserPosts.save(data)
            post = UserPosts.get_by_id(post_id)
            new_post_HTML = render_template("partials/post.html", post=post)

            return {'newPostElem': new_post_HTML}, 200
    return 405 #METHOD_NOT_ALLOWED

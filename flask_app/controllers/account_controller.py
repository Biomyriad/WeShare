from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash

from flask_app.models.user_model import User
from flask_app.models.post_model import UserPosts

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/account')
def route_account():
    if not 'logged_in' in session: return redirect("/")
    
    userPosts = UserPosts.get_by_user_id(session['user']['id'])
    user = User.get_by_id(session['user']['id'])

    return render_template("pages/userdetails.html", user=user, userPosts=userPosts)

@app.route('/account/<username>')
def route_by_user(username):
    print(username)
    if not 'logged_in' in session: return redirect("/")
    
    user = User.get_by_username(username)
    userPosts = UserPosts.get_by_user_id(user.id)

    return render_template("pages/userdetails.html", user=user, userPosts=userPosts)

@app.route('/account/edit', methods=['GET'])
def route_account_edit():
    if not 'logged_in' in session: return redirect("/")
    
    user = User.get_by_id(session['user']['id'])

    return render_template("pages/userinfo.html", user=user)

@app.route('/account/edit', methods=['POST'])
def route_account_edit_save():

    if not 'logged_in' in session: return redirect("/")
    user = User.get_by_id(session['user']['id'])

    form_data = request.form.to_dict()

    if not user.valid_user_info(form_data):
        return redirect("/account/edit") 

    data = {
        'id': user.id,
        'first_name': form_data['first_name'],
        'last_name': form_data['last_name'],
        'username': form_data['username'],
        'about_me': form_data['about_me']    
    }

    user.update(data)

    return redirect("/account") 
from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash

from flask_app.models.post_model import UserPosts

@app.route('/dashboard')
def route_dashboard():

    userPosts = UserPosts.get_all()

    return render_template("pages/post_feed.html", userPosts=userPosts)  
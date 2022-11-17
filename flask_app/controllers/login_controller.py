from flask_app import app
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app) 
from flask import render_template, request, redirect, url_for, session, flash

from flask_app.models.user_model import User

# set on valid login/register URL string
valid_login_url = "/dashboard"

# # # # # # # # # # #
#   Routes 
# # # # # # # # # # #

@app.route('/logout')
def route_logout():
    print("logging out ")
    if 'logged_in' in session:
        print("logged_in")
        del session["logged_in"]
    if 'user' in session:
        print("user")
        del session["user"]

    return redirect("/") 

@app.route('/login', methods=['POST', 'GET'])
def route_login():
    if request.method == 'GET':
        if "logged_in" in session:
            return redirect(valid_login_url) 
        return render_template("pages/login.html")
    else:
        
        # LOGIN
        if request.form['action'] == 'login':
            print("--- LOG button")
            session_data = User.validate_login(request.form)
            if not session_data:
                return redirect('/login')

            session['logged_in'] = True
            #session_data.id = int(session_data.id)
            print(session_data['id'])
            session['user'] = session_data
            return redirect(valid_login_url) 

        # REGISTER
        else: 
            data = {}
            data['first_name'] = request.form['first_name'].capitalize()
            data['last_name'] = request.form['last_name'].capitalize()
            data['username'] = request.form['username']
            data['email'] = request.form['email'].lower()

            print("VALID ")
            print(User.valid_register(request.form))

            if not User.valid_register(request.form):
                # set a temp session variable so that page will display registration on load
                #   - session variable will be removed in page jinja onload
                session['show_registration'] = True
                flash(data, "registration_form_data")
                return redirect('/login')

            data["password"] = bcrypt.generate_password_hash(request.form['password'])
            user_id = User.save(data)

            session['logged_in'] = True
            session['user'] = {
                "id": int(user_id),
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "username": data['username'],
                "email": data['email']
            }
            return redirect(valid_login_url) 
# End of ROUTE_LOGIN  

# # # # # # # # # # #
#   Posts
# # # # # # # # # # #

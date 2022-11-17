from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class User:
    db = "weshare"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.username = data["username"]
        self.email = data["email"]
        self.about_me = data["about_me"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#######################################################
#                       save
#######################################################
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, username, email, password, created_at, updated_at)
            VALUES (%(first_name)s,%(last_name)s, %(username)s,%(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db).query_db(query, data)


#######################################################
#                       get(s)
#######################################################

    @classmethod
    def get_by_username(cls,username):
        query = """
            SELECT id, first_name, last_name, username, email, about_me, created_at, updated_at 
            FROM users
            WHERE username = %(username)s;
        """
        data = {"username" : username}
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        
        # Didn't find a matching user
        if result == False:
            return []
        if len(result) < 1:
            return False

        result[0]['password'] = ""
        return cls(result[0])

    @classmethod
    def get_by_id(cls,id):
        query = """
            SELECT id, first_name, last_name, username, email, about_me, created_at, updated_at 
            FROM users
            WHERE users.id = %(id)s;
        """
        data = {"id" : id}
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if result == False:
            return []
        if len(result) < 1:
            return False
        result[0]['password'] = ""
        return cls(result[0])

    @classmethod
    def get_by_email_with_hash(cls, email):
        query = f"""
            SELECT * 
            FROM users 
            WHERE email=%(email)s;
        """
        data = { "email": email }
        results = connectToMySQL(cls.db).query_db(query,data)
        
        if results == False:
            return []
        if len(results) > 0:
            item = cls(results[0])
        else:
            return False

        return item


#######################################################
#                       delete
#######################################################
    @classmethod
    def delete(cls, id):
        query = """
            DELETE FROM posts WHERE id=%(id)s;
        """
        data = {"id" : id}
        return connectToMySQL(cls.db).query_db(query,data)
        

#######################################################
#                       update
#######################################################
    @classmethod
    def update(cls, data ):
        query = """
            UPDATE users 
            SET first_name=%(first_name)s, 
            last_name = %(last_name)s,
            username = %(username)s,
            about_me = %(about_me)s,
            updated_at=NOW() 
            WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)


#######################################################
#                  validate register
#######################################################
    @staticmethod
    def valid_register(data):
        is_valid = True

        # current validation is just for length or empty

        if data["first_name"] == "":
            flash({"label": "first_name", "message": "First name is required"}, "register")
            is_valid = False
        if len(data["first_name"]) <=2:
            flash({"label": "first_name", "message": "First name must be greater than 2 letters."},"register")
            is_valid = False

        if data["last_name"] == "":
            flash({"label": "last_name", "message": "Last name is required"}, "register")
            is_valid = False
        if len(data["last_name"]) <=2:
            flash({"label": "last_name", "message": "Last name must be greater than 2 letters."},"register")
            is_valid = False

        if data["username"] == "":
            flash({"label": "username", "message": "Username name is required"}, "register")
            is_valid = False
        if len(data["username"]) <=2:
            flash({"label": "Username", "message": "Must enter an email address."},"register")
            is_valid = False

        if data["email"] == "":
            flash({"label": "email", "message": "Email is required"}, "register")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash({"label": "email", "message": "Must be a valid email."},"register")
            is_valid = False

        if data["password"] == "":
            flash({"label": "password", "message": "Must enter a password."},"register")
            is_valid = False
        if len(data["password"]) <8:
            flash({"label": "password", "message": "Password must be greater then 8"},"register")
            is_valid = False

        if data["confirm"] == "":
            flash({"label": "confirm_password", "message": "Must enter a confirm password."},"register")
            is_valid = False
        if data["password"] != (data["confirm"]):
            flash({"label": "confirm_password", "message": "Passwords do not match."},"register")
            is_valid = False

        if is_valid == True:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            print(query)
            results = connectToMySQL(User.db).query_db(query,data)
            if len(results) >= 1:
                flash({"label": "email", "message": "email is already in use."}, "register")
                is_valid=False

        return is_valid


#######################################################
#                  validate login
#######################################################
    @staticmethod
    def validate_login(data):
        # missing data
        missing_login_info = False
        if data['email'] == None or data['email'] == "":
            flash({"label": "email", "message": "Please enter an email."},"login")
        if data['password'] == None or data['password'] == "":
            flash({"label": "password", "message": "Please enter your password."},"login")
        if missing_login_info:
            return False
        
        # invalid info
        user = User.get_by_email_with_hash(data['email'].lower())
        if not user:
            flash({"label": "email", "message": f"No account found for {data['email'].lower()}"},"login")
            return False
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash({"label": "password", "message": "Invalid Password, please try again."},"login")
            return False

        session_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email
            }

        return session_data


    @staticmethod
    def valid_user_info(data):
        is_valid = True

        if data["first_name"] == "":
            flash({"label": "first_name", "message": "first name is required"}, "register")
            is_valid = False
        if len(data["first_name"]) <=2:
            flash({"label": "first_name", "message": "First name must be greater than 2 letters."},"register")
            is_valid = False

        if data["last_name"] == "":
            flash({"label": "last_name", "message": "last name is required"}, "register")
            is_valid = False
        if len(data["last_name"]) <=2:
            flash({"label": "last_name", "message": "Last name must be greater than 2 letters."},"register")
            is_valid = False

        if data["username"] == "":
            flash({"label": "username", "message": "username name is required"}, "register")
            is_valid = False
        if len(data["username"]) <=2:
            flash({"label": "username", "message": "Must enter an email address."},"register")
            is_valid = False

        return is_valid



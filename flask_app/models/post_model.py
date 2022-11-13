from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.user_model import User

class UserPosts:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_by_id(cls, id):
        query = f"""
            SELECT *
            FROM posts
            JOIN users ON users.id = posts.user_id
            WHERE posts.id=%(id)s;
        """
        data = { "id": id }
        results = cls.run_query(query, data)

        if not len(results) > 0:
            return False

        post = cls(results[0])
        post.user = User({
                "id": results[0]['users.id'],
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "username": results[0]['username'],
                "email": results[0]['email'],
                "password": "",
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at']
            })

        return post

    @classmethod
    def get_all(cls):
        query = f"""
            SELECT posts.*, users.id, users.first_name, users.last_name, users.username, users.email, users.created_at, users.updated_at
            FROM posts
            JOIN users ON users.id = posts.user_id
            ORDER BY posts.created_at DESC;
        """
        results = cls.run_query(query)

        # if not len(results) > 0:
        #     return False

        posts = []
        for post in results:
            item = cls(post)
            item.user = User({
                "id": post['users.id'],
                "first_name": post['first_name'],
                "last_name": post['last_name'],
                "username": post['username'],
                "email": post['email'],
                "password": "",
                "created_at": post['users.created_at'],
                "updated_at": post['users.updated_at']
            })
            posts.append( item )
            
        return posts          

    @classmethod
    def save(cls, data ):
        query = f"""
            INSERT INTO posts ( user_id, description, image_path, created_at, updated_at) 
            VALUES ( %(user_id)s, %(description)s, %(image_path)s, NOW(), NOW() );
        """
        return cls.run_query(query, data)

    @classmethod
    def update(cls, data ):
        query = f"""
            UPDATE posts 
            SET description=%(description)s, 
            image_path=%(image_path)s, 
            updated_at=NOW() 
            WHERE id=%(id)s;
        """
        return cls.run_query(query, data)

    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM posts WHERE id=%(id)s;"
        return cls.run_query( query, data )  

    @classmethod
    def run_query(cls, query, data=None):
        return connectToMySQL('weshare').query_db( query, data )
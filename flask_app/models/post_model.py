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
            WHERE posts.id=%(id)s;
        """
        data = { "id": id }
        results = cls.run_query(query, data)

        Posts = []
        for post in results:
            Posts.append( cls(post) )
        return Posts

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

        Posts = []
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
            Posts.append( item )
            
        return Posts          

    @classmethod
    def save(cls, data ):
        query = f"""
            INSERT INTO posts ( description, image_path, created_at, updated_at) 
            VALUES ( %(description)s, %(image_path)s, NOW(), NOW() );
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
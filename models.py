# Data bases

__author__ = "Christian Ramírez de León"

import datetime
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DB = SqliteDatabase('social.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=50)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DB
        order_by = '-joined_at',

    def get_post(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            (Post.user << self.following()),
            (Post.user == self)
        )

    def following(self):
        """ The users that already follow """
        return(
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )

    def followers(self):
        """ Obtain the users that follow me"""
        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )

    @classmethod
    def create_user(cls, username, email, password):
        try:
            with DB.transaction():
                cls.create(username=username,
                           email=email,
                           password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError('User or email already exist')


class Post(Model):
    user = ForeignKeyField(
        User,
        related_name='posts'
    )
    timestamp = DateTimeField(default=datetime.datetime.now)
    content = TextField()

    class Meta:
        database = DB
        order_by = '-joined_at',


class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationship')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = DB
        indexes = (
            (('from_user', 'to_user'), True),
        )


def initialize():
    DB.connect()
    DB.create_tables([User, Post, Relationship], safe=True)
    DB.close()

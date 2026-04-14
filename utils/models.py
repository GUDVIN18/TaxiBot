from database import db
from peewee import Model, IntegerField, TextField


class User(Model):
    user_id = IntegerField()

    class Meta:
        database = db


class Settings(Model):
    bot_password = TextField()

    class Meta:
        database = db


class Filter(Model):
    user_id = IntegerField()
    price = IntegerField()
    classes = TextField()
    date = TextField()
    time = IntegerField()
    endtime = IntegerField()

    class Meta:
        database = db


class Orders(Model):
    order_id = IntegerField()

    class Meta:
        database = db

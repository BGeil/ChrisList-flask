from peewee import *
from datetime import datetime, timedelta
from flask_login import UserMixin

DATABASE = SqliteDatabase('chrislists.sqlite')

class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE



class Family_Name(Model):
	family_name = CharField()

	class Meta:
		database = DATABASE



class Family_Member(Model):
	user_id = ForeignKeyField(User, backref='users')
	family_id = ForeignKeyField(Family_Name, backref='family_names')

	class Meta:
		database = DATABASE


class Present(Model):

	present_name = CharField()
	present_description = CharField()
	present_notes = TextField()
	present_price = IntegerField()
	present_bought = BooleanField()
	present_added = DateTimeField(default=datetime.now())
	present_final = DateTimeField(default=datetime.now()) + timedelta(days=1)
	user_id = ForeignKeyField(User, backref='users')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Family_Name, Family_Member, Present], safe=True)
	print("Created tables for chrislists.sqlite, if they weren't already there")
	DATABASE.close()
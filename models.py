from peewee import *
from flask_login import UserMixin


DATABASE = SqliteDatabase('chrislists.sqlite')

# Users:

# 	First Name
# 	Last Name
# 	Email
# 	Password

class User(UserMixin, Model):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE

# Family:

# 	family_name

class Family_Name(Model):
	family_name = CharField()

	class Meta:
		database = DATABASE


# Family_Members:

# 	name = user.id
# 	family = family.id

class Family_Member(Model):
	user.id = ForeignKeyField(User, backref='users')
	family.id = ForeignKeyField(Family, backref='family_members')

# Presents:

# 	present_name
# 	present_description
# 	present_notes
# 	present_price
# 	present_bought
# 	24hour_timer
# 	user.id 

class Present(Model):

	present_name = CharField()
	present_description = CharField()
	present_notes = TextField()
	present_price = IntegerField()
	present_bought = BooleanField()
	# 24hour_timer = IntegerField()
	user.id = ForeignKeyField(User, backref='users')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Family_Name, Family_Member, Present], safe=True)
	print("Created tables for chrislists.sqlite, if they weren't already there")
	DATABASE.close()
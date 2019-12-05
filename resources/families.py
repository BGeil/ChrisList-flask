import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

families = Blueprint('families', 'families')


# idea: for later: helper function to see if current_user is a member of a family given its id



#index route to all the current user's families
@families.route('/', methods=['GET'])
def get_users_families():
	try: 
		query = models.Family_Member.select().where(models.Family_Member.user_id == current_user.id)
		families = [model_to_dict(family) for family in query]
		[family["user_id"].pop("password") for family in families]
		return jsonify(data=families, status={'code': 200, 'message': 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'}), 401



# index route to the current user's currently selected individual family members
# they just now saw the list (including ids)
@families.route('/<id>', methods=['GET']) 
def get_users_individual_family(id):
	try: 
		# get all memberships where the family id is the one from url params
		query = models.Family_Member.select().where(models.Family_Member.id == id)
		memberships = [model_to_dict(membership) for membership in query]
		[membership["user_id"].pop("password") for membership in memberships]
		return jsonify(data=memberships, status={'code': 200, 'message': 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={'message': 'Error'}, status={'code': 401, 'message': 'Error getting resources'}), 401

 
#Create Route
# this route creates a family and adds currently logged in user as a member
# will check if family exists(stretch goal)
@families.route('/', methods=['POST'])
def create_family():
	payload = request.get_json()
	try:
		family = models.Family_Name.create(**payload)
		family_dict = model_to_dict(family)
		# add current user to family
		user = models.Family_Member.create(user_id=current_user.id,
			family_id=family.id)
		user_dict = model_to_dict(user)
		user_dict["user_id"].pop("password")
		return jsonify(data={'family': family_dict, 'user': user_dict}, status={'code': 201, 'message': 'Success'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'}), 401


# This route will be a query search to search all users and list them out based on query
@families.route('/search/<query>', methods=['GET'])
def get_users_search_form(query):
	try:
		query = models.User.select().where(models.User.first_name == query.lower()) #lowercase	
		users = [model_to_dict(users) for users in query]
		[user.pop('password') for user in users]
		return jsonify(data=users, status={'code': 200, 'message': 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'}), 401
	

# This route will add users to a family (aka adding family members to a family)
@families.route('/add_member', methods=['POST'])
def add_users_to_families():
	payload = request.get_json()
	family_member = models.Family_Member.create(**payload)
	family_member_dict = model_to_dict(family_member)
	family_member_dict["user_id"].pop("password")
	return jsonify(data=family_member_dict, status={'code': 200, 'message': 'Success'})



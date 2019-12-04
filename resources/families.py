import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

families = Blueprint('families', 'families')

#index route 
@families.route('/', methods=['GET'])
def get_users_family_names():
	try: 
		query = models.Family_Name.select().where(models.Family_Name.user_id == current_user.id)
		family_names = [model_to_dict(family_names) for family_names in query]
		print(family_names)
		
		[family_name["user_id"].pop("password") for family_name in family_names]
		
		return jsonify(data=family_names, status={'code': 200, 'message': 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'}), 401


#Create Route
@families.route('/', methods=['POST'])
def create_family():
	payload = request.get_json()

	print(payload)
	family_names = models.Family_Name.create(**payload,
		user_id=current_user.id)

	print(family_names.__dict__)
	print(dir(family_names))
	print(model_to_dict(family_names), 'model to dict')
	family_names_dict = model_to_dict(family_names)
	return jsonify(data=family_names_dict, status={'code': 201, 'message': 'Success'})



# This route will be a query search to search all users and list them out based on query
@families.route('/', methods=['GET'])
def get_users_families():
	try:
		query = models.Family_Name.select().where(models.Family_Name.user_id == current_user.id)
		family_names = [model_to_dict(family_names) for family_names in query]
		print(family_names)

		[family_name['user_id'].pop('password') for family_name in family_names]

		query = models.User.select().where(models.User.first_name == payload['query'])
		users = [model_to_dict(users) for users in query]
		print(users)
		[user['user_id'].pop('password') for user in users]


		return jsonify(data=families, status={'code': 200, 'message': 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'}), 401
	

# This route will add family members to a family
@families.route('/<user_id>', methods=['POST'])
def add_users_to_families(user_id):
	payload = request.get_json()
	print(payload)

	family_members = models.Family_Members.create(**payload,
		user_id=user_id,
		family_id=payload['family_name'])

	print(family_members.__dict__)
	print(dir(family_members))
	print(model_to_dict(family_members), 'model to dict')

	family_members_dict = model_to_dict(family_members)
	return jsonify(data=family_members_dict, status={'code': 201, 'message': 'Success'})







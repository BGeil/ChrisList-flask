import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

presents = Blueprint('presents', 'presents')


# Index route thats shows all your presents
@presents.route('/', methods=['GET'])
def get_all_presents():
	try:
		query = models.Present.select().where(models.Present.user_id == current_user.id)
		presents = [model_to_dict(presents) for presents in query]
		print(presents)

		[present['user_id'].pop('password') for present in presents]

		return jsonify(data=presents , status={'code': 200, 'message' : 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message' : 'Error getting resources'}), 401


# Index route that shows all the presents of all the family members in a family
@presents.route('/familypresents', methods=['GET'])
def show_family_presents():
	try:
		query = models.Present.select()
		presents = [model_to_dict(presents) for presents in query]
		print(presents)
		[present['family_id'].pop('password') for present in presents]

		return jsonify(data=presents , status={'code': 200, 'message' : 'Successful'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message' : 'Error getting resources'}), 401

# Create Route
@presents.route('/', methods=['POST'])
def create_present():
	payload = request.get_json()
	print(payload)
	print("current user id", current_user.id )
	presents = models.Present.create(**payload, family_member_id=current_user.id)
	print(presents.__dict__)
	print(dir(presents))

	# print(model_to_dict(presents), 'model to dict')
	presents_dict = model_to_dict(presents)
	# presents_dict["user_id"].pop("password") 
	return jsonify(data=presents_dict, status={'code': 201, 'message': 'Success'})



# Show Route
@presents.route('/<id>', methods=['GET'])
def get_one_present(id):
	print(id)
	present = models.Present.get_by_id(id)
	present_dict = model_to_dict(present)

	return jsonify(data=present_dict, status={'code': 200, "message": "Found present with id {}".format(present.id)}), 200


#Update Route
@presents.route('/<id>', methods=['PUT'])
def update_presents(id):
	payload = request.get_json()
	print(payload)
	query = models.Present.update(**payload).where(models.Present.id == id)
	query.execute()
	presents = models.Present.get_by_id(id)

	presents_dict = model_to_dict(presents)
	return jsonify(data=presents_dict, status={'code': 200, 'message':'Resource updated successfully!'})



#Delete Route 
@presents.route('/<id>', methods=['Delete'])
def delete_presents(id):
	query = models.Present.delete().where(models.Present.id == id)
	query.execute()

	return jsonify(data='Resource has successfully been deleted', status={
		'code': 200, 'message': 'Resource has been deleted successfully'
		})
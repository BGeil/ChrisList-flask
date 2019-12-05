from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
from resources.users import users
from resources.families import families
from resources.presents import presents

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'This is a super secret key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return none


@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(families, origins=['http://localhost:3000'], supports_credentials=True)
CORS(presents, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(families, url_prefix='/api/v1/families')
app.register_blueprint(presents, url_prefix='/api/v1/presents')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

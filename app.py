# from flask import Flask, jsonify, g
# from flask_cors import CORS
# from flask_login import LoginManager
# from resources.listings import listings
# from resources.agents import agents

# import models

# DEBUG = True
# PORT = 8000

# app = Flask(__name__)
# app.secret_key = 'This is a super secret key'

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_agent(agentid):
# 	try:
# 		return models.Agent.get(models.Agent.id == agentid)
# 	except models.DoesNotExist:
# 		return none


# @app.before_request
# def before_request():
# 	g.db = models.DATABASE
# 	g.db.connect()

# @app.after_request
# def after_request(response):
# 	g.db.close()
# 	return response

# CORS(listings, origins=['http://localhost:3000'], supports_credentials=True)
# CORS(agents, origins=['http://localhost:3000'], supports_credentials=True)

# app.register_blueprint(listings, url_prefix='/api/v1/listings')
# app.register_blueprint(agents, url_prefix='/api/v1/agents')

# if __name__ == '__main__':
# 	models.initialize()
# 	app.run(debug=DEBUG, port=PORT)

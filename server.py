import os
from flask import Flask, Response, jsonify, request, json

# create a flask application
app = Flask(__IceCream__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    return jsonify(name='Ice Cream REST API Service', version='1.0', url='/ice-creams'), HTTP_200_OK

######################################################################
# Add an Ice Cream Flavor
######################################################################
@app.route('/ice-creams', methods=['POST'])
def create_flavor():
	payload = json.loads(request.data)
	if is_valid(payload):
		id = payload['name']
		if ice_creams.has_key(id):
			message = {'error': 'Ice Cream Flavor %s already exists' % id }
			rc = HTTP_409_CONFLICT
		else:
			ice_creams[id] = {'name': payload['name'], 'description': payload['description'], 'status': payload['status'], 'base': payload['base'], 'price': payload['price'], 'popularity': payload['popularity']}
			message = ice_creams[id]
			rc = HTTP_201_CREATED
	else:
		message = { 'error' : 'Data is not valid' }
		rc = HTTP_400_BAD_REQUEST

	return reply(message, rc)

######################################################################
# utility functions
######################################################################
def reply(message, rc):
	response = Response(json.dumps(message))
	response.headers['Content-Type'] = 'application/json'
	response.status_code = rc
	return response

def is_valid(data):
	valid = False
	try:
		name = data['name']
		description = data['description']
		status = data['status']
		base = data['base']
		price = data['price']
		popularity = data['popularity']
		valid = True
	except KeyError as err:
		app.logger.error('Missing value error: %s', err)
	return valid


	

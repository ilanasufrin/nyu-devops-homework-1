# Copyright 2016 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import redis
from flask import Flask, Response, jsonify, request, json

# ice-cream Model for testing
icecreams = {'Vanilla': {'name': 'Vanilla', 'description': 'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.3/5'}, \
            'Chocolate': {'name': 'Chocolate', 'description': 'Ice Cream made from real cacao bean, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.8/5'}, \
            'Strawberry': {'name': 'Strawberry', 'description': 'Ice Cream made from real strawberry, milk and sweet cream','status':'melted','base':'almond milk','price':'$4.49','popularity':'3.8/5'} \
            }

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# Create Flask application
app = Flask(__name__)

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    docs = {
      "name": "Ice-cream REST API",
      "version": "1.0",
      "domain": "http://devops-icecream.mybluemix.net/",
      "url": [
        {
          "url":"/ice-cream",
          "method": "GET",
          "description": "List all icecream information"
        },{
          "url":"/ice-cream/<id>",
          "method": "GET",
          "description": "Get icecream with id <id>"
        },{
          "url":"/ice-cream",
          "method": "POST",
          "description": "Create an icecream",
          "sample_body": {
            "id": 0,
            "name": "Vanilla",
            "description": "Ice Cream made from real vanilla, milk and sweet cream",
            "status": "frozen",
            "base": "milk",
            "price": "$4.49",
            "popularity": "4.3/5"
          }
        },{
          "url":"/ice-cream/<id>",
          "method": "DELETE",
          "description": "Delete an icecream"
        },{
          "url":"/ice-cream/<id>",
          "method": "PUT",
          "description": "Update ice-cream with id <id>. Updates description and status",
          "sample_body": {
            "id": 0,
            "name": "Vanilla",
            "description": "Ice Cream made from real vanilla, milk and sweet cream",
            "status": "frozen",
            "base": "milk",
            "price": "$4.49",
            "popularity": "4.3/5"
          }
        }
      ]
    }
    return reply(docs, HTTP_200_OK)

######################################################################
# LIST ALL resourceS
######################################################################
@app.route('/ice-creams', methods=['GET'])
def list_all_ice_creams():
     results = []
     for key, value in icecreams.iteritems():
         results.append(icecreams[key])
     return reply(results, HTTP_200_OK)

######################################################################
# RETRIEVE A resource
######################################################################
@app.route('/ice-creams/<id>', methods=['GET'])
def get_an_ice_cream(id):
     if (icecreams).has_key(id):
         message = icecreams[id]
         rc = HTTP_200_OK
     else:
         message = { 'error' : 'Ice-cream %s was not found' % id }
         rc = HTTP_404_NOT_FOUND

     return reply(message, rc)

######################################################################
# ADD A NEW Ice cream flavor
######################################################################
@app.route('/ice-cream', methods=['POST'])
def create_flavor():
    global flavors
    payload = json.loads(request.data)
    id = str(payload['id'])
    flavors = get_from_redis('flavors')
    if flavors.has_key(id):
        message = { 'error' : 'Flavor %s already exists' % id }
        rc = HTTP_409_CONFLICT
    else:
        flavors[id] = payload
        message = flavors[id]
        rc = HTTP_201_CREATED
        json_users=json.dumps(flavors)
        redis_server.set('flavors',json_users)
    return reply(message, rc)

######################################################################
# UPDATE AN EXISTING resource
######################################################################
@app.route('/ice-creams/<id>', methods=['PUT'])
def update_ice_cream(id):
     payload = json.loads(request.data)
     if icecreams.has_key(id):
         icecreams[id] = {'name': payload['name'], 'description': payload['description'], 'status': payload['status'], 'base': payload['base'], 'price': payload['price'], 'popularity': payload['popularity']}
         message = icecreams[id]
         rc = HTTP_200_OK
     else:
         message = { 'error' : 'Ice-cream %s was not found' % id }
         rc = HTTP_404_NOT_FOUND

     return reply(message, rc)

######################################################################
# DELETE A resource
######################################################################
@app.route('/ice-creams/<id>', methods=['DELETE'])
def delete_flavor(id):
    if icecreams.has_key(id):
        del icecreams[id]
        return '', HTTP_204_NO_CONTENT
    else:
        return '', HTTP_204_NO_CONTENT


############################################################################
# QUERY Resources by some attribute of the Resource - Type: Melted/Frozen
############################################################################
@app.route('/ice-creams/<id>', methods=['GET'])
def list_resources_by_type():
	results = icecreams.values()
	status = request.args.get('status')
	if status:
		results = []
		for key, value in icecreams.iteritems():
			if value['status'] == 'status':
				results.append(icecreams[key])

	return reply(results, HTTP_200_OK)

######################################################################
# PERFORM some Action on the Resource - UPDATE a resource status
# http://localhost:5000/ice-creams?status=melt changes the status of all ice creams to melted
# http://localhost:5000/ice-creams?status=freeze changes the status of all ice creams to frozen
######################################################################

@app.route('/ice-creams', methods=['PUT'])
def  put_ice_cream_status():
     statusupdate = request.args.get('status')
     if statusupdate == 'melt':
          for key, value in icecreams.iteritems():
#              status = icecreams[key]['status']
#              if status == 'frozen':
               icecreams[key]['status'] = 'melted'
               message = { 'success' : 'All ice creams have been melted.'}
               rc = HTTP_200_OK
     elif statusupdate == 'freeze':
          for key, value in icecreams.iteritems():
#              status = icecreams[key]['status']
#              if status == 'melt':
               icecreams[key]['status'] = 'frozen'
               message = { 'success' : 'All ice creams have been frozen.'}
               rc = HTTP_200_OK
     else:
          message = { 'error' : 'No ice creams were found therefore none could have there status changed to %s'  %  statusupdate}
          rc = HTTP_404_NOT_FOUND

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

# Initialize Redis
def init_redis(hostname, port, password):
    # Connect to Redis Server
    global redis_server
    redis_server = redis.Redis(host=hostname, port=port, password=password)
    if not redis_server:
        print('*** FATAL ERROR: Could not conect to the Redis Service')
        exit(1)

def get_from_redis(s):
    unpacked = redis_server.get(s)
    if unpacked:
        return json.loads(unpacked)
    else:
        return {}

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # Get bindings from the environment
    # Get the crdentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        VCAP_SERVICES = os.environ['VCAP_SERVICES']
        services = json.loads(VCAP_SERVICES)
        redis_creds = services['rediscloud'][0]['credentials']
        # pull out the fields we need
        redis_hostname = redis_creds['hostname']
        redis_port = int(redis_creds['port'])
        redis_password = redis_creds['password']
    else:
        redis_hostname = '127.0.0.1'
        redis_port = 6379
        redis_password = None

    init_redis(redis_hostname, redis_port, redis_password)
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=True)

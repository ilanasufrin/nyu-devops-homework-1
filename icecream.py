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
from redis import Redis
from redis.exceptions import ConnectionError
from flask import Flask, Response, jsonify, request, json

# ice-cream Model for testing
flavors = {'Vanilla': {'name': 'Vanilla', 'description': 'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.3/5'}, \
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

debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '5000')

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
# LIST ALL resources
# EXAMPLE http://localhost:5000/ice-cream
# EXAMPLE http://localhost:5000/ice-cream?status=frozen
######################################################################
@app.route('/ice-cream', methods=['GET'])
def list_all_ice_creams():
    global flavors
    flavors = get_from_redis('flavors')
    results = []
    # check to see if there is a query parameter to use as a filter
    status = request.args.get('status')
    if status:
        for key, value in flavors.iteritems():
            if value['status'] == status:
                results.append(flavors[key])
    else:
        results = flavors.values()
    return reply(results, HTTP_200_OK)


######################################################################
# RETRIEVE A resource
######################################################################
@app.route('/ice-cream/<id>', methods=['GET'])
def get_an_ice_cream(id):
    global flavors
    flavors = get_from_redis('flavors')
    if (flavors).has_key(id):
        message = flavors[id]
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
    if is_valid(payload):
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
            redis.set('flavors',json_users)
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST
    return reply(message, rc)

######################################################################
# UPDATE AN EXISTING resource
######################################################################
@app.route('/ice-cream/<id>', methods=['PUT'])
def update_ice_cream(id):
    global flavors
    flavors = get_from_redis('flavors')
    payload = json.loads(request.data)
    if flavors.has_key(id):
        flavors[id] = {'name': payload['name'], 'description': payload['description'], 'status': payload['status'], 'base': payload['base'], 'price': payload['price'], 'popularity': payload['popularity'],'id':payload['id']}
        json_flavors=json.dumps(flavors)
        redis.set('flavors',json_flavors)
        message = flavors[id]
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Ice-cream flavor %s was not found' % id }
        rc = HTTP_404_NOT_FOUND
    return reply(message, rc)

######################################################################
# DELETE A resource
######################################################################
@app.route('/ice-cream/<id>', methods=['DELETE'])
def delete_flavor(id):
    global flavors
    flavors = get_from_redis('flavors')
    if not flavors.has_key(id):
        return reply({ 'error' : 'Ice-cream flavor %s doesn\'t exist' % id }, HTTP_400_BAD_REQUEST)
    del flavors[id];
    json_flavors=json.dumps(flavors)
    redis.set('flavors',json_flavors)
    return reply('', HTTP_204_NO_CONTENT)

######################################################################
# PERFORM some Action on a Resource - UPDATE a resource status
# /ice-cream/<id>/freeze - update the status to frozen
#/ice-cream/<id>/melt -  update the status to melted
######################################################################

@app.route('/ice-cream/<id>/<status>', methods=['PUT'])
def change_status_freeze(id,status):
    global flavors
    flavors = get_from_redis('flavors')
    if flavors.has_key(id):
        if status == 'freeze':
            flavors[id] ['status']= 'frozen'
        elif status == 'melt':
            flavors[id] ['status']= 'melted'
        json_flavors=json.dumps(flavors)
        redis.set('flavors',json_flavors)
        message = flavors[id]
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Ice-cream flavor %s was not found' % id }
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
        id = data['id']
        valid = True
    except KeyError as err:
        app.logger.error('Missing value error: %s', err)
    return valid

# Initialize Redis

def seed_database_with_data():
  global flavors
  flavors = get_from_redis('flavors')

  if not flavors:
      data = {0: {"name": "Vanilla","description": "Ice Cream made from real vanilla, milk and sweet cream","status": "frozen","base": "milk","price": "$4.49","popularity": "4.3/5","id":"0"}, 1: {"name": "Chocolate","description": "Yummy chocolate ice cream","status": "melted","base": "frozen yogurt","price": "$5.99","popularity": "4.8/5","id":"1"}}
      redis.set('flavors', json.dumps(data))

def get_from_redis(s):
    unpacked = redis.get(s)
    if unpacked:
        return json.loads(unpacked)
    else:
        return {}

######################################################################
# Connect to Redis and catch connection exceptions
######################################################################

def connect_to_redis(hostname, port, password):
    redis = Redis(host=hostname, port=port, password=password)
    try:
        redis.ping()
    except ConnectionError:
        redis = None
    return redis

######################################################################
# INITIALIZE Redis
# This method will work in the following conditions:
#   1) In Bluemix with Redsi bound through VCAP_SERVICES
#   2) With Redis running on the local server as with Travis CI
#   3) With Redis --link ed in a Docker container called 'redis'
######################################################################
def inititalize_redis():
    global redis
    redis = None
    # Get the crdentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        print "Using VCAP_SERVICES..."
        VCAP_SERVICES = os.environ['VCAP_SERVICES']
        services = json.loads(VCAP_SERVICES)
        creds = services['rediscloud'][0]['credentials']
        print "Conecting to Redis on host %s port %s" % (creds['hostname'], creds['port'])
        redis = connect_to_redis(creds['hostname'], creds['port'], creds['password'])
    else:
        print "VCAP_SERVICES not found, checking localhost for Redis"
        redis = connect_to_redis('127.0.0.1', 6379, None)
        if not redis:
            print "No Redis on localhost, pinging: redis"
            response = os.system("ping -c 1 redis")
            if response == 0:
                print "Connecting to remote: redis"
                redis = connect_to_redis('redis', 6379, None)
    seed_database_with_data()
    if not redis:
        # if you end up here, redis instance is down.
        print '*** FATAL ERROR: Could not connect to the Redis Service'
        exit(1)
######################################################################
#   M A I N
######################################################################

if __name__ == "__main__":
    print "Ice-cream Service Starting..."
    inititalize_redis()
    app.run(host='0.0.0.0', port=int(port), debug=debug)

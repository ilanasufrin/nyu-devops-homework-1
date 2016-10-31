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
from flask import Flask, Response, jsonify, request, json

# ice-cream Model for testing
icecreams = {'Vanilla': {'name': 'Vanilla', 'description': 'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.3/5'}, 'Chocolate': {'name': 'Chocolate', 'description': 'Ice Cream made from real cacao bean, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.8/5'}, 'Strawberry': {'name': 'Strawberry', 'description': 'Ice Cream made from real strawberry, milk and sweet cream','status':'melted','base':'almond milk','price':'$4.49','popularity':'3.8/5'}}

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
    return jsonify(name='Ice Cream REST API Service', version='1.0', url='/ice-creams'), HTTP_200_OK

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
@app.route('/ice-creams', methods=['POST'])
def create_flavor():
    payload = json.loads(request.data)
    if is_valid(payload):
        id = payload['name']
        if icecreams.has_key(id):
            message = {'error': 'Ice Cream Flavor %s already exists' % id }
            rc = HTTP_409_CONFLICT
        else:
            icecreams[id] = {'name': payload['name'], 'description': payload['description'], 'status': payload['status'], 'base': payload['base'], 'price': payload['price'], 'popularity': payload['popularity']}
            message = icecreams[id]
            rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

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
    del icecreams[id]
    return '', HTTP_204_NO_CONTENT
    
    
######################################################################
# RETRIEVE ice-creams based on popularity
# http://localhost:5000/ice-creams?popularity=4 fetches all the
# ice creams with popularity greater equal to 4.0
######################################################################
@app.route('/ice-creams/', methods=['GET'])
def get_popular_ice_cream():
     pop = request.args.get('popularity')
     results = []
     for key, value in icecreams.iteritems():
         #popularity is stored as a string 4.3/5,
         #hence split on '/' and take the first item(index = 0)
         # to get 4.3
         icepop = icecreams[key]['popularity'].split("/")[0]
         if float(icepop) >= float(pop):
             results.append(icecreams[key])
             rc = HTTP_200_OK
     if not results:
         message = { 'error' : 'Ice-cream popularity greater than %s was not found' % pop}
         rc = HTTP_404_NOT_FOUND
         return reply(message, rc)
     else:     
         return reply(results, rc)    

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

@app.route('/ice-creams/', methods=['PUT'])
def  put_ice_cream_status():
     payload = json.loads(request.data)
     statusupdate = request.args.get('status')
     if statusupdate == 'melt':
          for key, value in icecreams.iteritems():
               status = icecreams[key]['status']
               if status == 'frozen':
                    icecreams[icecreams[key][0]['id']] = {'name': payload['name'], 'description': payload['description'], 'status' : 'melted', 'base': payload['base'], 'price':payload['price'], 'popularity': payload['popularity']}
                    rc = HTTP_200_OK
     if statusupdate == 'freeze':
          for key, value in icecreams.iteritems():
               status = icecreams[key]['status']
               if status == 'melt':
                    icecreams[icecreams[key][0]['id']]  = {'name': payload['name'], 'description': payload['description'], 'status' : 'frozen', 'base': payload['base'], 'price':payload['price'], 'popularity': payload['popularity']}
                    rc = HTTP_200_OK
     else:
          message = { 'error' : 'No ice creams were found therefore none could have there status changed to'  %  statusupdate}
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

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # Get bindings from the environment
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=True)

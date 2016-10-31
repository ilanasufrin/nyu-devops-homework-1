# run with:
# python -m unittest discover

import unittest
import json
import icecream

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestIceCreamicecream(unittest.TestCase):

    def setUp(self):
        icecream.app.debug = True
        self.app = icecream.app.test_client()
        icecream.icecreams = {'Vanilla': {'name': 'Vanilla', 'description': 'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.3/5'}, 'Chocolate': {'name': 'Chocolate', 'description': 'Ice Cream made from real cacao bean, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.8/5'}, 'Strawberry': {'name': 'Strawberry', 'description': 'Ice Cream made from real strawberry, milk and sweet cream','status':'melted','base':'almond milk','price':'$4.49','popularity':'3.8/5'}}

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('Ice Cream REST API Service' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )

    def test_get_ice_creams_list(self):
        resp = self.app.get('/ice-creams')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )

    def test_get_ice_creams(self):
        resp = self.app.get('/ice-creams/Vanilla')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'Vanilla')

    def test_create_ice_creams(self):
        # save the current number of ice creams for later comparison
        ice_cream_count = self.get_ice_creams_count()
        # add a new ice cream
        new_ice_cream = {'name': 'Caramel', 'description': 'Ice Cream made from caramel flavoring, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.3/5'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-creams', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Caramel')
        # check that count has gone up and includes sammy
        resp = self.app.get('/ice-creams')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == ice_cream_count + 1 )
        self.assertTrue( new_ice_cream in data )

    def test_update_ice_creams(self):
        new_ice_cream = {'name': 'Vanilla', 'description':'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'2.3/5'}
        data = json.dumps(new_ice_cream)
        resp = self.app.put('/ice-creams/Vanilla', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['popularity'] == '2.3/5')

    def test_delete_ice_creams(self):
        # save the current number of ice creams for later comparison
        ice_creams_count = self.get_ice_creams_count()
        # delete a ice cream
        resp = self.app.delete('/ice-creams/Vanilla', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_ice_creams_count()
        self.assertTrue ( new_count == ice_creams_count - 1)

    def test_create_ice_cream_with_no_name(self):
        new_ice_cream = {'description': 'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.3/5'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-creams', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_query_ice_creams_list(self):
        resp = self.app.get('/ice-creams', query_string='status=melted')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertTrue(query_item['status'] == 'melted')


######################################################################
# Utility functions
######################################################################

    def get_ice_creams_count(self):
        # save the current number of ice creams
        resp = self.app.get('/ice-creams')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # print 'resp_data: ' + resp.data
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()

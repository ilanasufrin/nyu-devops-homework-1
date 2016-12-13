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
class TestIcecreamService(unittest.TestCase):

    def setUp(self):
        icecream.app.debug = True
        self.app = icecream.app.test_client()
        icecream.inititalize_redis()
        TestIcecreamService.setup_data(self)

    def tearDown(self):
        TestIcecreamService.delete_data(self)
        self.app = None

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('Swagger UI' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )

    def test_api_url(self):
        resp = self.app.get('/')
        self.assertTrue ('Ice-cream REST API' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )

    def test_get_ice_cream_list(self):
        resp = self.app.get('/ice-cream')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )

    def test_get_ice_cream_by_id(self):
        resp = self.app.get('/ice-cream/500')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'Matcha')

    def test_get_non_existing_icecream(self):
        resp = self.app.get('/ice-cream/100')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )

    def test_perform_action_on_non_existing_icecream(self):
        resp = self.app.put('/ice-cream/100/melt')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )

    def test_create_ice_cream(self):
        # save the current number of ice creams for later comparison
        ice_cream_count = self.get_ice_creams_count()
        # add a new ice cream
        new_ice_cream = {'name': 'Caramel', 'description': 'Ice Cream made from caramel sauce, milk and sweet cream','status':'frozen','base':'milk','price':'$4.49','popularity':'4.0/5','id':'503'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-cream', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'Caramel')
        # check that count has gone up and includes sammy
        resp = self.app.get('/ice-cream')
        data = json.loads(resp.data)
        x = {}
        for i in data:
            if i['name'] == 'Caramel':
                x = i
                break
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == ice_cream_count + 1 )
        self.assertTrue( x['name']== 'Caramel')

    def test_create_existing_icecream(self):
        new_ice_cream = {'name': 'Vanilla', 'description':'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.99','popularity':'4.75/5','id':'500'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-cream', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_409_CONFLICT )


    def test_update_ice_cream(self):
        new_ice_cream = {'name': 'Matcha', 'description':'Ice Cream made from finest Japanese Matcha green tea, milk and sweet cream','status':'frozen','base':'almond milk','price':'$5.99','popularity':'4.5/5','id':'500'}
        data = json.dumps(new_ice_cream)
        resp = self.app.put('/ice-cream/500', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['popularity'] == '4.5/5')
        self.assertTrue (new_json['price'] == '$5.99')

    def test_update_non_existing_icecream(self):
        new_ice_cream = {'name': 'Vanilla', 'description':'Ice Cream made from real vanilla, milk and sweet cream','status':'frozen','base':'milk','price':'$4.99','popularity':'4.75/5','id':'100'}
        data = json.dumps(new_ice_cream)
        resp = self.app.put('/ice-cream/100', data=data, content_type='application/json')
        self.assertTrue( resp.status_code ==HTTP_404_NOT_FOUND )

    def test_delete_ice_cream(self):
        # save the current number of ice creams for later comparison
        ice_creams_count = self.get_ice_creams_count()
        # delete a ice cream
        resp = self.app.delete('/ice-cream/501', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_ice_creams_count()
        self.assertTrue ( new_count == ice_creams_count - 1)


    def test_query_ice_creams_by_status(self):
        resp = self.app.get('/ice-cream?status=melted')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        #self.assertTrue( len(resp.data) > 0 )
        if len(resp.data) > 0:
            data = json.loads(resp.data)
            x = {}
            for i in data:
                x = i;
                self.assertTrue(x['status'] == 'melted')
                self.assertFalse(x['status'] == 'frozen')
        resp = self.app.get('/ice-cream?status=frozen')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        #self.assertTrue( len(resp.data) > 0 )
        if len(resp.data) > 0:
            data = json.loads(resp.data)
            x = {}
            for i in data:
                x = i;
                self.assertFalse(x['status'] == 'melted')
                self.assertTrue(x['status'] == 'frozen')

    def test_perform_action_change_status_of_icecream(self):
        resp = self.app.put('/ice-cream/500/melt')
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        self.assertTrue(data['status'] == 'melted')
        self.assertTrue('melted' in resp.data)
        self.assertFalse('frozen' in resp.data)
        resp = self.app.put('/ice-cream/500/freeze')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        data = json.loads(resp.data)
        self.assertTrue(data['status'] == 'frozen')
        self.assertFalse('melted' in resp.data)
        self.assertTrue('frozen' in resp.data)

    def test_create_ice_cream_with_no_name(self):
        new_ice_cream = {'description':'Ice Cream made from real matcha, milk and sweet cream','status':'frozen','base':'almond milk','price':'$4.99','popularity':'4.35/5','id':'10'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-cream', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )


######################################################################
# Swagger Tests
######################################################################

    def test_index(self):
        response = self.app.get("/")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_send_lib(self):
        response = self.app.get("/lib/marked.js")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_send_spec(self):
        response = self.app.get("/specification/icecream.js")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_send_img(self):
        response = self.app.get("/images/logo_small.png")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_send_css(self):
        response = self.app.get("/css/style.css")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_send_fonts(self):
        response = self.app.get("/fonts/DroidSans.ttf")
        self.assertNotEqual(response.status_code, HTTP_404_NOT_FOUND)



######################################################################
# Utility functions
######################################################################

    def get_ice_creams_count(self):
        # save the current number of ice creams
        resp = self.app.get('/ice-cream')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        return len(data)

    def setup_data(self):
        new_ice_cream = {'name': 'Matcha', 'description':'Ice Cream made from finest Japanese Matcha green tea, milk and sweet cream','status':'frozen','base':'almond milk','price':'$4.99','popularity':'4.75/5','id':'500'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-cream', data=data, content_type='application/json')
        new_ice_cream = {'name': 'Peanut Butter n Jelly', 'description':'Ice Cream made from georgia peanut and strawberry jam, milk and sweet cream','status':'frozen','base':'coconut milk','price':'$4.99','popularity':'4.75/5','id':'501'}
        data = json.dumps(new_ice_cream)
        resp = self.app.post('/ice-cream', data=data, content_type='application/json')

    def delete_data(self):
        self.app.delete('/ice-cream/500', content_type='application/json')
        self.app.delete('/ice-cream/501', content_type='application/json')
        self.app.delete('/ice-cream/503', content_type='application/json')

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()

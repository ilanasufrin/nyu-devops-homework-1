from behave import *
import icecream
import json

@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.resp.data

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.resp.data

@given(u'the following icecream')
def step_impl(context):
    icecream.data_reset()
    flavors = {}
    for row in context.table:
        flavors[row['id']] = {'name': row['name'], 'id': row['id']}
    context.icecream.flavors = flavors

@when(u'I visit \'{url}\'')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@then(u'I should see \'{name}\'')
def step_impl(context, name):
    assert name in context.resp.data

@then(u'I should not see \'{name}\'')
def step_impl(context, name):
    assert name not in context.resp.data

@when(u'I create \'{url}\'')
def step_impl(context, url):
    flavor = {}
    for row in context.table:
        flavor = {'name': row['name'], 'description': row['description'], 'status': row['status'], 'base': row['base'], 'price': row['price'], 'popularity': row['popularity'],'id':row['id']}
        context.resp = context.app.post(url, data=json.dumps(flavor), content_type='application/json')
    print(context.resp)
    assert context.resp.status_code == 201

@when(u'I delete \'{url}\'')
def step_impl(context, url):
    context.resp = context.app.delete(url)
    assert context.resp.status_code == 204

@when(u'I update \'{url}\'')
def step_impl(context, url):
    flavor = {}
    for row in context.table:
        flavor = {'name': row['name'], 'description': row['description'], 'status': row['status'], 'base': row['base'], 'price': row['price'], 'popularity': row['popularity'],'id':row['id']}
        context.resp = context.app.put(url, data=json.dumps(flavor), content_type='application/json')
    assert context.resp.status_code == 200

#"base": "frozen yogurt",
#"description": "Yummy chocolate ice cream",
#"id": "6",
#"name": "Chocolate",
#"popularity": "4.8/5",
#"price": "$5.99",
#"status": "melted"



# @then(u'I should see a list of icecreams')
# def step_impl(context):
#     assert context.resp.status_code == 200
#     assert len(context.resp.data) > 0
@given('I want to query ice-cream by status')
def step_impl(context):
    context.resp = context.app.get('/ice-cream?status=frozen')
    assert context.resp.status_code == 200

@when(u'I give status as frozen')
def step_impl(context):
    context.resp = context.app.get('/ice-cream?status=frozen')

@then(u'I should get \'frozen\'')
def step_impl(context):
    context.resp = context.app.get('/ice-cream?status=frozen')
    assert 'frozen' in context.resp.data

@then(u'I should not get \'melted\'')
def step_impl(context):
    context.resp = context.app.get('/ice-cream?status=frozen')
    assert 'melted' not in context.resp.data




@given('I want to melt or freeze an icecream')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/melt')
    assert context.resp.status_code == 200
    context.resp = context.app.put('/ice-cream/4/freeze')
    assert context.resp.status_code == 200

@when('I append melt at the end of the url')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/melt')

@then(u'I should have \'melted\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/melt')
    assert 'melted' in context.resp.data

@then(u'I should have melted \'Vanilla\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/melt')
    assert 'Vanilla' in context.resp.data

@when(u'I append freeze at the end of the url')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/freeze')

@then(u'I should have \'frozen\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/freeze')
    assert 'frozen' in context.resp.data

@then(u'I should have frozen \'Vanilla\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/4/freeze')
    assert 'Vanilla' in context.resp.data

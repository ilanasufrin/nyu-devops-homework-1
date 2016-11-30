from behave import *
import icecream

@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.resp.data

@given(u'the following icecreams')
def step_impl(context):
    icecreams = {}
    for row in context.table:
        icecreams[row['name']] = {'name': row['name'], 'id': row['id']}
    context.icecream.icecreams = icecreams

@when(u'I visit \'{url}\'')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@then(u'I should see \'{name}\'')
def step_impl(context, name):
    assert name in context.resp.data

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.resp.data

# @then(u'I should see a list of icecreams')
# def step_impl(context):
#     assert context.resp.status_code == 200
#     assert len(context.resp.data) > 0

@given('I want to melt or freeze an icecream')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/melt')
    assert context.resp.status_code == 200
    context.resp = context.app.put('/ice-cream/0/freeze')
    assert context.resp.status_code == 200

@when('I append melt at the end of the url')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/melt')

@then(u'I should have \'melted\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/melt')
    assert 'melted' in context.resp.data

@then(u'I should have melted \'Vanilla\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/melt')
    assert 'Vanilla' in context.resp.data

@when(u'I append freeze at the end of the url')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/freeze')

@then(u'I should have \'frozen\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/freeze')
    assert 'frozen' in context.resp.data

@then(u'I should have frozen \'Vanilla\'')
def step_impl(context):
    context.resp = context.app.put('/ice-cream/0/freeze')
    assert 'Vanilla' in context.resp.data

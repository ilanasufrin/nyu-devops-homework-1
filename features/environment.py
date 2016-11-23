from behave import *
import icecream

def before_all(context):
    context.app = icecream.app.test_client()
    context.icecream = icecream

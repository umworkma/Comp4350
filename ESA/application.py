from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, json
from ESA import app
from flask.ext.testing import TestCase

@app.route('/_submit_form')
def submit_form():
    #get all user information
    username = request.args.get('username')
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    email = request.args.get('email')
    pwd1 = request.args.get('pwd1')
    phonenum = request.args.get('phonenum')
    address = request.args.get('address')
    #create a jason object and send it back to client 
    return jsonify(username=username, fname=fname, lname=lname, email=email, pwd1=pwd1, phonenum=phonenum, address=address)

import config
import models
import controllers

app.config.from_object(config)

db = models.init_app(app)
app.db = db

# helper method to check if request header contain json
# source http://flask.pocoo.org/snippets/45/
def is_request_json():
    if hasattr(request, 'accept_mimetypes'):
        best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
        return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
    else:
        return False

@app.route('/')
def home():
    return render_template('index.html')

# qunit - Javascript unit testing
@app.route('/_test')
def qunit_test():
    # List of html pages that use the Javascript function, as might needed for testing 
    pages = ['index.html', 'register_organization.html']
    return render_template('unit_test.html', qunit=True, testPage=pages)

@app.route('/register_organization/')
def register_organization():
    return render_template('register_organization.html')

@app.route('/_check_dup_org_name', methods=['GET', 'POST'])
def check_dup_org_name():
    if request.method == 'POST' and is_request_json():
        result = controllers.checkForDuplicateOrganizationName(request.json)
        return result

    else :
        return jsonify(msg='Assess define')

@app.route('/_submit_org_form', methods=['GET', 'POST'])
def submit_org_form():
    if request.method == 'POST' and is_request_json():
        result = controllers.registerOrganization(request.json,db)
        return result

    else:
        return jsonify(msg='Other request method[%s]' % request.method)

@app.route('/landing')
def landing():
    session.logged_in = True
    return render_template('landing.html')

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run()   

class InitTest(TestCase):

    def my_small_test(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

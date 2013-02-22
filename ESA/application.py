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

@app.route('/')
def home():
    return render_template('index.html')

# qunit - Javascript unit testing
@app.route('/_test')
def qunit_test():
    return render_template('unit_test.html')

@app.route('/register_organization.html/')
def register_organization():
    return render_template('register_organization.html')

@app.route('/_submit_org_form', methods=['GET', 'POST'])
def submit_org_form():
    if request.method == 'POST':
        result = controllers.registerOrganization(request.form.keys()[0],db)
        return result

    else:
        return jsonify(msg='Other request method[%s]' % request.method)


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

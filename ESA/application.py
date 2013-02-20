from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from ESA import app

import config
import models

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
        #get all user information
        orgname  = request.form['orgname']
        desc     = request.form['desc']
        pwd      = request.form['pwd']
        phone    = request.form['phone']
        address  = request.form['address']
        city     = request.form['city']
        province = request.form['province']
        postal   = request.form['postal']
        email    = request.form['email']

        #create a jason object and send it back to client 
        # return jsonify(request.form)
        return jsonify(orgname=orgname, desc=desc, pwd=pwd, phone=phone, address=address, city=city, province=province, postal=postal, email=email)

    else:
        return jsonify(msg='Other request method[%s]' % request.method)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run()

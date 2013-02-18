from flask import Flask, render_template, request, redirect, url_for, abort, session
from ESA import app

import config
import models

app.config.from_object(config)

db = models.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_organization.html/')
def register_organization():
    return render_template('register_organization.html')

@app.route('/_submit_org_form/')
def submit_org_form():
    #get all user information
    orgname = request.args.get('inputName')
    description = request.args.get('inputDescription')
    phone = request.args.get('inputPhone')
    address = request.args.get('inputAddress')
    city = request.args.get('inputCity')
    province = request.args.get('inputProvince')
    postal = request.args.get('inputPostal')
    email = request.args.get('inputEmail')
    #create a jason object and send it back to client 
    return jsonify(orgname=orgname, description=description, phone=phone, address=address, city=city, province=province, postal=postal, email=email)

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run()

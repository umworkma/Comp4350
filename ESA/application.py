from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, json
from ESA import app

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
        print request.form
        result = controllers.registerOrganization(request.form,db)
        return result

    else:
        return jsonify(msg='Other request method[%s]' % request.method)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, json, flash, Response
from ESA import app, login_manager, login_required, login_user, current_user, logout_user
from flask.ext.testing import TestCase

import config
import models
import controllers
import controller_privileges

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

# user loader callback
@login_manager.user_loader
def load_user(id):
    return controllers.getPersonById(int(id), db)


@app.route('/')
def home():
    # If its a user logged in display landing page
    if current_user.is_authenticated():
        return render_template('landing.html')

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        remember = False

        if request.form.has_key('username') and request.form.has_key('password'):
            username = request.form['username']
            user = controllers.getPersonByUsername(username, db)

            if user is not None:
                # See below comment
                # if request.form.has_key('rememberMe') and request.form['rememberMe'] == "True":
                #     remember = True 

                if user.password == request.form['password']:
                    # For some reason login-manager doesn't remember login user at the next request, 
                    # but it works at once remember set to True
                    # login_user(user, remember=remember)
                    login_user(user, remember=True) 

                    if request.values.has_key('next'):
                        return redirect(request.values['next'], code=302)

                    return redirect(url_for('home'))
                  
            flash("Please check user name and password.")

        else:
            flash("Please provide user name and password.")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# qunit - Javascript unit testing
@app.route('/_test', methods=['GET', 'POST', 'DELETE'])
def qunit_test():
    # List of html pages that use the Javascript function, as might needed for testing 
    pages = ['index.html', 'register_organization.html', 'privilege.html']

    if is_request_json():
        # if request.method == 'GET':
        print "I am here"
        return jsonify(request=request.method, success=True, msg='testing')
        # elif request.method == 'POST':

    return render_template('unit_test.html', qunit=True, testPage=pages)

@app.route('/register_organization/')
@login_required
def register_organization():
    return render_template('register_organization.html')


# No login required URL
@app.route('/signup')
def load_employee_reg_form():
    return render_template('employee_reg_form.html')


# No login required URL
@app.route('/_check_dup_employee_user_name', methods=['GET', 'POST'])
def check_dup_employee_user_name():
    if request.method == 'POST' and is_request_json():
        result = controllers.checkForDuplicateEmployeeUserName(request.json)
        return result
    else :
        return jsonify(msg='Asses define')
    	
	

@app.route('/_check_dup_org_name', methods=['GET', 'POST'])
@login_required
def check_dup_org_name():
    if request.method == 'POST' and is_request_json():
        result = controllers.checkForDuplicateOrganizationName(request.json)
        return result
    else :
        return jsonify(msg='Assess define')


@app.route('/_submit_org_form', methods=['GET', 'POST'])
@login_required
def submit_org_form():
    if request.method == 'POST' and is_request_json():
        result = controllers.registerOrganization(request.json,db)
        return result
    else:
        return jsonify(msg='Other request method[%s]' % request.method)

#No Login Required
@app.route('/organization')
def browse_orgs():
    data = controllers.getAllOrgNamesJSON(db)
    if request.method == 'GET' and is_request_json():
        return data
    else:
        return render_template('browse_orgs.html', data=json.loads(data))

#No Login Required
@app.route('/organization/<entityid>')
def org_info(entityid):
    data = controllers.getOrganizationByIDJSON(entityid)
    if data == None:
        data = entityid
        return render_template('org_404.html', data=data)
    if request.method == 'GET' and is_request_json():
        return data
    else:
        session.logged_in = True
        return render_template('org_info.html', org=json.loads(data))

# No login required URL
@app.route('/_submit_employee_form', methods=['GET', 'POST'])
def submit_employee_form():
    if request.method == 'POST' and is_request_json():
        result = controllers.registerEmployee(request.json,db)
        return result
    else:
        return jsonify(msg='Other request method[%s]' % request.method)


# privilege portal main handle function. If request is not support it will return error 403
@app.route('/privilege', methods=['GET', 'POST'])
@login_required
def privilege():
    try:
        user_id = current_user.entityFK

        if request.method == 'GET':
            org_json        = controller_privileges.getOrgsWithPrivilegesForPersonJSON(user_id)
            privilege_json  = controller_privileges.getAllPrivilegesJSON()

            if is_request_json():
                return jsonify(privilege_data=org_json + privilege_json)

            else:
                org_dict = json.loads(org_json)
                privilege_dict = json.loads(privilege_json)
                return render_template('privilege.html', orgs=org_dict, privileges=privilege_dict)
    except Exception, e:
        return abort(404)

    return abort(403)

# privilege portal get and post handle function. If request is not support it will return error 403
@app.route('/privilege/<org_id>', methods=['GET', 'POST'])
@login_required
def privilege_org(org_id):
    try:
        user_id = current_user.entityFK

        if request.method == 'GET':
            persons      = controllers.getPeopleInOrganizationJSON(org_id)
            persons_dict = json.loads(persons);
            org          = controllers.getOrganizationByIDJSON(org_id)
            org_dict     = json.loads(org);

            if is_request_json():
                return jsonify(persons_dict, Organization=org_dict)
                # return Response(response=persons, mimetype='application/json')
            
    except Exception, e:
        return abort(404)

    return abort(403)


# privilege portal get and post member privileges function. If request is not support it will return error 403
@app.route('/privilege/<org_id>/<person_id>', methods=['GET', 'POST'])
@login_required
def privilege_org_member(org_id, person_id):
    try:
        user_id = current_user.entityFK;

        if request.method == 'GET':
            privileges = controller_privileges.getPrivilegesForPersonJSON(person_id, org_id)

            if is_request_json():
                return Response(response=privileges, mimetype='application/json')

        elif request.method == 'POST':

            if is_request_json():
                result = controller_privileges.grantPrivilegeToPersonJSON(db, request.json['privilege_id'], person_id, org_id)
                return Response(response=result, mimetype='application/json')

    except Exception, e:
        return abort(404)

    return abort(403)

        
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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

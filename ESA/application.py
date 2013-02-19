from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
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


@app.route('/employee_reg_form.html')
def load_employee_reg_form():
    return render_template('employee_reg_form.html')
      


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()   

class InitTest(TestCase):

    def my_small_test(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
        

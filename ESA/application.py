from flask import Flask, render_template, request, redirect, url_for, abort, session
from ESA import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_organization.html/')
def home2():
    return render_template('register_organization.html')

if __name__ == '__main__':
    app.run()
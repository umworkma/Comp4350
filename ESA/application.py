from flask import Flask, render_template, request, redirect, url_for, abort, session
from ESA import app

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
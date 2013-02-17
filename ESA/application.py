from flask import Flask, render_template, request, redirect, url_for, abort, session
from database import db_session
from ESA import app

import config
import models

app.config.from_object(config)


@app.route('/')
def home():
    return render_template('index.html')

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()

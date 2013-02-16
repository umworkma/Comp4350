from flask import Flask, render_template, request, redirect, url_for, abort, session
from ESA import app

import config
import models

app.config.from_object(config)

db = models.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

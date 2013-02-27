from flask import Flask 
import os
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
import assets
# from flask.ext.login import LoginManager


env = os.environ.get('ESA')

# Allow to run manage.py without the uWSGI env variable
# There might be another way to set environ at manage.py, but 
# have no time to 
if env is None:
    env = "Dev"

app = Flask(__name__)
app.config.from_object('ESA.settings.%sConfig' % env.capitalize())

# webassets management
assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)

# login_manager = LoginManager()
# login_manager.setup_app(app)


import ESA.application
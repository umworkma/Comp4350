from flask import Flask 
import os
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
import assets
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user


env = os.environ.get('ESA')

# Allow to run manage.py without the uWSGI env variable
# There might be another way to set environ at manage.py, but 
# have no time to 
if env is None:
    env = "Dev"

app = Flask(__name__)
app.config.from_object('ESA.settings.%sConfig' % env.capitalize())

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.setup_app(app)
# login_message is not being pass into login_manager to flash out to login page
# login_manager.login_message = u"Please log in to access this page."

# webassets management
assets_env = Environment(app)
assets_loader = PythonAssetsLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)




import ESA.application
#!/var/local/Comp4350/venv/bin/python
from flask.ext.script import Manager, Shell, Server
from ESA import app, assets_env
import os
from flask_assets import ManageAssets

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.add_command("assets", ManageAssets(assets_env))
manager.run()
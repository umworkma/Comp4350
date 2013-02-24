#!./venv/bin/python
from flask.ext.script import Manager, Shell, Server, Command
from ESA import app, assets_env, models, fixtures
import os
from flask_assets import ManageAssets

class runlocal(Command):
    "Runs the server in a local, testing configuration"

    def run(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ESA/test.db'
        app.db = models.init_app(app)
        app.db.drop_all()
        models.create_tables(app)
        fixtures.install(app, *fixtures.all_data)
        app.run()
        app.db.session.remove()
        app.db.drop_all()

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("runlocal", runlocal())
manager.add_command("shell", Shell())
manager.add_command("assets", ManageAssets(assets_env))
manager.run()

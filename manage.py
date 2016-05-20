#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Advisor
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
#from . import models
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))


def make_shell_context():
    return dict(app=app, db=db, Advisor=Advisor, Client=Client)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver',Server(host="0.0.0.0", port=port))

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

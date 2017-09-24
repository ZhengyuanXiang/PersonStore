#!/usr/bin/env python
import os, sys
from app import create_app, db
from app.models import User
from flask_script import Manager, Shell, commands
from app.device_mng import socketio

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def test():
    pass

class MyServer(commands.Server):
    help = description = 'Runs the my socketio server i.e'

    def __call__(self, app, host, port, use_debugger, use_reloader,
               threaded, processes, passthrough_errors):
        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
                if sys.stderr.isatty():
                    print("Debugging is on. DANGER: Do not allow random users to connect to this server.")
        if use_reloader is None:
            use_reloader = app.debug
        socketio.run(app,host=host,
                port=port)

serv = MyServer()
manager.add_command("runserver", serv)

if __name__ == '__main__':
    manager.run()

from . import socketio
from flask_socketio import emit

@socketio.on('connect')
def handle_message():
    print('connect')

@socketio.on('login')
def my_event(data):
    print(data)
    from ..models import User
    user = User.query.filter_by(email=data['email']).first()
    if user is not None and user.verify_password(data['password']):
        print('%s login' % data['email'])
        emit("login", "OK")
        return
    emit("login", "NOT OK")
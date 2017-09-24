from . import socketio

@socketio.on('connect')
def handle_message():
    print('connect')

@socketio.on('my event')
def my_event():
    print('my event resv')
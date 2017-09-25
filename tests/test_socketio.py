from socketIO_client import SocketIO

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

def login_ret(data):
    print(data)

if __name__ == '__main__':
    socketIO = SocketIO('localhost', 5000)
    print('test_socketio')
    socketIO.on('login', login_ret)
    socketIO.emit('login', {'email':'xiangsocool@gmail.com', 'password':'123'})
    socketIO.wait()

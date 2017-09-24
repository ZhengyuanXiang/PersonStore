from socketIO_client import SocketIO

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

if __name__ == '__main__':
    socketIO = SocketIO('localhost', 5000)
    print('test_socketio')

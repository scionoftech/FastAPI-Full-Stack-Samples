import socketio
import time

"""
To instantiate an Socket.IO client, 
simply create an instance of the appropriate client class
"""
sio = socketio.Client(logger=True, engineio_logger=True)


class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print("I'm connected!")

    def on_connect_error(self):
        print("The connection failed!")

    def on_disconnect(self):
        print("I'm disconnected!")

    def on_my_event(self, data):
        self.emit('my_response', data)


sio.register_namespace(MyCustomNamespace('/api'))

# @sio.event(namespace="/api")
# def connect():
#     print("I'm connected!")
#
#
# @sio.event(namespace="/api")
# def connect_error():
#     print("The connection failed!")
#
#
# @sio.event(namespace="/api")
# def disconnect():
#     print("I'm disconnected!")


sio.connect('http://localhost:8088/ws')
# sio.wait()

if __name__ == "__main__":
    print('my sid is', sio.get_sid(namespace='/api'))
    time.sleep(5)
    sio.emit('test_event', {'foo': 'bar'}, namespace='/api')

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

"""
A Socket.IO server is an instance of class socketio.Server. 
This instance can be transformed into a standard WSGI application by wrapping 
it with the socketio.ASGIApp class:
"""
app = FastAPI()

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=["*"])
socket_app = socketio.ASGIApp(sio)
app.mount('/', socket_app)

# Middleware Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MyCustomNamespace(socketio.AsyncNamespace):

    def on_test_event(self, sid, data):
        print(sid, data)

    def on_connect(self, sid, environ):
        print("connected", sid)

    def on_disconnect(self, sid):
        print("disconnect", sid)


sio.register_namespace(MyCustomNamespace('/api'))

# @sio.on("test_event",namespace="/api")
# def test_event(sid, data):
#     print(sid, data)
#
#
# @sio.on("connect",namespace="/api")
# def connect(sid, environ):
#     print("connected", sid)
#
#
# @sio.on("disconnect",namespace="/api")
# def disconnect(sid):
#     print("disconnect", sid)

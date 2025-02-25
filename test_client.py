import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to Mezzo WebSocket!")

@sio.event
def disconnect():
    print("❌ Disconnected from Mezzo WebSocket!")

# Connect to the Flask-SocketIO server
sio.connect('http://127.0.0.1:5000', transports=['websocket'])
sio.wait()
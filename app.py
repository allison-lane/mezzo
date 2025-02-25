from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
import mediapipe as mp
import cv2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

@app.route('/')
def index():
    render_template('index.html')

def motion_detect():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('error: camera not initialized (permissions?)')
        return
    
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        avg_movement = np.mean(magnitude)

        if avg_movement < 3.0:
            motion_type = 'Small'
        elif avg_movement < 8.0:
            motion_type = 'Medium'
        else:
            motion_type = 'Large'

        socketio.emit('motion', {'intensity': float(avg_movement), 'type': motion_type})

        prev_gray = gray
        socketio.sleep(0.05)

@socketio.on('connect')
def start_motion_detection():
    print('connected & starting motion detection')
    socketio.start_background_task(motion_detect)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
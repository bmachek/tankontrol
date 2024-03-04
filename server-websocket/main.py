#!/usr/bin/env python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
from multiprocessing import Process, Queue
import config
import tank

tank.init_grovepi_board()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on_error_default
def default_error_handler(e):
    print("======================= ERROR")
    print(request.event["message"])
    print(request.event["args"])


@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]
    if "left" in data.keys():
        steering = float(data["left"]["x"])
        throttle = float(data["left"]["y"])

        # Reverse throttle value
        throttle *= -1

        if config._debug: print("[Tank] Movement: ",steering,",",throttle)

        throttle_l = 0.0
        throttle_r = 0.0


        if steering == 0:  # straight
            throttle_l = throttle
            throttle_r = throttle
        elif steering > 0: # right
            if throttle < 0:
                steering = -steering
            throttle_l = throttle
            throttle_r = (throttle) - (steering)
        elif steering < 0: # left
            if throttle < 0:
                steering = -steering
            throttle_l = (throttle) + (steering)
            throttle_r = (throttle)

        if config._debug:
            print("[Tank] Calculated throttle percentages, L: %f, R: %f" % (throttle_l, throttle_r))

        tank.move_tank(throttle_l, throttle_r)

    elif "right" in data.keys():
        x = float(data["right"]["x"])
        y = float(data["right"]["y"])
        if config._debug: print("[Tank] Turret: ",x,",",y)

        if x != 0:
            tank.move_turret(float(x))

@socketio.on('shoot', namespace='/control')
def shoot(message):
    if config._debug: print("Received fire order.")
    tank.shoot()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=config._debug, use_reloader=config._debug)

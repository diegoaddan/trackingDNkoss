from flask import Flask
from flask import url_for, render_template, Response, redirect, session, flash, send_file, request
from flask_socketio import SocketIO
import os, cv2, numpy as np

#Cria a aplicação
app = Flask(__name__)
app.secret_key = '65kXuwka'
socket_io = SocketIO(app)

count = 0

def detect_color(imageFrame, count):
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

	yellow_lower = np.array([20, 100, 100], np.uint8)
	yellow_upper = np.array([30, 255, 255], np.uint8)
	yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

	# Morphological Transform, Dilation
	# for each color and bitwise_and operator
	# between imageFrame and mask determines
	# to detect only that particular color
	kernal = np.ones((5, 5), "uint8")

	# For yellow color
	yellow_mask = cv2.dilate(yellow_mask, kernal)
	res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
	mask = yellow_mask)

	# Creating contour to track yellow color
	contours, hierarchy = cv2.findContours(yellow_mask,
	cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 700):
			count += 1
			return count
	return count

@app.route('/')
@app.route('/index')
def index():
	global count
	count = 0
	return render_template('index.html', titulo_pagina="Prova de conceito", contador=count)

@app.route("/upload",methods= ['POST'])
def upload():
	global count
	snapshot = request.files['webcam']
	snapthotnp = np.fromfile(snapshot, np.uint8)
	snapshot = cv2.imdecode(snapthotnp, cv2.IMREAD_COLOR)
	count = detect_color(snapshot, count)
	socket_io.emit('valor-amarelo', count)
	print(count)
	return str(count)

if __name__=='__main__':
    socket_io.run(app, host='0.0.0.0', debug=True)

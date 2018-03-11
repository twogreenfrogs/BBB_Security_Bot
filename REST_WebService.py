#!/usr/bin/python
#This flask based RESTful Web Service is thanks to below blog
#http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

from flask import Flask, render_template, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
import serial, os, random, time

#todo: use sql for saving data
#import sqlite3 

#todo: enable auth for restful APIs
#auth = HTTPBasicAuth() 
app = Flask(__name__)     

'''
@auth.get_password
def get_password(username):
    if username == 'beaglebone':
        return 'cisco123'
    return None

def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)
'''

#todo: robot functions: replace this with database
status = [
    {
        'desc': u'wifi',
        'status': u'on',
    },
    {
        'desc': u'umts',
        'status': u'on',
    },
    {
        'desc': u'webcam',
        'status': u'off',
    },
    {
        'desc': u'ipcam',
        'status': u'off',
    },
    {
        'desc': u'robot',
        'status': u'off',
    },
    {
        'desc': u'move',
        'status': u'stop',
    },
    {
        'desc': u'armed',
        'status': u'off',
    },
    {
        'desc': u'lamp',
        'status': u'off',
    },
]

@app.route('/', methods = ['GET', 'POST'])
def home():
  wifi = None
  umts = None
  webcam = None
  ipcam = None
  robot = None
  move = None
  lamp = None

  if request.method == 'GET':
        return render_template('index.html', wifi=status[0]['status'], umts=status[1]['status'], \
        webcam=status[2]['status'], ipcam=status[3]['status'], robot=status[4]['status'], \
        move=status[5]['status'], armed=status[6]['status'], lamp=status[7]['status']\
        )

  if request.method == 'POST':
    	print "content_type: ", request.content_type
    	print "request.form[desc]: ", request.form['desc']
    	print "request.form[status]: ", request.form['status']
	item=request.form['desc']
	on_off_status=request.form['status']
	print item, on_off_status

  	return render_template('index.html', wifi=status[0]['status'], umts=status[1]['status'], \
	webcam=status[2]['status'], ipcam=status[3]['status'], robot=status[4]['status'], \
        move=status[5]['status'], armed=status[6]['status'] \
	)

'''
# experiment to display LDR values on Webpage in realtime
port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
@app.route('/LDR.html')
def ldr_display():
	port.flushInput()
	newdata=port.readline().strip('\r\n')
	print newdata
	return render_template('LDR.html', data=newdata)
'''

# RESTFUI APIs implementation
@app.route('/robot/api', methods = ['GET'])
def get_status():
  return jsonify({'status':status}) 

@app.route('/robot/api/<item>', methods = ['GET'])
def get_item(item):
  #filter(lambda ftn, list to filter)
  item = filter(lambda t: t['desc'] == item, status)
  if len(item) == 0:
      abort(404)
  return jsonify( { 'status': item[0] } )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/robot/api', methods = ['POST'])
def create_item():
    if not request.json or not 'desc' in request.json or not 'status' in request.json:
        abort(400)
    item = {
        'desc': request.json['desc'],
        'status': request.json['status'],
    }
    status.append(item)
    return jsonify( { 'status': status } ), 201

@app.route('/robot/api/<item>', methods = ['DELETE'])
def del_item(item):
    item = filter(lambda t: t['desc'] == item, status)
    if len(item) == 0:
        abort(404)
    status.remove(item[0])
    return jsonify( { 'status': status } )

@app.route('/robot/api/<item>', methods = ['PUT'])
def update_item(item):
    item = filter(lambda t: t['desc'] == item, status)
    if len(item) == 0:
        abort(404)
    
    print "content_type: ", request.content_type
    print "request.json: ", request.json

    if not request.get_json:
	print "bad json format"
        abort(400)
    if 'desc' in request.json and type(request.json['desc']) != unicode:
        abort(400)
    if 'status' in request.json and type(request.json['status']) is not unicode:
        abort(400)

    item[0]['desc'] = request.json.get('desc', item[0]['desc'])
    item[0]['status'] = request.json.get('status', item[0]['status'])
    return jsonify( { 'status': item[0] } )

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=80)
   

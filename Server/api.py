# -*- coding: UTF-8 -*-

from flask import Flask, json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
	
@app.route("/get_route", methods=['GET'])
def get_route_json():
	return "WELL Done!"
	
@app.route("/index")
def index():
	return  "This is a test page !"

if __name__ == '__main__':
    app.run(host='localhost', port=3080, debug=True, threaded=True)
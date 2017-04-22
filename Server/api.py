# -*- coding: UTF-8 -*-

from flask import Flask, json
from config import DevConfig
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return "<H1>Hello World!<H1>"
	
@app.route("/get_route", methods=['GET'])
def get_route_json():
	return "WELL Done!"
	
@app.route("/index")
def index():
	return  "This is a test page !"

class User(db.Model):
	__tablename__ = 'user_table_name' 
	id = db.Column(db.Integer(),primary_key=True)
	username = db.Column(db.String(255))
	password = db.Column(db.String(255))
	birth = db.Column(db.Date())
	
	def __init__(self,username):
		self.username = username
	
	def __repr__(self):
		return "<User '{}'>".format(self.username)
	
if __name__ == '__main__':
    #app.run(host='localhost', port=3080, debug=True, threaded=True)
	app.run()
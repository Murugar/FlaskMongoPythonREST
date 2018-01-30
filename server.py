from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'

mongo = PyMongo(app)

@app.route('/room', methods=['GET'])
def get_all_rooms():
	rooms = mongo.db.rooms
	
	output = []
	
	for q in rooms.find():
		output.append({'name' : q['name'], 'address' : q['address']})
		
	return jsonify({'result' : output})
	
@app.route('/room/<name>', methods=['GET'])
def get_one_room(name):
	rooms = mongo.db.rooms
	
	q = rooms.find_one({'name' : name})
	output = {'name' : q['name'], 'address' : q['address']}
	
	return jsonify({'result' : output})
	
@app.route('/room', methods=['POST'])
def add_room():
	rooms = mongo.db.rooms
	
	name = request.json['name']
	address = request.json['address']
	
	room_id = rooms.insert({'name' : name, 'address' : address})
	new_room = rooms.find_one({'_id' : room_id})
	
	output = {'name' : new_room['name'], 'address' : new_room['address']}
	
	return jsonify({'result' : output})

if __name__ == '__main__':
	app.run(debug=True)
	

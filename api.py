from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid
import os

app = Flask(__name__)

# You'll need to set the environment variable below in .profile, .zshrc, or .login
app.config['SECRET_KEY'] = os.environ['FLASK_DB_NO_AUTH']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///names.db'

db = SQLAlchemy(app)

class Name(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))

@app.route('/name', methods=['GET'])
def get_all_names():
	names = Name.query.all()
	output = [{'name': name.name, "public_id": name.public_id} for name in names]

	return jsonify({'names': output})

@app.route('/name/<name>', methods=['GET'])
def get_one_name(name):
	db_name = Name.query.filter_by(name=name).first()
	if not db_name:
		return jsonify({'message': 'That name couldn\'t be found.'})

	return jsonify({'name': db_name.name, 'public_id': db_name.public_id})

@app.route('/name', methods=['POST'])
def add_name():

	data = request.get_json() #How will I do this outside of postman?
	#At the very least, I can make GET requests from another flask app.

	new_name = Name(public_id=str(uuid.uuid4()), name=data['name'])
	db.session.add(new_name)
	db.session.commit()

	return jsonify({'message': "New name created"})

@app.route('/name/<name>', methods=['PUT'])
def change_name(name):

	data = request.get_json() #This is returning a NoneType object
	#When I put from the other flask app.

	db_name = Name.query.filter_by(name=name).first()
	if not db_name:
		return jsonify({'message': "That name couldn't be found."})

	db_name.name = data['name']
	db.session.commit()

	return jsonify({'message': f"{name} has been changed to {data['name']}"})

@app.route('/name/<name>', methods=['DELETE'])
def delete_name(name):

	db_name = Name.query.filter_by(name=name).first()
	if not db_name:
		return jsonify({'message': "That name couldn't be found."})

	db.session.delete(db_name)
	db.session.commit()

	return jsonify({'message': f'{name} was deleted.'})

if __name__ == '__main__':
	app.run(debug=True, port=5002)
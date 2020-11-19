from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'x83mvasdei2349vja33m' #bonus - put this in environ variables
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

	return jsonify({'message': 'New name created.'})

@app.route('/name/<name>', methods=['PUT'])
def change_name(name):

	data = request.get_json()

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
# app/api.py
from app import app
from app.models import User, Post, Logbooktable
from flask import jsonify

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)

@app.route('/api/users', methods=['GET'])
def get_users():
    data = User.to_collection()
    return jsonify(data)

@app.route('/api/logbook/<int:id>', methods=['GET'])
def get_logbookentry(id):
    data = Logbooktable.query.get_or_404(id).to_dict()
    return jsonify(data)
    
@app.route('/api/logbook', methods=['GET'])
def get_logbookall():
    data = Logbooktable.to_collection()
    return jsonify(data)
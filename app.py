from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("localhost", 27017)
db = client.todo_db  # Database
todos_collection = db.todos  # Collection for todos

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Todo API!"})

@app.route('/todos', methods=['GET'])
def get_all_todos():
    todos = []
    for todo in todos_collection.find():
        todos.append({
            'id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description'],
            'status': todo['status'],
            'created_at': todo['created_at'],
            'updated_at': todo['updated_at']
        })
    return jsonify(todos), 200

@app.route('/todos/<id>', methods=['GET'])
def get_todo(id):
    todo = todos_collection.find_one({'_id': ObjectId(id)})
    if todo:
        return jsonify({
            'id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description'],
            'status': todo['status'],
            'created_at': todo['created_at'],
            'updated_at': todo['updated_at']
        }), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data.get('title') or not data.get('description'):
        return jsonify({"error": "Title and description are required"}), 400
    
    new_todo = {
        'title': data['title'],
        'description': data['description'],
        'status': 'pending',  # Default status
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    result = todos_collection.insert_one(new_todo)
    return jsonify({"message": "Todo created", "id": str(result.inserted_id)}), 201

@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    updated_todo = {
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'status': data.get('status', 'pending'),
        'updated_at': datetime.utcnow()
    }
    result = todos_collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': updated_todo}
    )
    if result.matched_count:
        return jsonify({"message": "Todo updated"}), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    result = todos_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Todo deleted"}), 200
    else:
        return jsonify({"error": "Todo not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)

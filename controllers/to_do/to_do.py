from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource
from bson.objectid import ObjectId
from database import todos_collection


class AllTodo(Resource):
    def get(self):
        todos = []
        for todo in todos_collection.find():
            todos.append({
                'id': str(todo['_id']),
                'title': todo['title'],
                'description': todo['description'],
                'status': todo['status'],
                'created_at': todo['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['created_at'], datetime) else todo['created_at'],
                'updated_at': todo['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['updated_at'], datetime) else todo['updated_at']
            })
        return todos, 200

class TODO(Resource):

    def get(self, id):
        todo = todos_collection.find_one({'_id': ObjectId(id)})
        print(id)
        if todo:
            return ({
                'id': str(todo['_id']),
                'title': todo['title'],
                'description': todo['description'],
                'status': todo['status'],
                'created_at': todo['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['created_at'], datetime) else todo['created_at'],
                'updated_at': todo['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['updated_at'], datetime) else todo['updated_at']
            }), 200
        else:
            return ({"error": "Todo not found"}), 404

    def post():
        data = request.get_json()
        if not data.get('title') or not data.get('description'):
            return ({"error": "Title and description are required"}), 400
        
        new_todo = {
            'title': data['title'],
            'description': data['description'],
            'status': 'pending',  # Default status
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = todos_collection.insert_one(new_todo)
        return ({"message": "Todo created", "id": str(result.inserted_id)}), 201

    def put(self, id):
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
            return ({"message": "Todo updated"}), 200
        else:
            return ({"error": "Todo not found"}), 404

    def delete(self, id):
        result = todos_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return ({"message": "Todo deleted"}), 200
        else:
            return ({"error": "Todo not found"}), 404
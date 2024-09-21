from datetime import datetime
from flask import request
from flask_restful import Resource
from bson.objectid import ObjectId
from database import todos_collection


class AllTodo(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        # Calculate the skip value based on page and limit
        skip = (page - 1) * limit
        todos = []
        for todo in todos_collection.find().skip(skip).limit(limit):
            todos.append({
                'id': str(todo['_id']),
                'title': todo['title'],
                'description': todo['description'],
                'status': todo['status'],
                'created_at': todo['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['created_at'], datetime) else todo['created_at'],
                'updated_at': todo['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['updated_at'], datetime) else todo['updated_at']
            })
        total_todos = todos_collection.count_documents({})
        total_pages = (total_todos + limit - 1) // limit  # To get the total number of pages

        return {
            'todos': todos,
            'page': page,
            'total_pages': total_pages,
            'total_todos': total_todos
        }, 200

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
        error_message, is_valid = validate_todo_data(data)
        if not is_valid:
            return {"error": error_message}, 400
            
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
        error_message, is_valid = validate_todo_data(data)
        if not is_valid:
            return {"error": error_message}, 400
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
        

def validate_todo_data(data):
        VALID_STATUSES = ['pending', 'in_progress', 'completed']
        if not data.get('title'):
            return "Title is required", False
        if not data.get('description'):
            return "Description is required", False
        if data.get('status') and data['status'] not in VALID_STATUSES:
            return f"Status must be one of {VALID_STATUSES}", False
        return None, True
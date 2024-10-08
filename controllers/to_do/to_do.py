from datetime import datetime
import traceback
from flask import request
from flask_restful import Resource
from bson.objectid import ObjectId
from controllers.to_do.token import require_api_key
from database import todos_collection
from bson.errors import InvalidId
from database import limiter

class AllTodo(Resource):
    @limiter.limit("10 per minute")  # Rate limit for this specific route
    # @require_api_key

    def get(self):
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            status_filter = request.args.get('status')
            title_filter = request.args.get('title')
            sort_by = request.args.get('sort_by', 'created_at')  # Default sort by created_at
            sort_order = request.args.get('sort_order', 'asc')  # Default sort order ascending

            # Calculate the skip value based on page and limit
            skip = (page - 1) * limit

            query = {}
            if status_filter and status_filter in VALID_STATUSES:
                query['status'] = status_filter
            if title_filter:
                query['title'] = {'$regex': title_filter, '$options': 'i'}  # Case-insensitive match

            # Determine sort order
            sort_direction = 1 if sort_order == 'asc' else -1  # 1 for ascending, -1 for descending
            
            todos = []
            for todo in todos_collection.find(query).sort(sort_by, sort_direction).skip(skip).limit(limit):
                todos.append({
                    'id': str(todo['_id']),
                    'title': todo['title'],
                    'description': todo['description'],
                    'status': todo['status'],
                    'created_at': todo['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['created_at'], datetime) else todo['created_at'],
                    'updated_at': todo['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(todo['updated_at'], datetime) else todo['updated_at']
                })
            total_todos = todos_collection.count_documents(query)
            total_pages = (total_todos + limit - 1) // limit  # To get the total number of pages

            return {
            'todos': todos,
            'page': page,
            'total_pages': total_pages,
            'total_todos': total_todos
        }, 200

        except ValueError:
            # Handle invalid integer conversions for page and limit
            return {'error': 'Invalid page or limit parameter'}, 400

        except Exception as e:
            # Handle any other exceptions, returning traceback details
            return {
                'error': 'An error occurred',
                'details': str(e),
                'traceback': traceback.format_exc()  # Add traceback details to the response
            }, 500

class TODO(Resource):
    # @require_api_key
    def get(self, id):
        try:
            todo = todos_collection.find_one({'_id': ObjectId(id)})
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
        except InvalidId:
            return {"error": "Invalid ID format"}, 400
        
    def post(self):
        try: 
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
        except KeyError as e:
        # Handle missing required fields
            return {
                "error": f"Missing required field: {str(e)}",
                "traceback": traceback.format_exc()
            }, 400
        
    @require_api_key
    def put(self, id):
        try:
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
        except KeyError as e:
        # Handle missing required fields
            return {
                "error": f"Missing required field: {str(e)}",
                "traceback": traceback.format_exc()
            }, 400

    @require_api_key
    def delete(self, id):
        try:
            result = todos_collection.delete_one({'_id': ObjectId(id)})
            if result.deleted_count:
                return ({"message": "Todo deleted"}), 200
            else:
                return ({"error": "Todo not found"}), 404
        except KeyError as e:
        # Handle missing required fields
            return {
                "error": f"Missing required field: {str(e)}",
                "traceback": traceback.format_exc()
            }, 400

VALID_STATUSES = ['pending', 'in_progress', 'completed']

def validate_todo_data(data):
        if not data.get('title'):
            return "Title is required", False
        if not data.get('description'):
            return "Description is required", False
        if data.get('status') and data['status'] not in VALID_STATUSES:
            return f"Status must be one of {VALID_STATUSES}", False
        return None, True



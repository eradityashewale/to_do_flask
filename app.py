from flask import Flask, jsonify, request
from pymongo import MongoClient

from datetime import datetime
from flask_restful import Api

from controllers.to_do.to_do import *


app = Flask(__name__)

# # MongoDB connection
# client = MongoClient("localhost", 27017)
# db = client.todo_db  # Database
# todos_collection = db.todos  # Collection for todos

api = Api(app)

# Setting the endpoints for plant
api.add_resource(AllTodo, "/todos")
api.add_resource(TODO, "/todo/<id>", "/todo", )


if __name__ == '__main__':
    app.run(debug=True)

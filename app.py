from flask import Flask
from flask_limiter import Limiter
from flask_restful import Api
from flask_limiter.util import get_remote_address
from database import limiter
from controllers.to_do.to_do import *


app = Flask(__name__)

api = Api(app)

limiter.init_app(app)
# Setting the endpoints for plant
api.add_resource(AllTodo, "/todos")
api.add_resource(TODO, "/todo/<id>", "/todo", )


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_restful import Api
from database import limiter
from controllers.to_do.to_do import *
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

CORS(app)

api = Api(app)

limiter.init_app(app)

SWAGGER_URL = '/swagger-ui'
API_URL = '/static/swagger.json'  # Path to your Swagger JSON file

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={
    'app_name': "Flask Todo API"
})

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Setting the endpoints for todo
api.add_resource(AllTodo, "/todos")
api.add_resource(TODO, "/todo/<id>", "/todo", )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


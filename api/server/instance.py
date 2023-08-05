import os

from flask import Flask, Blueprint
from flask_restx import Api

class Server():
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.blueprint, doc='/doc', title='Taskou API')
        self.app.register_blueprint(self.blueprint)
        self.taskou_ns = self.taskou_ns()
        self.server_config()
        
    def taskou_ns(self,):
        return self.api.namespace(name='Taskou', description='Taskou related operations', path='/')

    def server_config(self,):
        self.app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 't4sk0uKey')

    def run(self,):
        self.app.run(
            debug=True,
            port=7001,
            host="0.0.0.0"
        )

server = Server()

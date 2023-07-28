from flask import jsonify

from api.server.instance import server
from api.controller.task_controller import *

api = server.api
app = server.app

if __name__ == '__main__':
    server.run()
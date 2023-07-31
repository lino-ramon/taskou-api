from flask import jsonify
import logging

from api.server.instance import server
from api.controller.task_controller import *

api = server.api
app = server.app

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)-6s - %(message)s',
        encoding='utf-8',
        handlers=[
            logging.FileHandler("logs/taskou_api.log", mode="w"),
            logging.StreamHandler()
        ]
    )
    server.run()
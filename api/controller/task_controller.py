import json
import logging
import os
import uuid
import time

from bson import json_util
from flask import jsonify, request
from flask_restx import Resource
from datetime import datetime

from api.model.errors import TaskNotFoundError, KeyError, SaveUserError
from api.model.generic_mongodb import GenericMongoDB
from api.model.ns_models import task_model
from api.model.task import Task
from api.server.instance import server

from api.service.create_user_service import CreateUserService

HTTP_SUCCESS_CODE = 200
HTTP_CODE_ERROR = 404

app = server.app
api = server.api
taskou_ns = server.taskou_ns

app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 't4sk0uKey')

@app.before_request
def request_init():
    request.request_id = str(uuid.uuid4())
    request.start_time = time.time()

@api.route('/tasks')
class Tasks(Resource):
    def get(self):
        collection = GenericMongoDB().get_collection('tasks')
        response = {}
        payload = request.get_json()
        try:
            if 'id' not in payload:
                raise KeyError("Field 'id' is required!")

            task_id = payload['id']

            if not task_id:
                raise ValueError("ID cannot be empty!")

            task = collection.find_one({'id': task_id}, {'_id': 0})

            if not task:
                raise TaskNotFoundError("Task not found!")

            response = {
                "task": task,
                "message": "success"
            }
        except (ValueError, KeyError) as e:
            response = {
                "error": str(e),
                "message": "Invalid Payload."
            }
        except TaskNotFoundError as e:
            response = {
                "error": str(e),
                "message": "Task not found in database."
            }
        
        return jsonify(response)

    @taskou_ns.expect(task_model, validate=True)
    @taskou_ns.doc('Create a task model.')
    def post(self):
        collection = GenericMongoDB().get_collection('tasks')
        task_data = request.get_json()
        task = Task(task_data)
        task.save()
        response = {'message': 'Task insert successfull!!!'}
        return jsonify(response)

@api.route('/users')
class Users(Resource):
    def get(self):
        request_exec_id = request.request_id
        create_user_service = CreateUserService()
        response = create_user_service.create_user(request_exec_id)
        return jsonify(response)

@app.after_request
def request_end(response):
    request_exec_info = {
        'request_id': request.request_id,
        'endpoint': request.endpoint,
        'http_method': request.method,
        'start_data': request.headers.get('Date'),
        'end_data': datetime.now(),
        'runtime': time.time() - request.start_time
    }
    logging.info('[%s] Saving Request Exec Info: [%s]', request.request_id, request_exec_info)
    collection = GenericMongoDB().get_collection('request_exec_history')
    collection.insert_one(request_exec_info)

    return response
    
import json
import logging
import os
import uuid
import time

from bson import json_util
from flask import jsonify, request, g as gvar
from flask_restx import Resource
from datetime import datetime

from api.model.errors import TaskNotFoundError, KeyError, SaveUserError
from api.model.generic_mongodb import GenericMongoDB
from api.model.ns_models import task_model, user_model
from api.model.task import Task
from api.model.request_history import RequestHistory
from api.server.instance import server

from api.service.user_service import UserService

app = server.app
api = server.api
taskou_ns = server.taskou_ns

app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 't4sk0uKey')

@app.before_request
def request_init():
    request.request_id = str(uuid.uuid4())
    request.start_time = time.time()
    gvar.start_data = datetime.now()

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
        request_id = request.request_id
        user_service = UserService()
        response = user_service.generate_user(request_id)
        gvar.user_id = response.get('user_id', '')
        
        return jsonify(response)

    @taskou_ns.expect(user_model, validate=True)
    @taskou_ns.doc('Delete user payload model.')
    def delete(self):
        request_id = request.request_id
        try:
            payload = request.get_json()
            
            if 'user_id' not in payload:
                raise KeyError("Field 'user_id' is required!")

            user_id = payload['user_id']

            if not user_id:
                raise ValueError("ID cannot be empty!")
            
            user_service = UserService()
            response = user_service.delete_user(request_id, user_id)
            
        except (ValueError, KeyError) as e:
            response = {
                "error": str(e),
                "message": "Invalid Payload."
            }
        
        gvar.user_id = user_id if response.get('erro', '') == 'success' else ''
        return jsonify(response)

@app.after_request
def request_end(response):
    request_history = RequestHistory()
    request_history.save()
    return response
    
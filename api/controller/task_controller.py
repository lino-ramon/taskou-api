import json
import logging
import os
import uuid

from bson import json_util
from flask import jsonify, request
from flask_restx import Resource

from api.model.errors import TaskNotFoundError, KeyError, SaveUserError
from api.model.generic_mongodb import GenericMongoDB
from api.model.ns_models import task_model
from api.model.task import Task
from api.model.user import User
from api.server.instance import server

from api.service.create_user_service import CreateUserService

HTTP_SUCCESS_CODE = 200
HTTP_CODE_ERROR = 404

app = server.app
api = server.api
taskou_ns = server.taskou_ns

app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 't4sk0uKey')

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
        create_user_service = CreateUserService()
        response = create_user_service.get_response()
        return jsonify(response)
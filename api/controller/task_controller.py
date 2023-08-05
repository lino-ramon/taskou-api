import json
import logging
import os
import time
import uuid
from datetime import datetime, timedelta

import jwt
from api.model.errors import KeyError, SaveUserError, TaskNotFoundError, ValidationUserError, ActivationUserError
from api.model.generic_mongodb import GenericMongoDB
from api.model.ns_models import task_model, user_model
from api.model.request_history import RequestHistory
from api.model.task import Task
from api.server.instance import server
from api.service.user_service import UserService
from bson import json_util
from flask import g as gvar
from flask import jsonify, request
from flask_restx import Resource

app = server.app
api = server.api
taskou_ns = server.taskou_ns

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

            user_id = payload['user_id']

            if not user_id:
                raise ValueError("'user_id' cannot be empty!")
            
            user_service = UserService()
            response = user_service.delete_user(request_id, user_id)
            
        except (ValueError, KeyError) as e:
            response = {
                "error": str(e),
                "message": "Invalid Payload."
            }
        
        gvar.user_id = user_id if response.get('erro', '') == 'success' else ''
        return jsonify(response)

@api.route('/token')
class Token(Resource):
    @taskou_ns.expect(user_model, validate=True)
    @taskou_ns.doc('Get token payload model.')
    def get(self):
        request_id = request.request_id
        response   = {}
        try:
            payload = request.get_json()
            user_id = payload['user_id']
            gvar.user_id = user_id
            user_service = UserService()
            if not user_id:
                raise ValueError("'user_id' cannot be empty!")

            valid_user, message = user_service.validate_user(request_id, user_id)

            if not valid_user:
                raise ValidationUserError(message)

            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(minutes=2)
            }
            secret_key = app.config['SECRET_KEY']
            token = jwt.encode(payload, secret_key)
            
            activated_user = user_service.activated_user(request_id, user_id)
            if not activated_user:
                activated_user = user_service.activate_user(request_id, user_id)
            
            if not activated_user:
                raise ActivationUserError('Error at actavation user')

            response = {'token': token}

        except ValueError as e:
            response = {
                "error": str(e),
                "message": "Invalid Payload."
            }  
        except ValidationUserError as e:
            response = {
                "error": str(e),
                "message": "Validation User Failed!"
            }
        except ActivationUserError as e:
            response = {
                "error": str(e),
                "message": "Actavation User Failed!"
            }

        return jsonify(response)

@app.after_request
def request_end(response):
    request_history = RequestHistory()
    request_history.save()
    return response    

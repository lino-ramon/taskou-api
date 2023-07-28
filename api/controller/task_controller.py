from flask import request, jsonify
from flask_restx import Resource, fields
from ..model.generic_mongodb import GenericMongoDB
from ..model.task import Task
from ..server.instance import server
from bson import json_util
import json

HTTP_SUCCESS_CODE = 200
HTTP_CODE_ERROR = 404

app = server.app
api = server.api
taskou_ns = server.taskou_ns

@api.route('/tasks')
class Tasks(Resource):
    def get(self):
        collection = GenericMongoDB().get_collection('tasks')
        payload = request.get_json()
        task = {}
        msg = ""
        if 'id' not in payload:
            msg = 'Payload invalid. Field \"id\" is required!'

        id = payload.get("id")
        if not id:
            msg = 'Invalid Id: Empty!'

        task = json.loads(json_util.dumps(collection.find({'id': id}, {'_id': 0})))
        if not task:
            msg = 'Task not found!'

        response = {
                'message': msg,
                'task': task
            }
        return jsonify(response)

    def post(self):
        collection = GenericMongoDB().get_collection('tasks')
        task_data = request.get_json()
        task = Task(task_data)
        task = task.get_json()
        collection.insert_one(task)
        response = {'message': 'Task insert successfull!!!'}
        return jsonify(response)


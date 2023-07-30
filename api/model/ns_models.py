from flask_restx import fields
from ..server.instance import server

taskou_ns = server.taskou_ns

task_model = taskou_ns.model('Task', {
                'name': fields.String(required=True),
                'status': fields.String(),
                'start_data': fields.String(),
                'end_data': fields.String(),
                'description': fields.String(),
                'annotations': fields.List(fields.String())
            })
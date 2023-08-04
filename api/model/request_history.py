import logging
import time
from datetime import datetime

from flask import g as gvar
from flask import request

from .generic_mongodb import GenericMongoDB


class RequestHistory(object):
    request_id: str
    endpoint: str
    http_method: str
    start_data: datetime
    end_data: datetime
    runtime: time
    user_id: str
    task_id: str

    def __init__(self) -> None:
        self.request_id = request.request_id
        self.endpoint = str(request.endpoint).replace('.', '/')
        self.http_method = request.method
        self.start_data = getattr(gvar, 'start_data', '')
        self.end_data = datetime.now()
        self.runtime = time.time() - request.start_time
        self.user_id = getattr(gvar, 'user_id', '')
        self.task_id = getattr(gvar, 'task_id', '')

    def save(self) -> bool:
        try:
            request_history_collection = GenericMongoDB().get_collection('request_history')
            request_json = self.get_json()
            logging.info("[%s] Saving a Request History - Fields: [%s]", self.request_id, request_json)
            request_history_collection.insert_one(request_json)
        except Exception as erro:
            logging.exception("[%s] Error to insert at mongo. Erro: [%s]", self.user_id, erro)
            return False

        return True

    def get_json(self) -> dict:
        return {
            'request_id': self.request_id,
            'endpoint': self.endpoint,
            'http_method': self.http_method,
            'start_data': self.start_data,
            'end_data': self.end_data,
            'runtime': self.runtime,
            'user_id': self.user_id,
            'task_id': self.task_id
        }

import logging
from api.model.generic_mongodb import GenericMongoDB
from datetime import datetime
class Task(object):
    user_id: str
    task_id: str
    operation: str
    start_data: datetime

    def __init__(self, user_id, task_id, operation) -> None:
        self.user_id = user_id,
        self.task_id = task_id,
        self.operation = operation
        self.start_data = datetime.now()
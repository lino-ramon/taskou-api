import logging
from .generic_mongodb import GenericMongoDB

class Task(object):
    id: str
    name: str
    status: str
    start_data: str
    end_data: str
    description: str
    annotations: list

    def __init__(self, task_data: dict) -> None:
        self.id = task_data.get('id', '')
        self.name = task_data.get('name', '')
        self.status = task_data.get('status', '')
        self.start_data = task_data.get('start_data', '')
        self.end_data = task_data.get('end_data', '')
        self.description = task_data.get('description', '')
        self.annotations = task_data.get('annotations', [])

    def save(self, user_id) -> bool:
        try:
            task_collection = GenericMongoDB().get_collection('tasks')
            task_json = self.get_json()
            logging.info("[%s] Saving a task - Fields: [%s]", self.user_id, task_json)
            task_collection.insert_one(task_json)
        except Exception as erro:
            logging.exception("[%s] Error to insert at mongo. Erro: [%s]", self.user_id, erro)
            return False

        return True
    def get_json(self) -> dict:
        return {
                'id': self.id,
                'name': self.name,
                'status': self.status,
                'start_data': self.start_data,
                'end_data': self.end_data,
                'description': self.description,
                'annotations': self.annotations
            }
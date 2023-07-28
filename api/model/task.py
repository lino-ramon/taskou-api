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

    def save(self) -> bool:
        try:
            task_collection = GenericMongoDB().get_collection('tasks')
            task_json = self.get_json()
            task_collection.insert_one(task_json)
        except Exception as erro:
            print("Erro ao inserir no mongo. Erro: [%s]", erro)
            return False

        return True
    def get_json(self) -> dict:
        task_json = {
                'id': self.id,
                'name': self.name,
                'status': self.status,
                'start_data': self.start_data,
                'end_data': self.end_data,
                'description': self.description,
                'annotations': self.annotations
            }
        return task_json
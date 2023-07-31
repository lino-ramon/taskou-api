import logging
from .generic_mongodb import GenericMongoDB
from datetime import datetime

class User(object):
    user_id: str
    created_at: datetime
    status: str

    def __init__(self, user_id) -> None:
        self.user_id = str(user_id)
        self.created_at = datetime.now()
        self.status = 'created'

    def save(self) -> bool:
        try:
            collection = GenericMongoDB().get_collection('users')
            user_json = self.get_json()
            logging.info("[%s] Saving an user - Fields: [%s]", self.user_id, user_json)
            collection.insert_one(user_json)
        except Exception as erro:
            logging.exception("[%s] Error to insert at mongo. Erro: [%s]", self.user_id, erro)
            return False

        return True

    def get_json(self) -> dict:
        return {
                'user_id': self.user_id,
                'created_at': self.created_at,
                'status': self.status
            }
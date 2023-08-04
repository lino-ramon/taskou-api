import logging
import uuid

from api.model.user import User
from api.model.errors import SaveUserError
from api.model.generic_mongodb import GenericMongoDB
from flask import g as gvar

class UserService(object):
    def __init__(self) -> None:
        pass

    def create_user(self, request_exec_id):
        logging.info("[%s] ################## CREATING AN USER ##################", request_exec_id)
        response = {}
        try:
            logging.info("[%s] Generating User ID.", request_exec_id)
            user_id = str(uuid.uuid4())

            logging.info("[%s] Building User.", request_exec_id)
            user = User(user_id)

            logging.info("[%s] Saving User.", request_exec_id)
            result = user.save()

            if not result: 
                raise SaveUserError('Error Saving User.')

            logging.info("[%s] User created successfull.", request_exec_id)
            response = {
                    'user_id': user_id,
                    'message': 'User Created Successfull!'
                }
            gvar.user_id = user_id
        except SaveUserError as e:
            logging.exception("[%s] Erro to create user: [%s]", request_exec_id, e)
            response = {
                    'message': 'User Created Unsuccessfull!',
                    'erro': str(e)
                }
        return response
    
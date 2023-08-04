import logging
import uuid

from api.model.user import User
from api.model.errors import SaveUserError, UserNotFoundError
from api.model.generic_mongodb import GenericMongoDB

class UserService(object):
    def __init__(self) -> None:
        pass

    def generate_user(self, request_id):
        logging.info("[%s] ################## CREATING AN USER ##################", request_id)
        response = {}
        try:
            logging.info("[%s] Generating User ID.", request_id)
            user_id = str(uuid.uuid4())

            logging.info("[%s] Building User.", request_id)
            user = User(user_id)

            logging.info("[%s] Saving User.", request_id)
            result = user.save()

            if not result: 
                raise SaveUserError('Error Saving User.')

            logging.info("[%s] User created successfull.", request_id)
            response = {
                    'erro': 'success',
                    'user_id': user_id,
                    'message': 'User Created Successfull!'
                }
            
        except SaveUserError as e:
            logging.exception("[%s] Erro to create user: [%s]", request_id, e)
            response = {
                    'message': 'User Created Unsuccessfull!',
                    'erro': str(e)
                }
        return response
    
    def delete_user(self, request_id, user_id):
        logging.info("[%s] ################## DELITING AN USER ##################", request_id)
        response = {}
        try:
            user_collection = GenericMongoDB().get_collection('users')
            user_mongo = list(user_collection.find({'user_id': user_id}).limit(1))

            if not user_mongo:
                raise UserNotFoundError("User not exist in database")
            
            user_collection.delete_one({'user_id': user_id})
            logging.info("[%s] User [%s] Deleted!", request_id, user_id)
            response = {
                "erro": "success",
                "message": "User deleted successfull!"
            }
            
        except UserNotFoundError as e:
            logging.exception("[%s] Erro to delete user. Error: [%s]", request_id, e)
            response = {
                "erro": str(e),
                "message": "User delete unsuccessfull"
            }
        except Exception as e:
            logging.exception("[%s] Erro to delete user. Error: [%s]", request_id, e)
            response = {
                "erro": "Technical error",
                "message": "User delete unsuccessfull"
            }
        return response
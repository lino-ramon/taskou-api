import logging
import uuid

from api.model.user import User
from api.model.errors import SaveUserError, UserNotFoundError, ValidationUserError
from api.model.generic_mongodb import GenericMongoDB

class UserService(object):
    user_collection: str
    def __init__(self) -> None:
        self.user_collection = GenericMongoDB().get_collection('users')

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
            logging.exception("[%s] Erro to create user: [%s]", request_id, e, exc_info=False)
            response = {
                    'message': 'User Created Unsuccessfull!',
                    'erro': str(e)
                }
        return response
    
    def delete_user(self, request_id, user_id):
        logging.info("[%s] ################## DELITING AN USER ##################", request_id)
        response = {}
        try:
            logging.info("[%s] Chamando serviço de validação de usuário.", request_id)
            valid_user, message = self.validate_user(request_id, user_id)

            if not valid_user:
                raise ValidationUserError(message)
            
            self.user_collection.delete_one({'user_id': user_id})
            logging.info("[%s] User [%s] Deleted!", request_id, user_id)
            response = {
                "erro": "success",
                "message": "User deleted successfull!"
            }
            
        except ValidationUserError as e:
            logging.exception("[%s] Erro to delete user. Error: [%s]", request_id, e, exc_info=False)
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
    
    def validate_user(self, request_id, user_id):
        logging.info("[%s] ################## VALIDATING AN USER ##################", request_id)
        logging.info("[%s] User: [%s]", request_id, user_id)
        valid = False
        message = ''
        try:
            user_mongo = list(self.user_collection.find({'user_id': user_id}).limit(1))
        
            if not user_mongo:
                raise UserNotFoundError("User not exist in database")

            valid = True
            message = 'Valid'
            logging.info("[%s] Valid User!", request_id)
        except UserNotFoundError as e:
            logging.exception("[%s] Validation User Error: [%s]", request_id, e, exc_info=False)
            message = str(e)

        except Exception as e:
            logging.exception("[%s] Erro to delete user. Error: [%s]", request_id, e)
            message = "User validation unsuccessfull - Technical error"

        return valid, message

    def activate_user(self, request_id, user_id):
        logging.info("[%s] ################## ACTIVATING AN USER ##################", request_id)
        try:
            self.user_collection.update_one({'user_id': user_id}, {'$set': {'status': 'activated'}})
            logging.info("[%s] User activated!", request_id)
        except Exception as e:
            logging.exception("[%s] Erro to Active User. Error: [%s]", request_id, e)
            return False
        return True

    def activated_user(self, request_id, user_id):
        logging.info("[%s] ################## VERIFYING AN USER ACTIVATED ##################", request_id)
        try:
            activated_user_mongo = list(self.user_collection.find({'user_id': user_id, 'status': 'activated'}).limit(1))
            if not activated_user_mongo:
                logging.info("[%s] User not active", request_id)
                return False
        except Exception as e:
            logging.exception("[%s] Erro to Active User. Error: [%s]", request_id, e)
            return None
        
        logging.info("[%s] Active User!", request_id)
        return True
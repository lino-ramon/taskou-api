import logging
import uuid

from api.model.user import User
from api.model.errors import SaveUserError, TechnicalError
from api.model.generic_mongodb import GenericMongoDB

class CreateUserService(object):
    def __init__(self) -> None:
        pass

    def get_response(self,):
        logging.info("################## CREATING AN USER ##################")
        response = {}
        try:
            user_id = self.create_user_id()
            if not user_id:
                raise TechnicalError("Technical Error in UserID Creation.")

            logging.info("[%s] Building User.", user_id)
            user = User(user_id)
            result = user.save()

            if not result: 
                raise SaveUserError('Error Saving User.')

            logging.info("[%s] User created successfull.", user_id)
            response = {
                    'user_id': user_id,
                    'message': 'User Created Successfull!'
                }
        except TechnicalError as e:
            logging.exception("Erro to create user: [%s]", e)
            response = {
                    'message': 'User Created Unsuccessfull!',
                    'erro': str(e)
                }
        except SaveUserError as e:
            logging.exception("[%s] Erro to create user: [%s]", user_id, e)
            response = {
                    'message': 'User Created Unsuccessfull!',
                    'erro': str(e)
                }
        return response
    
    def create_user_id(self,):
        logging.info('Creation User ID.')
        user_id = self.generate_user_id()
        valid, validation_msg = self.validate_user_id(user_id)

        while not valid and validation_msg == 'exist':
            logging.info("User ID [%s] Existing. Retries generate UserID", user_id)
            user_id = self.generate_user_id()
            valid, validation_msg = self.validate_user_id(user_id)

        if validation_msg == 'error':
            logging.error("UserID not created.")
            return None
        
        logging.info("UserID Created. UserID: [%s]", user_id)
        return user_id

    def generate_user_id(self,):
        logging.info("Generation User ID.")
        return str(uuid.uuid4())
        
    def validate_user_id(self, user_id):
        logging.info("Validation User ID.")
        valid = False
        validation_msg = ''

        try:
            collection = GenericMongoDB().get_collection('users')
            finded_user = list(collection.find({'user_id': user_id}))

            if not finded_user:
                valid = True
                validation_msg = 'valid'
            else:
                validation_msg = 'exist'
                
        except Exception as e:
            logging.exception("[%s] Validation User ID Erro: [%s]", user_id, e)
            validation_msg = 'error'
        
        return valid, validation_msg
    
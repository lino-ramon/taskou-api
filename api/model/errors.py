# app/model/error.py

class TaskNotFoundError(LookupError):
    def __init__(self, message):
        self.mensagem = message

    def __str__(self):
        return self.mensagem

class UserNotFoundError(LookupError):
    def __init__(self, message):
        self.mensagem = message

    def __str__(self):
        return self.mensagem

class ValidationUserError(LookupError):
    def __init__(self, message):
        self.mensagem = message

    def __str__(self):
        return self.mensagem

class KeyError(KeyError):
    def __init__(self, message):
        self.mensagem = message

    def __str__(self):
        return self.mensagem
    
class SaveUserError(Exception):
    def __init__(self, message):
        self.mensagem = message

    def __str__(self):
        return self.mensagem


class ActivationUserError(Exception):
    def __init__(self, message):
        self.mensagem = message

    def __str__(self):
        return self.mensagem
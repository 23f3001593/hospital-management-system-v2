from flask import make_response, jsonify
from werkzeug.exceptions import HTTPException

class BaseError(HTTPException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def get_response(self):
        response = make_response(
            jsonify({'message': self.message}), self.status_code
        )
        return response

class ValidationError(BaseError):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)

class NotFoundError(BaseError):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)

class AlreadyExistError(BaseError):
    def __init__(self, message, status_code=409):
        super().__init__(message, status_code)

class MissingFieldsError(BaseError):
    def __init__(self, message, status_code=422):
        super().__init__(message, status_code)
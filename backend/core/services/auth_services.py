from core.models.models import User
from core.utils.exceptions import ValidationError,NotFoundError,MissingFieldsError

class AuthServices:

    @staticmethod
    def authenticate_user(data):
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['username'],data['password']]):
            raise MissingFieldsError("All fields are required.")
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            raise NotFoundError("Invalid username.")
        if not user.check_password(data['password']):
            raise ValidationError("Invalid password.")
        return user
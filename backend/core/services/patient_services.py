from core.extensions import db
from core.models.models import User,Patient
from core.utils.exceptions import ValidationError,AlreadyExistError,MissingFieldsError
from datetime import datetime

class PatientServices:

    @staticmethod
    def register_patient(data):
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['dob'], data['gender'], data['phone_number'], data['email'], data['address'], data['pincode'], data['username'], data['password']]):
            raise MissingFieldsError("All fields are required.")
        if not data['phone_number'][3:].isdigit() or len(data['phone_number']) != 13:
            raise ValidationError("Phone Number must be a 10-digit number.")
        if not data['pincode'].isdigit() or len(data['pincode']) != 6:
            raise ValidationError("Pincode must be a 6-digit number.")
        if len(data['username']) > 25:
            raise ValidationError("Username cannot exceed 25 characters.")
        if len(data['full_name']) > 100:
            raise ValidationError("Fullname cannot exceed 100 characters.")
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            raise AlreadyExistError("Username already exists.")
        dob = datetime.strptime(data['dob'],'%Y-%m-%d').date()
        new_user = User(username=data['username'], password=data['password'], email=data['email'], phone_number=data['phone_number'], full_name=data['full_name'], role='patient')
        db.session.add(new_user)
        db.session.commit()
        new_patient = Patient(user_id=new_user.id, dob=dob, gender=data['gender'], address=data['address'], pincode=data['pincode'])
        db.session.add(new_patient)
        db.session.commit()
        return new_user
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from core.extensions import db
from core.models.models import User,Patient,Appointment
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

UPLOAD_FOLDER = "core/static/uploads/patients"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class PatientServices:

    @staticmethod
    def create_patient(data):
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
        try:
            dob = datetime.strptime(data['dob'],'%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Invalid DOB format.")
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            raise AlreadyExistError("Username already exists.")
        new_user = User(username=data['username'], password=data['password'], email=data['email'], phone_number=data['phone_number'], full_name=data['full_name'], role='patient')
        db.session.add(new_user)
        db.session.flush()
        new_patient = Patient(user_id=new_user.id, dob=dob, gender=data['gender'], address=data['address'], pincode=data['pincode'])
        db.session.add(new_patient)
        db.session.commit()
        return new_user
    
    @staticmethod
    def read_patient(patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            raise NotFoundError("Patient not found.")
        return patient

    @staticmethod
    def update_patient(patient_id, data, file):
        patient = Patient.query.get(patient_id)
        if not patient:
            raise NotFoundError("Patient not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['phone_number'], data['email'], data['address'], data['pincode'], data['username'], data['password']]):
            raise MissingFieldsError("All fields are required.")
        if not data['phone_number'][3:].isdigit() or len(data['phone_number']) != 13:
            raise ValidationError("Phone Number must be a 10-digit number.")
        if not data['pincode'].isdigit() or len(data['pincode']) != 6:
            raise ValidationError("Pincode must be a 6-digit number.")
        if len(data['username']) > 25:
            raise ValidationError("Username cannot exceed 25 characters.")
        if len(data['full_name']) > 100:
            raise ValidationError("Fullname cannot exceed 100 characters.")
        if data['username'] != patient.user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != patient.user.id:
                raise AlreadyExistError("Username already exists.")
        remove_profile_picture_flag = data.get("remove_profile_picture") == "true"
        if remove_profile_picture_flag and patient.user.profile_picture:
            try:
                os.remove(patient.user.profile_picture)
            except FileNotFoundError:
                pass
            patient.user.profile_picture = None
        if file:
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError("Invalid file format. Allowed: png, jpg, jpeg, gif.")
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            if patient.user.profile_picture:
                try:
                    os.remove(patient.user.profile_picture)
                except FileNotFoundError:
                    pass
            new_filename = f"patient_{patient_id}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(filepath)
            patient.user.profile_picture = filepath
        patient.user.username = data['username']
        patient.user.password = data['password']
        patient.user.email = data['email']
        patient.user.phone_number = data['phone_number']
        patient.user.full_name = data['full_name']
        patient.address = data['address']
        patient.pincode = data['pincode']
        db.session.commit()
        return {"message":"Profile updated successfully."}
    
    @staticmethod
    def delete_patient(patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            raise NotFoundError("Patient not found.")
        if patient.user.is_archived:
            raise NotFoundError("Patient not found.")
        active_appointment = Appointment.query.filter(Appointment.patient_id==patient_id, Appointment.status=='booked').first()
        if active_appointment:
            raise ValidationError("Cannot delete account: You have an active appointment scheduled.")
        if patient.user.profile_picture:
            try:
                os.remove(patient.user.profile_picture)
            except FileNotFoundError:
                pass
            patient.user.profile_picture = None
        patient.user.is_archived = True
        db.session.commit()
        return {"message":"Account deleted successfully."}
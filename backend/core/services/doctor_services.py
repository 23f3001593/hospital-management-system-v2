import os
from decimal import Decimal,InvalidOperation
from werkzeug.utils import secure_filename
from core.extensions import db
from core.models.models import User,Doctor,Appointment
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

UPLOAD_FOLDER = "core/static/uploads/doctors"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class DoctorServices:
    
    @staticmethod
    def read_doctor(doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            raise NotFoundError("Doctor not found.")
        return doctor

    @staticmethod
    def update_doctor(doctor_id, data, file):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            raise NotFoundError("Doctor not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['phone_number'], data['email'], data['qualifications'], data['fees'], data['username'], data['password']]):
            raise MissingFieldsError("All fields are required.")
        if not data['phone_number'][3:].isdigit() or len(data['phone_number']) != 13:
            raise ValidationError("Phone Number must be a 10-digit number.")
        if len(data['username']) > 25:
            raise ValidationError("Username cannot exceed 25 characters.")
        if len(data['full_name']) > 100:
            raise ValidationError("Fullname cannot exceed 100 characters.")
        try:
            fees = Decimal(data['fees'])
        except InvalidOperation:
            raise ValidationError("Fees must be a numeric value.")
        if data['username'] != doctor.user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != doctor.user.id:
                raise AlreadyExistError("Username already exists.")
        remove_profile_picture_flag = data.get("remove_profile_picture") == "true"
        if remove_profile_picture_flag and doctor.user.profile_picture:
            try:
                os.remove(doctor.user.profile_picture)
            except FileNotFoundError:
                pass
            doctor.user.profile_picture = None
        if file:
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError("Invalid file format. Allowed: png, jpg, jpeg, gif.")
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            if doctor.user.profile_picture:
                try:
                    os.remove(doctor.user.profile_picture)
                except FileNotFoundError:
                    pass
            new_filename = f"doctor_{doctor_id}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(filepath)
            doctor.user.profile_picture = filepath
        doctor.user.username = data['username']
        doctor.user.password = data['password']
        doctor.user.email = data['email']
        doctor.user.phone_number = data['phone_number']
        doctor.user.full_name = data['full_name']
        doctor.qualifications = data['qualifications']
        doctor.fees = fees
        db.session.commit()
        return {"message":"Profile updated successfully."}
    
    @staticmethod
    def delete_doctor(doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            raise NotFoundError("Doctor not found.")
        if doctor.user.is_archived:
            raise NotFoundError("Doctor not found.")
        active_appointment = Appointment.query.filter(Appointment.doctor_id==doctor_id, Appointment.status=='booked').first()
        if active_appointment:
            raise ValidationError("Cannot delete doctor: An active appointment is assigned to it.")
        if doctor.user.profile_picture:
            try:
                os.remove(doctor.user.profile_picture)
            except FileNotFoundError:
                pass
            doctor.user.profile_picture = None
        doctor.user.is_archived = True
        db.session.commit()
        return {"message":"Account deleted successfully."}
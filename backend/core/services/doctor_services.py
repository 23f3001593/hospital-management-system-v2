import os
from decimal import Decimal,InvalidOperation
from werkzeug.utils import secure_filename
from core.extensions import db
from core.models.models import User,Doctor,Availability,Appointment
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

UPLOAD_FOLDER = "core/static/uploads/doctors"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class DoctorServices:
    
    @staticmethod
    def read_doctor(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "doctor") or not user.doctor:
            raise NotFoundError("Doctor not found.")
        return user.doctor

    @staticmethod
    def update_doctor(id, data, file):
        user = User.query.get(id)
        if not user or not hasattr(user, "doctor") or not user.doctor:
            raise NotFoundError("Doctor not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['phone_number'], data['email'], data['qualifications'], data['fees'], data['username'], data['current_password']]):
            raise MissingFieldsError("All fields are required.")
        if not user.check_password(data['current_password']):
            raise ValidationError("Invalid Password.")
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
        if data['username'] != user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != user.id:
                raise AlreadyExistError("Username already exists.")
        remove_profile_picture_flag = data.get("remove_profile_picture") == "true"
        if remove_profile_picture_flag and user.profile_picture:
            try:
                os.remove(user.profile_picture)
            except FileNotFoundError:
                pass
            user.profile_picture = None
        if file:
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError("Invalid file format. Allowed: png, jpg, jpeg, gif.")
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            if user.profile_picture:
                try:
                    os.remove(user.profile_picture)
                except FileNotFoundError:
                    pass
            new_filename = f"doctor_{user.doctor.doctor_id}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(filepath)
            user.profile_picture = filepath
        user.username = data['username']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.full_name = data['full_name']
        user.doctor.qualifications = data['qualifications']
        user.doctor.fees = fees
        if data['new_password']:
            user.password = data['new_password']
        db.session.commit()
        return {"message":"Profile updated successfully."}
    
    @staticmethod
    def delete_doctor(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "doctor") or not user.doctor:
            raise NotFoundError("Doctor not found.")
        if user.is_archived:
            raise NotFoundError("Doctor not found.")
        active_appointment = Appointment.query.filter(Appointment.doctor_id==user.doctor.doctor_id, Appointment.status=='booked').first()
        if active_appointment:
            raise ValidationError("Cannot delete doctor: An active appointment is assigned to it.")
        if user.profile_picture:
            try:
                os.remove(user.profile_picture)
            except FileNotFoundError:
                pass
            user.profile_picture = None
        user.is_archived = True
        db.session.commit()
        return {"message":"Account deleted successfully."}
    
    @staticmethod
    def read_availability(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "doctor") or not user.doctor:
            raise NotFoundError("Doctor not found.")
        doctor_id = user.doctor.doctor_id
        availabilities = Availability.query.filter_by(doctor_id=doctor_id).all()        
        availability_dict = {availability.week_day: [availability.forenoon_slot, availability.afternoon_slot] for availability in availabilities}
        return availability_dict
    
    @staticmethod
    def update_availability(id, data):
        user = User.query.get(id)
        if not user or not hasattr(user, "doctor") or not user.doctor:
            raise NotFoundError("Doctor not found.")
        doctor_id = user.doctor.doctor_id
        for week_day, slots in data.items():
            forenoon_slot, afternoon_slot = slots
            availability = Availability.query.filter_by(doctor_id=doctor_id, week_day=week_day).first()
            availability.forenoon_slot = bool(forenoon_slot)
            availability.afternoon_slot = bool(afternoon_slot)
        user.doctor.is_availability_updated = True
        db.session.commit()
        return {"message": "Availability updated successfully."}
import os
from datetime import time,datetime
from werkzeug.utils import secure_filename
from core.extensions import db
from core.models.models import User,Doctor,Patient,Slot,Appointment,Treatment
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
        return new_patient.to_dict(include_user=True)
    
    @staticmethod
    def read_patient(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        patient = Patient.query.get(user.patient.patient_id)
        return patient.to_dict(include_user=True)

    @staticmethod
    def update_patient(id, data, file):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['phone_number'], data['email'], data['address'], data['pincode'], data['username'], data['current_password']]):
            raise MissingFieldsError("All fields are required.")
        if not user.check_password(data['current_password']):
            raise ValidationError("Invalid Password.")
        if not data['phone_number'][3:].isdigit() or len(data['phone_number']) != 13:
            raise ValidationError("Phone Number must be a 10-digit number.")
        if not data['pincode'].isdigit() or len(data['pincode']) != 6:
            raise ValidationError("Pincode must be a 6-digit number.")
        if len(data['username']) > 25:
            raise ValidationError("Username cannot exceed 25 characters.")
        if len(data['full_name']) > 100:
            raise ValidationError("Fullname cannot exceed 100 characters.")
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
            new_filename = f"patient_{user.patient.patient_id}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(filepath)
            user.profile_picture = filepath
        user.username = data['username']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.full_name = data['full_name']
        user.patient.address = data['address']
        user.patient.pincode = data['pincode']
        if data['new_password']:
            user.password = data['new_password']
        db.session.commit()
        doctor_user_ids = [row[0]
            for row in db.session.query(User.id)
                .join(Doctor, Doctor.user_id == User.id)
                .join(Appointment, Appointment.doctor_id == Doctor.doctor_id)
                .filter(
                    Appointment.patient_id == user.patient.patient_id,
                    Appointment.status == "booked"
                )
                .distinct()
                .all()
        ]
        return {"message":"Profile updated successfully.", "data": user.patient.to_dict(include_user=True), "doctor_user_ids": doctor_user_ids}
    
    @staticmethod
    def delete_patient(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        active_appointment = Appointment.query.filter(Appointment.patient_id==user.patient.patient_id, Appointment.status=='booked').first()
        if active_appointment:
            raise ValidationError("Cannot delete account: An active appointment is assigned.")
        if user.profile_picture:
            try:
                os.remove(user.profile_picture)
            except FileNotFoundError:
                pass
            user.profile_picture = None
        user.is_archived = True
        db.session.commit()
        return {"message":"Account deleted successfully.", "data": user.patient.to_dict(include_user=True)}
    
    @staticmethod
    def create_appointment(data, id, doctor_id):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['day'], data['date'], data['time']]):
            raise MissingFieldsError("All fields are required.")
        try:
            appointment_date = datetime.strptime(data['date'],'%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Invalid Date format.")
        try:
            label = data['time']
            start_label = label.split(" - ")[0]
            slot_time_dt = datetime.strptime(start_label, "%I:%M%p")
            slot_time = time(slot_time_dt.hour, slot_time_dt.minute)
        except:
            raise ValidationError("Invalid Time format.")
        slot = Slot.query.filter_by(doctor_id=doctor_id, week_day=data['day'], slot_time=slot_time).first()
        if not slot:
            raise NotFoundError("Slot not found.")
        if slot.status == "booked":
            raise AlreadyExistError("This slot is already booked.")
        slot.status = "booked"
        new_appointment = Appointment(patient_id=user.patient.patient_id, doctor_id=doctor_id, slot_id=slot.slot_id, appointment_date=appointment_date)
        db.session.add(new_appointment)
        db.session.commit()
        return {"message":"Appointment booked successfully.", "data": new_appointment.to_dict(include_doctor=True, include_patient=True)}
    
    @staticmethod
    def update_appointment(data, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            raise NotFoundError("Appointment not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['day'], data['date'], data['time']]):
            raise MissingFieldsError("All fields are required.")
        try:
            appointment_date = datetime.strptime(data['date'],'%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Invalid Date format.")
        try:
            label = data['time']
            start_label = label.split(" - ")[0]
            slot_time_dt = datetime.strptime(start_label, "%I:%M%p")
            slot_time = time(slot_time_dt.hour, slot_time_dt.minute)
        except:
            raise ValidationError("Invalid Time format.")
        appointment.slot.status = "available"
        slot = Slot.query.filter_by(doctor_id=appointment.doctor_id, week_day=data['day'], slot_time=slot_time).first()
        if not slot:
            raise NotFoundError("Slot not found.")
        if slot.status == "booked":
            raise AlreadyExistError("This slot is already booked.")
        slot.status = "booked"
        appointment.slot_id = slot.slot_id
        appointment.appointment_date = appointment_date
        db.session.commit()
        return {"message":"Appointment rescheduled successfully.", "data": appointment.to_dict(include_doctor=True, include_patient=True)}
    
    @staticmethod
    def delete_appointment(appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            raise NotFoundError("Appointment not found.")
        if appointment.status!="booked":
            raise NotFoundError("Appointment not found.")
        appointment.slot.status = "available"
        appointment.status = "cancelled"
        db.session.commit()
        return {"message":"Appointment cancelled successfully.", "data": appointment.to_dict(include_doctor=True, include_patient=True)}

    @staticmethod
    def all_scheduled_appointments(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        appointments = Appointment.query.filter_by(patient_id=user.patient.patient_id, status="booked").all()
        return {"appointments": [appointment.to_dict(include_doctor=True, include_slot=True) for appointment in appointments]}
    
    @staticmethod
    def all_past_appointments(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        appointments = Appointment.query.filter(Appointment.patient_id==user.patient.patient_id, Appointment.status!="booked").all()
        return {"appointments": [appointment.to_dict(include_doctor=True, include_slot=True) for appointment in appointments]}
    
    @staticmethod
    def all_treatments(id):
        user = User.query.get(id)
        if not user or not hasattr(user, "patient") or not user.patient:
            raise NotFoundError("Patient not found.")
        if user.is_archived:
            raise NotFoundError("Patient not found.")
        treatments = Treatment.query.join(Appointment).filter(Appointment.patient_id == user.patient.patient_id).all()
        return {"treatments": [{
            **treatment.to_dict(include_appointment=True),
            "doctor": treatment.appointment.doctor.to_dict(include_user=True, include_department=True)
        } for treatment in treatments]}
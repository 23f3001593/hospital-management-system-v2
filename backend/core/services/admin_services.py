from datetime import datetime
from decimal import Decimal,InvalidOperation
from core.extensions import db
from core.models.models import User,Department,Doctor,Patient,Availability,Slot,Appointment
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

class AdminServices:

    @staticmethod
    def read_admin():
        admin = User.query.filter_by(role='admin').first()
        return admin.to_dict()

    @staticmethod
    def update_admin(data):
        admin = User.query.filter_by(role='admin').first()
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['phone_number'], data['email'], data['username'], data['current_password']]):
            raise MissingFieldsError("All fields are required.")
        if not admin.check_password(data['current_password']):
            raise ValidationError("Invalid Password.")
        if not data['phone_number'][3:].isdigit() or len(data['phone_number']) != 13:
            raise ValidationError("Phone Number must be a 10-digit number.")
        if len(data['username']) > 25:
            raise ValidationError("Username cannot exceed 25 characters.")
        if len(data['full_name']) > 100:
            raise ValidationError("Fullname cannot exceed 100 characters.")
        if data['username'] != admin.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != admin.id:
                raise AlreadyExistError("Username already exists.")
        admin.username = data['username']
        admin.email = data['email']
        admin.phone_number = data['phone_number']
        admin.full_name = data['full_name']
        if data['new_password']:
            admin.password = data['new_password']
        db.session.commit()
        return {"message":"Profile updated successfully.", "data": admin.to_dict()}

    @staticmethod
    def create_department(data):
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['department_name'], data['department_description']]):
            raise MissingFieldsError("All fields are required.")
        if len(data['department_name']) > 100:
            raise ValidationError("Department Name cannot exceed 100 characters.")
        existing_department = Department.query.filter_by(department_name=data['department_name']).first()
        if existing_department:
            raise AlreadyExistError("Department Name already exists.")
        new_department = Department(department_name=data['department_name'], department_description=data['department_description'])
        db.session.add(new_department)
        db.session.commit()
        return {"message":"Department created successfully.", "data": new_department.to_dict()}
    
    @staticmethod
    def read_department(department_id):
        department = Department.query.get(department_id)
        if not department:
            raise NotFoundError("Department not found.")
        return department.to_dict(include_doctors=True)
    
    @staticmethod
    def update_department(department_id, data):
        department = Department.query.get(department_id)
        if not department:
            raise NotFoundError("Department not found.")
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['department_name'], data['department_description']]):
            raise MissingFieldsError("All fields are required.")
        if len(data['department_name']) > 100:
            raise ValidationError("Department Name cannot exceed 100 characters.")
        if data['department_name'] != department.department_name:
            existing_department = Department.query.filter_by(department_name=data['department_name']).first()
            if existing_department and existing_department.department_id != department_id:
                raise AlreadyExistError("Department Name already exists.")
        department.department_name = data['department_name']
        department.department_description = data['department_description']
        db.session.commit()
        return {"message":"Department updated successfully.", "data": department.to_dict()}
    
    @staticmethod
    def delete_department(department_id):
        department = Department.query.get(department_id)
        if not department:
            raise NotFoundError("Department not found.")
        if department.is_archived:
            raise NotFoundError("Department not found.")
        active_doctor = Doctor.query.filter(Doctor.department_id==department_id, Doctor.user.has(is_archived=False)).first()
        if active_doctor:
            raise ValidationError("Cannot delete department: An active doctor is assigned to it.")
        department.is_archived = True
        db.session.commit()
        return {"message":"Department deleted successfully.", "data": department.to_dict()}
    
    @staticmethod
    def all_departments():
        departments = Department.query.filter(Department.is_archived==False).all()
        archived_departments = Department.query.filter_by(is_archived=True).all()
        return {
            "departments": [department.to_dict(include_doctors=True) for department in departments],
            "archived_departments": [department.to_dict(include_doctors=True) for department in archived_departments]
        }

    @staticmethod
    def assign_hod(department_id, doctor_id):
        department = Department.query.get(department_id)
        if not department:
            raise NotFoundError("Department not found.")
        department.hod_id = doctor_id
        db.session.commit()
        return {"message":"HOD assigned successfully.", "data": department.to_dict()}
    
    @staticmethod
    def create_doctor(data):
        if not data:
            raise MissingFieldsError("All fields are required.")
        if not all([data['full_name'], data['phone_number'], data['email'], data['license_number'], data['department_id'], data['qualifications'], data['practice_start_date'], data['fees'], data['username'], data['password']]):
            raise MissingFieldsError("All fields are required.")
        if not data['phone_number'][3:].isdigit() or len(data['phone_number']) != 13:
            raise ValidationError("Phone Number must be a 10-digit number.")
        if len(data['username']) > 25:
            raise ValidationError("Username cannot exceed 25 characters.")
        if len(data['full_name']) > 100:
            raise ValidationError("Fullname cannot exceed 100 characters.")
        if len(data['license_number']) > 25:
            raise ValidationError("License Number cannot exceed 25 characters.")
        try:
            department_id = int(data['department_id'])
        except ValueError:
            raise ValidationError("Department ID must be an integer.")
        try:
            practice_start_date = datetime.strptime(data['practice_start_date'],'%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Invalid practice start date format.")
        try:
            fees = Decimal(data['fees'])
        except InvalidOperation:
            raise ValidationError("Fees must be a numeric value.")
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            raise AlreadyExistError("Username already exists.")
        existing_doctor = Doctor.query.filter_by(license_number=data['license_number']).first()
        if existing_doctor:
            raise AlreadyExistError("Doctor with same License Number already exists.")
        new_user = User(username=data['username'], password=data['password'], email=data['email'], phone_number=data['phone_number'], full_name=data['full_name'], role='doctor')
        db.session.add(new_user)
        db.session.flush()
        new_doctor = Doctor(user_id=new_user.id, department_id=department_id, license_number=data['license_number'], qualifications=data['qualifications'], practice_start_date=practice_start_date, fees=fees)
        db.session.add(new_doctor)
        db.session.flush()
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in week_days:
            availability = Availability(doctor_id=new_doctor.doctor_id, week_day=day, forenoon_slot=False, afternoon_slot=False)
            db.session.add(availability)
        db.session.flush()
        slot_times = ["10:00", "11:00", "12:00", "16:00", "17:00", "18:00"]
        for day in week_days:
            for time_str in slot_times:
                slot_time = datetime.strptime(time_str, "%H:%M").time()
                slot = Slot(doctor_id=new_doctor.doctor_id, week_day=day, slot_time=slot_time)
                db.session.add(slot)
        db.session.commit()
        return {"message":"Doctor created successfully.", "data": new_doctor.to_dict(include_user=True, include_department=True, include_availabilities=True, include_slots=True)}

    @staticmethod
    def all_doctors():
        doctors = Doctor.query.filter(Doctor.user.has(is_archived=False)).all()
        archived_doctors = Doctor.query.filter(Doctor.user.has(is_archived=True)).all()
        return {
            "doctors": [doctor.to_dict(include_user=True, include_department=True) for doctor in doctors],
            "archived_doctors": [doctor.to_dict(include_user=True, include_department=True) for doctor in archived_doctors]
        }
    
    @staticmethod
    def all_patients():
        patients = Patient.query.filter(Patient.user.has(is_archived=False)).all()
        archived_patients = Patient.query.filter(Patient.user.has(is_archived=True)).all()
        return {
            "patients": [patient.to_dict(include_user=True) for patient in patients],
            "archived_patients": [patient.to_dict(include_user=True) for patient in archived_patients]
        }
    
    @staticmethod
    def all_appointments():
        scheduled_appointments = Appointment.query.filter_by(status="booked").all()
        past_appointments = Appointment.query.filter(Appointment.status!="booked").all()
        return {
            "scheduled_appointments": [appointment.to_dict(include_doctor=True, include_patient=True, include_slot=True) for appointment in scheduled_appointments],
            "past_appointments": [appointment.to_dict(include_doctor=True, include_patient=True, include_slot=True) for appointment in past_appointments]
        }
    
    @staticmethod
    def admin_summary():
        doctor_count = User.query.filter_by(role="doctor", is_archived=False).count()
        patient_count = User.query.filter_by(role="patient", is_archived=False).count()
        appointment_count = Appointment.query.filter_by(status="booked").count()
        return {"doctor_count": doctor_count, "patient_count": patient_count, "appointment_count": appointment_count}
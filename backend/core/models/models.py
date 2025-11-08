from core.extensions import db,bcrypt
from core.utils.exceptions import ValidationError

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    role = db.Column(db.String(7), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (
        db.CheckConstraint("length(phone_number)=13", name="phone_length_check"),
        db.CheckConstraint("role IN ('admin','doctor','patient')", name="role_check"),
    )
    doctor = db.relationship('Doctor', backref='user', uselist=False)
    patient = db.relationship('Patient', backref='user', uselist=False)
    
    @property
    def password(self):
        raise ValidationError("Access to the password is prohibited.")
    
    @password.setter
    def password(self,plain_text):
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')
    
    def check_password(self,plain_text):
        return bcrypt.check_password_hash(self.password_hash,plain_text)

    def to_dict(self, include_doctor=False, include_patient=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "full_name": self.full_name,
            "profile_picture": self.profile_picture,
            "role": self.role,
            "is_archived": self.is_archived
        }
        if include_doctor and self.doctor:
            data["doctor"] = self.doctor.to_dict(include_user=False)
        if include_patient and self.patient:
            data["patient"] = self.patient.to_dict(include_user=False)
        return data

class Department(db.Model):
    __tablename__ = "department"
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    department_description = db.Column(db.Text, nullable=False)
    hod_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"))
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    hod = db.relationship('Doctor', foreign_keys=[hod_id], post_update=True, uselist=False)
    doctors = db.relationship('Doctor', backref='department', foreign_keys="Doctor.department_id")

    def to_dict(self, include_doctors=False):
        data = {
            "department_id": self.department_id,
            "department_name": self.department_name,
            "department_description": self.department_description,
            "hod_id": self.hod_id,
            "is_archived": self.is_archived,
            "hod_name": self.hod.user.full_name if self.hod else None
        }
        if include_doctors:
            data["doctors"] = [doctor.to_dict(include_department=False, include_user=True) for doctor in self.doctors if not doctor.user.is_archived]
        return data

class Doctor(db.Model):
    __tablename__ = "doctor"
    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.department_id"), nullable=False)
    license_number = db.Column(db.String(25), unique=True, nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    practice_start_date = db.Column(db.Date, nullable=False)
    fees = db.Column(db.Numeric, nullable=False)
    availabilities = db.relationship('Availability', backref='doctor')
    slots = db.relationship('Slot', backref='doctor')
    appointments = db.relationship('Appointment', backref='doctor')

    def to_dict(self, include_user=False, include_department=False, include_availabilities=False, include_slots=False, include_appointments=False):
        data = {
            "doctor_id": self.doctor_id,
            "user_id": self.user_id,
            "department_id": self.department_id,
            "license_number": self.license_number,
            "qualifications": self.qualifications,
            "practice_start_date": self.practice_start_date.isoformat(),
            "fees": float(self.fees)
        }
        if include_user:
            data["user"] = self.user.to_dict(include_doctor=False)
        if include_department:
            data["department"] = self.department.to_dict(include_doctors=False)
        if include_availabilities:
            data["availabilities"] = [availability.to_dict() for availability in self.availabilities]
        if include_slots:
            data["slots"] = [slot.to_dict() for slot in self.slots]
        if include_appointments:
            data["appointments"] = [appointment.to_dict(include_doctor=False) for appointment in self.appointments]
        return data

class Patient(db.Model):
    __tablename__ = "patient"
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    __table_args__ = (
        db.CheckConstraint("gender IN ('male','female')", name="gender_check"),
        db.CheckConstraint("length(pincode)=6", name="pincode_length_check"),
    )
    appointments = db.relationship('Appointment', backref='patient')

    def to_dict(self, include_user=False, include_appointments=False):
        data = {
            "patient_id": self.patient_id,
            "user_id": self.user_id,
            "dob": self.dob.isoformat(),
            "gender": self.gender,
            "address": self.address,
            "pincode": self.pincode
        }
        if include_user:
            data["user"] = self.user.to_dict(include_patient=False)
        if include_appointments:
            data["appointments"] = [appointment.to_dict(include_patient=False) for appointment in self.appointments]
        return data

class Availability(db.Model):
    __tablename__ = "availability"
    availability_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    week_day = db.Column(db.String(9), nullable=False)
    forenoon_slot = db.Column(db.Boolean, nullable=False, default=False)
    afternoon_slot = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (
        db.CheckConstraint("week_day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')", name="availability_weekday_check"),
    )

    def to_dict(self):
        return {
            "availability_id": self.availability_id,
            "doctor_id": self.doctor_id,
            "week_day": self.week_day,
            "forenoon_slot": self.forenoon_slot,
            "afternoon_slot": self.afternoon_slot
        }

class Slot(db.Model):
    __tablename__ = "slot"
    slot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    week_day = db.Column(db.String(9), nullable=False)
    slot_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(11), nullable=False, default="unavailable")
    __table_args__ = (
        db.CheckConstraint("week_day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')", name="slot_weekday_check"),
        db.CheckConstraint("status IN ('available','booked','unavailable')", name="slot_status_check"),
    )
    appointments = db.relationship('Appointment', backref='slot')

    def to_dict(self, include_appointments=False):
        data = {
            "slot_id": self.slot_id,
            "doctor_id": self.doctor_id,
            "week_day": self.week_day,
            "slot_time": self.slot_time.isoformat(),
            "status": self.status
        }
        if include_appointments:
            data["appointments"] = [appointment.to_dict() for appointment in self.appointments]
        return data

class Appointment(db.Model):
    __tablename__ = "appointment"
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey("slot.slot_id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(9), nullable=False, default="booked")
    __table_args__ = (
        db.CheckConstraint("status IN ('booked','completed','cancelled')", name="appointment_status_check"),
    )
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

    def to_dict(self, include_doctor=False, include_patient=False, include_treatment=False):
        data = {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "slot_id": self.slot_id,
            "appointment_date": self.appointment_date.isoformat(),
            "status": self.status
        }
        if include_doctor:
            data["doctor"] = self.doctor.to_dict(include_appointments=False)
        if include_patient:
            data["patient"] = self.patient.to_dict(include_appointments=False)
        if include_treatment and self.treatment:
            data["treatment"] = self.treatment.to_dict()
        return data

class Treatment(db.Model):
    __tablename__ = "treatment"
    treatment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.appointment_id"), nullable=False)
    tests = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "treatment_id": self.treatment_id,
            "appointment_id": self.appointment_id,
            "tests": self.tests,
            "diagnosis": self.diagnosis,
            "prescription": self.prescription,
            "medicines": self.medicines,
            "notes": self.notes
        }

admin_data = ("ramkumar", "Ram&Kumar9", "ramkumar@example.com", "+915555555555", "Ram Kumar", "admin")
def create_admin(admin_data = admin_data):
    if not User.query.filter_by(username=admin_data[0]).first():
        new_admin = User(
            username=admin_data[0],
            password=admin_data[1],
            email=admin_data[2],
            phone_number=admin_data[3],
            full_name=admin_data[4],
            role=admin_data[5]
        )
        db.session.add(new_admin)
        db.session.commit()
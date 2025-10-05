from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    role = db.Column(db.String(7), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (
        db.CheckConstraint("length(phone_number)=10", name="phone_length_check"),
        db.CheckConstraint("role IN ('admin','doctor','patient')", name="role_check"),
    )
    doctor = db.relationship('Doctor', backref='user', uselist=False)
    patient = db.relationship('Patient', backref='user', uselist=False)

class Department(db.Model):
    __tablename__ = "department"
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    department_description = db.Column(db.Text, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    doctors = db.relationship('Doctor', backref='department')

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

class Treatment(db.Model):
    __tablename__ = "treatment"
    treatment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.appointment_id"), nullable=False)
    tests = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=False)

admin_data = ("ramkumar", "RamKumar9", "ramkumar@gmail.com", "9999999999", "Ram Kumar", "admin")
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
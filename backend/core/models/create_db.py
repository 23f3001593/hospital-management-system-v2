import sqlite3

conn = sqlite3.connect('database.sqlite3')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(25) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(13) NOT NULL CHECK(length(phone_number)=13),
    full_name VARCHAR(100) NOT NULL,
    profile_picture VARCHAR(255),
    role VARCHAR(7) NOT NULL CHECK(role IN ('admin','doctor','patient')),
    is_archived BOOLEAN NOT NULL DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS department(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    department_description TEXT NOT NULL,
    hod_id INTEGER,
    is_archived BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY(hod_id) REFERENCES doctor(doctor_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor(
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    license_number VARCHAR(25) UNIQUE NOT NULL,
    qualifications TEXT NOT NULL,
    practice_start_date DATE NOT NULL,
    fees NUMERIC NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(department_id) REFERENCES department(department_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(6) NOT NULL CHECK(gender IN ('male','female')),
    address TEXT NOT NULL,
    pincode VARCHAR(6) NOT NULL CHECK(length(pincode)=6),
    FOREIGN KEY(user_id) REFERENCES user(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS availability(
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    week_day VARCHAR(9) NOT NULL CHECK(week_day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    forenoon_slot BOOLEAN NOT NULL DEFAULT 0,
    afternoon_slot BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS slot(
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    week_day VARCHAR(9) NOT NULL CHECK(week_day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    slot_time TIME NOT NULL,
    status VARCHAR(11) NOT NULL CHECK(status IN ('available','booked','unavailable')) DEFAULT 'unavailable',
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS appointment(
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    status VARCHAR(9) NOT NULL CHECK(status IN ('booked','completed','cancelled')) DEFAULT 'booked',
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY(slot_id) REFERENCES slot(slot_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS treatment(
    treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    tests TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    prescription TEXT NOT NULL,
    medicines TEXT NOT NULL,
    notes TEXT NOT NULL,
    FOREIGN KEY(appointment_id) REFERENCES appointment(appointment_id)
)
''')

conn.commit()
cursor.close()
conn.close()
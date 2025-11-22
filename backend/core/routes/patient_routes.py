from flask import Blueprint,jsonify,request
from core.services.patient_services import PatientServices
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

patient_bp = Blueprint('patient_bp',__name__)

@patient_bp.route('', methods=['POST'])
def create_patient():
    try:
        data = request.json
        user = PatientServices.create_patient(data)
        return jsonify(user.to_dict()),200
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:id>', methods=['GET'])
def read_patient(id):
    try:
        patient = PatientServices.read_patient(id)
        return jsonify(patient.to_dict(include_user=True)),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:id>', methods=['PUT'])
def update_patient(id):
    try:
        data = request.form.to_dict()
        file = request.files.get('profile_picture')
        message = PatientServices.update_patient(id, data, file)
        return jsonify(message),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:id>', methods=['PATCH'])
def delete_patient(id):
    try:
        message = PatientServices.delete_patient(id)
        return jsonify(message),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointment/<int:id>/<int:doctor_id>', methods=['POST'])
def create_appointment(id, doctor_id):
    try:
        data = request.json
        message = PatientServices.create_appointment(data, id, doctor_id)
        return jsonify(message),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        data = request.json
        message = PatientServices.update_appointment(data, appointment_id)
        return jsonify(message),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointment/<int:appointment_id>', methods=['PATCH'])
def delete_appointment(appointment_id):
    try:
        message = PatientServices.delete_appointment(appointment_id)
        return jsonify(message),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointments/<int:id>', methods=['GET'])
def all_scheduled_appointments(id):
    try:
        appointments = PatientServices.all_scheduled_appointments(id)
        return jsonify({"appointments": [appointment.to_dict(include_doctor=True, include_slot=True) for appointment in appointments]}),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/treatments/<int:id>', methods=['GET'])
def all_treatments(id):
    try:
        treatments = PatientServices.all_treatments(id)
        return jsonify({"treatments": [{
            **treatment.to_dict(include_appointment=True),
            "doctor": treatment.appointment.doctor.to_dict(include_user=True, include_department=True)
        } for treatment in treatments]}),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
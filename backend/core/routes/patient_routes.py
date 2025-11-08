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

@patient_bp.route('/<int:patient_id>', methods=['GET'])
def read_patient(patient_id):
    try:
        patient = PatientServices.read_patient(patient_id)
        return jsonify(patient.to_dict(include_user=True)),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    try:
        data = request.form.to_dict()
        file = request.files.get('profile_picture')
        message = PatientServices.update_patient(patient_id, data, file)
        return jsonify(message),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:patient_id>', methods=['PATCH'])
def delete_patient(patient_id):
    try:
        message = PatientServices.delete_patient(patient_id)
        return jsonify(message),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
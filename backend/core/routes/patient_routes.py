from flask import Blueprint,jsonify,request
from core.services.patient_services import PatientServices
from core.utils.exceptions import ValidationError,AlreadyExistError,MissingFieldsError

patient_bp = Blueprint('patient_bp',__name__)

@patient_bp.route('/register', methods=['POST'])
def register_patient():
    try:
        data = request.json
        user = PatientServices.register_patient(data)
        return jsonify(user.to_dict()),200
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception as e:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
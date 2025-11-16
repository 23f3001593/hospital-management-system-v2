from flask import Blueprint,jsonify,request
from core.services.doctor_services import DoctorServices
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

doctor_bp = Blueprint('doctor_bp',__name__)

@doctor_bp.route('/<int:id>', methods=['GET'])
def read_doctor(id):
    try:
        doctor = DoctorServices.read_doctor(id)
        return jsonify(doctor.to_dict(include_user=True, include_department=True)),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/<int:id>', methods=['PUT'])
def update_doctor(id):
    try:
        data = request.form.to_dict()
        file = request.files.get('profile_picture')
        message = DoctorServices.update_doctor(id, data, file)
        return jsonify(message),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/<int:id>', methods=['PATCH'])
def delete_doctor(id):
    try:
        message = DoctorServices.delete_doctor(id)
        return jsonify(message),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/availability/<int:id>', methods=['GET'])
def read_availability(id):
    try:
        availability = DoctorServices.read_availability(id)
        return jsonify(availability),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/availability/<int:id>', methods=['PUT'])
def update_availability(id):
    try:
        data = request.json
        message = DoctorServices.update_availability(id, data)
        return jsonify(message),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
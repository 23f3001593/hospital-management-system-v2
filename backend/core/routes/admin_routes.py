from flask import Blueprint,jsonify,request
from core.services.admin_services import AdminServices
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

admin_bp = Blueprint('admin_bp',__name__)

@admin_bp.route('', methods=['GET'])
def read_admin():
    try:
        admin = AdminServices.read_admin()
        return jsonify(admin.to_dict()),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('', methods=['PUT'])
def update_admin():
    try:
        data = request.json
        message = AdminServices.update_admin(data)
        return jsonify(message),200
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department', methods=['POST'])
def create_department():
    try:
        data = request.json
        message = AdminServices.create_department(data)
        return jsonify(message),200
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department/<int:department_id>', methods=['GET'])
def read_department(department_id):
    try:
        department = AdminServices.read_department(department_id)
        return jsonify(department.to_dict(include_doctors=True)),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    try:
        data = request.json
        message = AdminServices.update_department(department_id, data)
        return jsonify(message),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department/<int:department_id>', methods=['PATCH'])
def delete_department(department_id):
    try:
        message = AdminServices.delete_department(department_id)
        return jsonify(message),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/departments', methods=['GET'])
def all_departments():
    try:
        departments,archived_departments = AdminServices.all_departments()
        return jsonify({
            "departments": [department.to_dict(include_doctors=True) for department in departments],
            "archived_departments": [department.to_dict(include_doctors=True) for department in archived_departments]
        }),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/assign-hod/<int:department_id>/<int:doctor_id>', methods=['PUT'])
def assign_hod(department_id, doctor_id):
    try:
        message = AdminServices.assign_hod(department_id, doctor_id)
        return jsonify(message),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/doctor', methods=['POST'])
def create_doctor():
    try:
        data = request.json
        message = AdminServices.create_doctor(data)
        return jsonify(message),200
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/doctors', methods=['GET'])
def all_doctors():
    try:
        doctors,archived_doctors = AdminServices.all_doctors()
        return jsonify({
            "doctors": [doctor.to_dict(include_user=True, include_department=True) for doctor in doctors],
            "archived_doctors": [doctor.to_dict(include_user=True, include_department=True) for doctor in archived_doctors]
        }),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/patients', methods=['GET'])
def all_patients():
    try:
        patients,archived_patients = AdminServices.all_patients()
        return jsonify({
            "patients": [patient.to_dict(include_user=True) for patient in patients],
            "archived_patients": [patient.to_dict(include_user=True) for patient in archived_patients]
        }),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/appointments', methods=['GET'])
def all_appointments():
    try:
        scheduled_appointments,past_appointments = AdminServices.all_appointments()
        return jsonify({
            "scheduled_appointments": [appointment.to_dict(include_doctor=True, include_patient=True) for appointment in scheduled_appointments],
            "past_appointments": [appointment.to_dict(include_doctor=True, include_patient=True, include_treatment=True) for appointment in past_appointments]
        }),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
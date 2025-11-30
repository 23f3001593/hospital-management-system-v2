from flask import Blueprint,jsonify,request
from core.extensions import cache
from core.services.admin_services import AdminServices
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

admin_bp = Blueprint('admin_bp',__name__)

@admin_bp.route('', methods=['GET'])
def read_admin():
    try:
        cache_key = "admin:profile"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.read_admin()
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('', methods=['PUT'])
def update_admin():
    try:
        data = request.json
        response = AdminServices.update_admin(data)
        cache.delete("admin:profile")
        return jsonify(response),200
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department', methods=['POST'])
def create_department():
    try:
        data = request.json
        response = AdminServices.create_department(data)
        cache.delete("admin:departments")
        return jsonify(response),201
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department/<int:department_id>', methods=['GET'])
def read_department(department_id):
    try:
        cache_key = f"admin:department:{department_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.read_department(department_id)
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    try:
        data = request.json
        response = AdminServices.update_department(department_id, data)
        cache.delete(f"admin:department:{department_id}")
        cache.delete("admin:departments")
        cache.delete("admin:doctors")
        cache.delete("admin:appointments")
        redis = cache.cache._write_client
        for key in redis.scan_iter("doctor:profile:*"):
            redis.delete(key)
        return jsonify(response),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/department/<int:department_id>', methods=['PATCH'])
def delete_department(department_id):
    try:
        response = AdminServices.delete_department(department_id)
        cache.delete(f"admin:department:{department_id}")
        cache.delete("admin:departments")
        return jsonify(response),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/departments', methods=['GET'])
def all_departments():
    try:
        cache_key = "admin:departments"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.all_departments()
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/assign-hod/<int:department_id>/<int:doctor_id>', methods=['PUT'])
def assign_hod(department_id, doctor_id):
    try:
        response = AdminServices.assign_hod(department_id, doctor_id)
        cache.delete(f"admin:department:{department_id}")
        cache.delete("admin:departments")
        cache.delete("admin:doctors")
        cache.delete("admin:appointments")
        redis = cache.cache._write_client
        for key in redis.scan_iter("doctor:profile:*"):
            redis.delete(key)
        return jsonify(response),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/doctor', methods=['POST'])
def create_doctor():
    try:
        data = request.json
        response = AdminServices.create_doctor(data)
        cache.delete("admin:doctors")
        cache.delete(f"admin:department:{response['data']['department']['department_id']}")
        cache.delete("admin:departments")
        cache.delete("admin:summary")
        return jsonify(response),201
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/doctors', methods=['GET'])
def all_doctors():
    try:
        cache_key = "admin:doctors"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.all_doctors()
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/patients', methods=['GET'])
def all_patients():
    try:
        cache_key = "admin:patients"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.all_patients()
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/appointments', methods=['GET'])
def all_appointments():
    try:
        cache_key = "admin:appointments"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.all_appointments()
        cache.set(cache_key, data, timeout=300)
        return jsonify(data),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@admin_bp.route('/summary', methods=['GET'])
def admin_summary():
    try:
        cache_key = "admin:summary"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = AdminServices.admin_summary()
        cache.set(cache_key, data, timeout=60)
        return jsonify(data),200
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
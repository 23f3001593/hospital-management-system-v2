from flask import Blueprint,jsonify,request
from core.extensions import cache
from core.services.doctor_services import DoctorServices
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

doctor_bp = Blueprint('doctor_bp',__name__)

@doctor_bp.route('/<int:id>', methods=['GET'])
def read_doctor(id):
    try:
        cache_key = f"doctor:profile:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = DoctorServices.read_doctor(id)
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/<int:id>', methods=['PUT'])
def update_doctor(id):
    try:
        data = request.form.to_dict()
        file = request.files.get('profile_picture')
        response = DoctorServices.update_doctor(id, data, file)
        cache.delete(f"doctor:profile:{id}")
        cache.delete("admin:doctors")
        cache.delete(f"admin:department:{response['data']['department']['department_id']}")
        cache.delete("admin:departments")
        cache.delete("admin:appointments")
        redis = cache.cache._write_client
        for id in response['patient_user_ids']:
            for key in redis.scan_iter(f"patient:appointments:scheduled:{id}"):
                redis.delete(key)
        return jsonify(response),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/<int:id>', methods=['PATCH'])
def delete_doctor(id):
    try:
        response = DoctorServices.delete_doctor(id)
        cache.delete(f"doctor:profile:{id}")
        cache.delete(f"doctor:availability:{id}")
        cache.delete(f"doctor:slot:{response['data']['doctor_id']}")
        cache.delete(f"doctor:appointments:scheduled:{id}")
        cache.delete(f"doctor:appointments:past:{id}")
        cache.delete("admin:doctors")
        cache.delete(f"admin:department:{response['data']['department']['department_id']}")
        cache.delete("admin:departments")
        cache.delete("admin:summary")
        return jsonify(response),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/availability/<int:id>', methods=['GET'])
def read_availability(id):
    try:
        cache_key = f"doctor:availability:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = DoctorServices.read_availability(id)
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/availability/<int:id>', methods=['PUT'])
def update_availability(id):
    try:
        data = request.json
        response = DoctorServices.update_availability(id, data)
        cache.delete(f"doctor:availability:{id}")
        return jsonify(response),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/slot/<int:doctor_id>', methods=['GET'])
def read_slot(doctor_id):
    try:
        cache_key = f"doctor:slot:{doctor_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = DoctorServices.read_slot(doctor_id)
        cache.set(cache_key, data, timeout=60)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/appointments/scheduled/<int:id>', methods=['GET'])
def all_scheduled_appointments(id):
    try:
        cache_key = f"doctor:appointments:scheduled:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = DoctorServices.all_scheduled_appointments(id)
        cache.set(cache_key, data, timeout=300)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/appointments/past/<int:id>', methods=['GET'])
def all_past_appointments(id):
    try:
        cache_key = f"doctor:appointments:past:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = DoctorServices.all_past_appointments(id)
        cache.set(cache_key, data, timeout=300)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@doctor_bp.route('/treatment/<int:appointment_id>', methods=['POST'])
def create_treatment(appointment_id):
    try:
        data = request.json
        response = DoctorServices.create_treatment(appointment_id, data)
        cache.delete(f"doctor:slot:{response['data']['appointment']['doctor_id']}")
        cache.delete(f"doctor:appointments:scheduled:{response['doctor_user_id']}")
        cache.delete(f"doctor:appointments:past:{response['doctor_user_id']}")
        cache.delete(f"patient:appointments:scheduled:{response['patient_user_id']}")
        cache.delete(f"patient:appointments:past:{response['patient_user_id']}")
        cache.delete(f"patient:treatments:{response['patient_user_id']}")
        cache.delete("admin:appointments")
        cache.delete("admin:summary")
        return jsonify(response),201
    except (NotFoundError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500
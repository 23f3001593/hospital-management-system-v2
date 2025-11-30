from flask import Blueprint,jsonify,request
from core.extensions import cache
from core.services.patient_services import PatientServices
from core.utils.exceptions import ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError

patient_bp = Blueprint('patient_bp',__name__)

@patient_bp.route('', methods=['POST'])
def create_patient():
    try:
        data = request.json
        response = PatientServices.create_patient(data)
        cache.delete("admin:patients")
        cache.delete("admin:summary")
        return jsonify(response),201
    except (ValidationError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:id>', methods=['GET'])
def read_patient(id):
    try:
        cache_key = f"patient:profile:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = PatientServices.read_patient(id)
        cache.set(cache_key, data, timeout=600)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:id>', methods=['PUT'])
def update_patient(id):
    try:
        data = request.form.to_dict()
        file = request.files.get('profile_picture')
        response = PatientServices.update_patient(id, data, file)
        cache.delete(f"patient:profile:{id}")
        redis = cache.cache._write_client
        for id in response['doctor_user_ids']:
            for key in redis.scan_iter(f"doctor:appointments:scheduled:{id}"):
                redis.delete(key)
        cache.delete("admin:patients")
        return jsonify(response),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/<int:id>', methods=['PATCH'])
def delete_patient(id):
    try:
        response = PatientServices.delete_patient(id)
        cache.delete(f"patient:profile:{id}")
        cache.delete(f"patient:appointments:scheduled:{id}")
        cache.delete(f"patient:appointments:past:{id}")
        cache.delete(f"patient:treatments:{id}")
        cache.delete("admin:patients")
        cache.delete("admin:summary")
        return jsonify(response),200
    except (ValidationError,NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointment/<int:id>/<int:doctor_id>', methods=['POST'])
def create_appointment(id, doctor_id):
    try:
        data = request.json
        response = PatientServices.create_appointment(data, id, doctor_id)
        cache.delete(f"patient:appointments:scheduled:{id}")
        cache.delete(f"doctor:appointments:scheduled:{response['data']['doctor']['user']['id']}")
        cache.delete(f"doctor:slot:{doctor_id}")
        cache.delete("admin:appointments")
        cache.delete("admin:summary")
        return jsonify(response),201
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        data = request.json
        response = PatientServices.update_appointment(data, appointment_id)
        cache.delete(f"patient:appointments:scheduled:{response['data']['patient']['user']['id']}")
        cache.delete(f"doctor:appointments:scheduled:{response['data']['doctor']['user']['id']}")
        cache.delete(f"doctor:slot:{response['data']['doctor_id']}")
        cache.delete("admin:appointments")
        return jsonify(response),200
    except (ValidationError,NotFoundError,AlreadyExistError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointment/<int:appointment_id>', methods=['PATCH'])
def delete_appointment(appointment_id):
    try:
        response = PatientServices.delete_appointment(appointment_id)
        cache.delete(f"patient:appointments:scheduled:{response['data']['patient']['user']['id']}")
        cache.delete(f"patient:appointments:past:{response['data']['patient']['user']['id']}")
        cache.delete(f"doctor:appointments:scheduled:{response['data']['doctor']['user']['id']}")
        cache.delete(f"doctor:appointments:past:{response['data']['doctor']['user']['id']}")
        cache.delete(f"doctor:slot:{response['data']['doctor_id']}")
        cache.delete("admin:appointments")
        cache.delete("admin:summary")
        return jsonify(response),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointments/scheduled/<int:id>', methods=['GET'])
def all_scheduled_appointments(id):
    try:
        cache_key = f"patient:appointments:scheduled:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = PatientServices.all_scheduled_appointments(id)
        cache.set(cache_key, data, timeout=300)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/appointments/past/<int:id>', methods=['GET'])
def all_past_appointments(id):
    try:
        cache_key = f"patient:appointments:past:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = PatientServices.all_past_appointments(id)
        cache.set(cache_key, data, timeout=300)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/treatments/<int:id>', methods=['GET'])
def all_treatments(id):
    try:
        cache_key = f"patient:treatments:{id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return jsonify(cached_data),200
        data = PatientServices.all_treatments(id)
        cache.set(cache_key, data, timeout=300)
        return jsonify(data),200
    except (NotFoundError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@patient_bp.route('/treatments/export/<int:id>', methods=['POST'])
def all_treatments_export(id):
    from core.jobs.patient_jobs import send_treatments_history
    send_treatments_history.delay(id)
    return jsonify({"message":"Export started. You will receive an email shortly."}),202
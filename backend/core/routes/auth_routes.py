from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from core.services.auth_services import AuthServices
from core.utils.exceptions import ValidationError,NotFoundError,MissingFieldsError

auth_bp = Blueprint('auth_bp',__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = AuthServices.authenticate_user(data)
        access_token = create_access_token(identity=str(user['id']))
        refresh_token = create_refresh_token(identity=str(user['id']))
        return jsonify({"user":user, "access_token":access_token, "refresh_token":refresh_token}),200
    except (ValidationError,NotFoundError,MissingFieldsError) as e:
        return e.get_response()
    except Exception:
        return jsonify({"message":"Something went wrong. Please try again later."}),500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)
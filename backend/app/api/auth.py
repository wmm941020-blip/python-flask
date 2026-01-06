from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from . import api_bp
from ..models.user import User
from .utils import success_response, error_response

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return error_response("Invalid username or password", 401)
        
    if not user.is_active:
        return error_response("User is disabled", 403)
        
    access_token = create_access_token(identity=str(user.id))
    
    return success_response({
        'accessToken': access_token,
        'username': user.username,
        'roles': [role.code for role in user.roles]
    }, "Login successful")

@api_bp.route('/auth/info', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("User not found", 404)
        
    return success_response(user.to_dict())

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..models.user import User
from ..models.role import Role
from ..models.user import Position
from ..extensions import db
from .utils import success_response, error_response

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return success_response([u.to_dict() for u in users])

@api_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return error_response("Username already exists")
        
    user = User(
        username=data['username'],
        email=data.get('email'),
        phone=data.get('phone'),
        position_id=data.get('position_id'),
        is_active=data.get('is_active', True)
    )
    user.set_password(data['password'])
    
    if 'role_ids' in data:
        roles = Role.query.filter(Role.id.in_(data['role_ids'])).all()
        user.roles = roles
        
    db.session.add(user)
    db.session.commit()
    return success_response(user.to_dict())

@api_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.position_id = data.get('position_id', user.position_id)
    user.is_active = data.get('is_active', user.is_active)
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
        
    if 'role_ids' in data:
        roles = Role.query.filter(Role.id.in_(data['role_ids'])).all()
        user.roles = roles
        
    db.session.commit()
    return success_response(user.to_dict())

@api_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return success_response(message="User deleted")

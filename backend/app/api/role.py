from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..models.role import Role
from ..models.menu import Menu
from ..extensions import db
from .utils import success_response, error_response

@api_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    roles = Role.query.all()
    return success_response([r.to_dict() for r in roles])

@api_bp.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    data = request.get_json()
    if Role.query.filter_by(code=data['code']).first():
        return error_response("Role code already exists")
        
    role = Role(
        name=data['name'],
        code=data['code'],
        description=data.get('description')
    )
    
    if 'menu_ids' in data:
        menus = Menu.query.filter(Menu.id.in_(data['menu_ids'])).all()
        role.menus = menus
        
    db.session.add(role)
    db.session.commit()
    return success_response(role.to_dict())

@api_bp.route('/roles/<int:id>', methods=['PUT'])
@jwt_required()
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.get_json()
    
    role.name = data.get('name', role.name)
    role.code = data.get('code', role.code)
    role.description = data.get('description', role.description)
    
    if 'menu_ids' in data:
        menus = Menu.query.filter(Menu.id.in_(data['menu_ids'])).all()
        role.menus = menus
        
    db.session.commit()
    return success_response(role.to_dict())

@api_bp.route('/roles/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return success_response(message="Role deleted")

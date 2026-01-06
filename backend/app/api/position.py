from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..models.user import Position
from ..extensions import db
from .utils import success_response, error_response

@api_bp.route('/positions', methods=['GET'])
@jwt_required()
def get_positions():
    positions = Position.query.all()
    return success_response([p.to_dict() for p in positions])

@api_bp.route('/positions', methods=['POST'])
@jwt_required()
def create_position():
    data = request.get_json()
    if Position.query.filter((Position.name == data['name']) | (Position.code == data['code'])).first():
        return error_response("Position already exists")
        
    position = Position(name=data['name'], code=data['code'])
    db.session.add(position)
    db.session.commit()
    return success_response(position.to_dict())

@api_bp.route('/positions/<int:id>', methods=['PUT'])
@jwt_required()
def update_position(id):
    position = Position.query.get_or_404(id)
    data = request.get_json()
    
    position.name = data.get('name', position.name)
    position.code = data.get('code', position.code)
    
    db.session.commit()
    return success_response(position.to_dict())

@api_bp.route('/positions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_position(id):
    position = Position.query.get_or_404(id)
    db.session.delete(position)
    db.session.commit()
    return success_response(message="Position deleted")

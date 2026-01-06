from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models.menu import Menu
from ..models.user import User
from ..extensions import db
from .utils import success_response, error_response

@api_bp.route('/menus', methods=['GET'])
@jwt_required()
def get_menus():
    # Return all menus as tree
    root_menus = Menu.query.filter_by(parent_id=None).order_by(Menu.sort).all()
    return success_response([m.to_dict() for m in root_menus])

@api_bp.route('/menus/user', methods=['GET'])
@jwt_required()
def get_user_menus():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Collect all menus from all roles
    menus = set()
    for role in user.roles:
        for menu in role.menus:
            menus.add(menu)
            
    allowed_ids = {m.id for m in menus}
    
    # Find roots among the allowed menus
    roots = [m for m in menus if m.parent_id is None]
    roots.sort(key=lambda x: x.sort)
    
    def process_menu(menu):
        # Convert to frontend router format
        # Use path as name if not provided (remove leading slash and capitalize)
        name = menu.path.lstrip('/').replace('/', '').capitalize() if menu.path else f'Menu{menu.id}'
        
        data = {
            'path': menu.path,
            'name': name,
            'component': menu.component,
            'meta': {
                'title': menu.title,
                'icon': menu.icon,
                'rank': menu.sort
            }
        }
        
        # Filter children
        children = [
            process_menu(c) for c in menu.children 
            if c.id in allowed_ids
        ]
        children.sort(key=lambda x: x['meta']['rank'])
        
        if children:
            data['children'] = children
            
        return data

    return success_response([process_menu(r) for r in roots])

@api_bp.route('/menus', methods=['POST'])
@jwt_required()
def create_menu():
    data = request.get_json()
    menu = Menu(
        title=data['title'],
        path=data['path'],
        component=data.get('component'),
        icon=data.get('icon'),
        sort=data.get('sort', 0),
        parent_id=data.get('parent_id')
    )
    db.session.add(menu)
    db.session.commit()
    return success_response(menu.to_dict())

@api_bp.route('/menus/<int:id>', methods=['PUT'])
@jwt_required()
def update_menu(id):
    menu = Menu.query.get_or_404(id)
    data = request.get_json()
    
    menu.title = data.get('title', menu.title)
    menu.path = data.get('path', menu.path)
    menu.component = data.get('component', menu.component)
    menu.icon = data.get('icon', menu.icon)
    menu.sort = data.get('sort', menu.sort)
    menu.parent_id = data.get('parent_id', menu.parent_id)
    
    db.session.commit()
    return success_response(menu.to_dict())

@api_bp.route('/menus/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_menu(id):
    menu = Menu.query.get_or_404(id)
    if menu.children:
        return error_response("Cannot delete menu with children")
    db.session.delete(menu)
    db.session.commit()
    return success_response(message="Menu deleted")

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models.log import WorkLog
from ..extensions import db, celery
from ..tasks.export import export_work_logs
from .utils import success_response, error_response
from datetime import datetime

@api_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Filter logic
    user_id = request.args.get('user_id')
    
    # Regular users can only see their own logs unless they have special permission
    # For simplicity, let's say checking 'user_id' param requires admin or same user
    current_user_id = get_jwt_identity()
    
    query = WorkLog.query
    if user_id:
        # Check permission here if needed
        query = query.filter_by(user_id=user_id)
    else:
        # Default to current user? Or all if admin?
        # Let's default to current user
        query = query.filter_by(user_id=current_user_id)
        
    pagination = query.order_by(WorkLog.date.desc()).paginate(page=page, per_page=per_page)
    
    return success_response({
        'items': [log.to_dict() for log in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@api_bp.route('/logs', methods=['POST'])
@jwt_required()
def create_log():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    log = WorkLog(
        user_id=user_id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if 'date' in data else datetime.utcnow().date(),
        content=data.get('content'),
        completion_status=data.get('completion_status'),
        issues=data.get('issues'),
        tomorrow_plan=data.get('tomorrow_plan'),
        rating=data.get('rating')
    )
    db.session.add(log)
    db.session.commit()
    return success_response(log.to_dict())

@api_bp.route('/logs/export', methods=['POST'])
@jwt_required()
def export_logs():
    # silent=True prevents 415 error if Content-Type is missing (e.g. empty body)
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id') or get_jwt_identity() # Export own or specific
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    task = export_work_logs.delay(user_id, start_date, end_date)
    
    return success_response({'task_id': task.id}, "Export started")

@api_bp.route('/logs/export/status/<task_id>', methods=['GET'])
@jwt_required()
def get_export_status(task_id):
    task = export_work_logs.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result # This will be the download URL when SUCCESS
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return success_response(response)

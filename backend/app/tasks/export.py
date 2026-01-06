import os
from ..extensions import celery, db
from ..models.log import WorkLog
from ..models.user import User
import openpyxl
from datetime import datetime

@celery.task
def export_work_logs(user_id=None, start_date=None, end_date=None):
    # This task runs in the background
    # Ensure directory exists
    # Use path relative to this file to be safe regardless of CWD
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # backend/app
    export_dir = os.path.join(base_dir, 'static', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f'work_logs_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
    filepath = os.path.join(export_dir, filename)
    
    query = WorkLog.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    if start_date:
        query = query.filter(WorkLog.date >= start_date)
    if end_date:
        query = query.filter(WorkLog.date <= end_date)
        
    logs = query.all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Work Logs"
    
    # Header
    headers = ['ID', 'User', 'Date', 'Content', 'Status', 'Issues', 'Tomorrow Plan', 'Rating', 'Created At']
    ws.append(headers)
    
    for log in logs:
        ws.append([
            log.id,
            log.user.username,
            log.date,
            log.content,
            log.completion_status,
            log.issues,
            log.tomorrow_plan,
            log.rating,
            log.created_at
        ])
        
    wb.save(filepath)
    
    # Return relative path for download
    return f'/static/exports/{filename}'

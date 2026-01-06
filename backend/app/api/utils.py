from flask import jsonify

def success_response(data=None, message="Success"):
    return jsonify({
        'code': 200,
        'data': data,
        'message': message,
        'success': True
    })

def error_response(message="Error", code=400):
    return jsonify({
        'code': code,
        'data': None,
        'message': message,
        'success': False
    }), code

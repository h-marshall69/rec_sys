from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__, url_prefix='/info')

@users_bp.route('/usuario/<int:user_id>', methods=['GET'])
def user_info(user_id):
    from api.app import user_service
    
    result = user_service.get_user_info(user_id)
    return jsonify(result), 200 if 'error' not in result else 404

@users_bp.route('/stats', methods=['GET'])
def stats():
    from api.app import user_service
    
    return jsonify(user_service.get_statistics())
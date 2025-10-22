from flask import Blueprint, jsonify

isbm_bp = Blueprint('isbm', __name__, url_prefix='/isbm')

@isbm_bp.route('/imagen', methods=['GET'])
def isbm_info():
    from api.app import data
    print("Hola desde nose")
    
    # return jsonify(data.users), 200
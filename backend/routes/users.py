from flask import Blueprint, request, jsonify
import pandas as pd

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def set_users():
    """
    Endpoint para que un usuario guarde sus géneros de películas preferidos
    Body esperado:
    {
        "user_id": "123",
        "selected_genres": ["Action", "Comedy", "Drama"]
    }
    """
    try:

        data = request.get_json()

        if not data or 'user_id' not in data or 'selected_genres' not in data:
            return jsonify({'error': 'Faltan campos requeridos: user_id y selected_genres'}), 400

        if not isinstance(data['selected_genres'], list):
            return jsonify({'error': 'El campo "selected_genres" debe ser una lista'}), 400

        # Aquí podrías guardar los datos en una base de datos o archivo
        print(f"Usuario: {data['user_id']}, Géneros: {data['selected_genres']}")

        return jsonify({
            'mensaje': 'Preferencias guardadas correctamente',
            'user_id': data['user_id'],
            'genres': data['selected_genres']
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error procesando la solicitud: {str(e)}'}), 500

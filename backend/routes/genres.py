from flask import Blueprint, jsonify
import pandas as pd

genres_bp = Blueprint('genres', __name__)

@genres_bp.route('/genres', methods=['GET'])
def get_genres():
    """
    Endpoint que retorna los géneros desde el archivo CSV guardado
    """
    try:
        # Cargar desde el CSV previamente guardado
        genres_df = pd.read_csv('data/genres.csv')
        
        generos_lista = genres_df['genre'].tolist()
        
        return jsonify({
            'all_genres': len(generos_lista),
            'genres': generos_lista
        })
            
    except Exception as e:
        return jsonify({'error': f'Error cargando géneros desde data/genres.csv: {str(e)}'}), 500

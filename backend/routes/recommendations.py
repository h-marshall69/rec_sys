from flask import Blueprint, request, jsonify
import pandas as pd

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """
    Endpoint para obtener recomendaciones de películas basadas en géneros preferidos
    Body esperado:
    {
        "user_id": "123",
        "selected_genres": ["Action", "Comedy", "Drama"],
        "limit": 10  # opcional, número de recomendaciones
    }
    """
    try:
        # Cargar datasets
        movies_df = pd.read_csv('data/movies.csv')
        ratings_df = pd.read_csv('data/ratings.csv') 
        
        data = request.get_json()

        if not data or 'user_id' not in data or 'selected_genres' not in data:
            return jsonify({'error': 'Faltan campos requeridos: user_id y selected_genres'}), 400

        user_id = data['user_id']
        selected_genres = data['selected_genres']
        limit = data.get('limit', 10)

        if not isinstance(selected_genres, list):
            return jsonify({'error': 'El campo "selected_genres" debe ser una lista'}), 400

        # Calcular rating promedio por película
        movie_ratings = ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_ratings.columns = ['movieId', 'avg_rating', 'rating_count']
        
        # Combinar con información de películas
        movies_with_ratings = pd.merge(movies_df, movie_ratings, on='movieId')
        
        # Filtrar películas que tengan al menos 10 ratings para mayor confiabilidad
        movies_with_ratings = movies_with_ratings[movies_with_ratings['rating_count'] >= 10]
        
        # Función para verificar si una película contiene al menos uno de los géneros seleccionados
        def matches_genres(movie_genres, selected_genres):
            movie_genres_list = movie_genres.split('|')
            return any(genre in movie_genres_list for genre in selected_genres)
        
        # Filtrar películas que coincidan con los géneros seleccionados
        genre_matches = movies_with_ratings[
            movies_with_ratings['genres'].apply(
                lambda x: matches_genres(x, selected_genres)
            )
        ]
        
        if genre_matches.empty:
            return jsonify({
                'message': 'No se encontraron películas que coincidan con los géneros seleccionados',
                'user_id': user_id,
                'selected_genres': selected_genres,
                'recommendations': []
            }), 200
        
        # Ordenar por rating promedio (de mayor a menor) y luego por cantidad de ratings
        recommendations = genre_matches.sort_values(
            ['avg_rating', 'rating_count'], 
            ascending=[False, False]
        ).head(limit)
        
        # Formatear respuesta
        recommendations_list = []
        for _, movie in recommendations.iterrows():
            recommendations_list.append({
                'movieId': int(movie['movieId']),
                'title': movie['title'],
                'genres': movie['genres'],
                'avg_rating': round(float(movie['avg_rating']), 2),
                'rating_count': int(movie['rating_count'])
            })
        
        print(recommendations_list)
        return jsonify({
            'message': f'Recomendaciones basadas en tus generos preferidos',
            'user_id': user_id,
            'selected_genres': selected_genres,
            'total_recommendations': len(recommendations_list),
            'recommendations': recommendations_list
        }), 200

    except FileNotFoundError as e:
        return jsonify({'error': f'Archivo de datos no encontrado: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error procesando la solicitud: {str(e)}'}), 500
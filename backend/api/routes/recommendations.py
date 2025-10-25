# api\routes\recommendations.py
from flask import Blueprint, request, jsonify
import pandas as pd

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/recomendaciones')

@recommendations_bp.route('/usuario/<int:user_id>', methods=['GET'])
def user_recommendations(user_id):
    """
    GET /recomendaciones/usuario/123?k=5
    Recomendaciones colaborativas para un usuario
    """
    from api.app import recommender, cache
    
    k = request.args.get('k', 5, type=int)
    cache_key = f"rec_user_{user_id}_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    result = recommender.collaborative_filtering(user_id, k)
    
    # Si hay error, no cachear
    if "error" in result:
        return jsonify(result), 404 if result["error"] == "cold_start" else 500
    
    cache.set(cache_key, result)
    return jsonify(result)

@recommendations_bp.route('/buscar/titulo', methods=['GET']) # Falta autor ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def book_recommendations():
    """
    GET /recomendaciones/libro?titulo=harry%20potter&k=5
    Recomendaciones basadas en contenido (título + autor)
    """
    from api.app import recommender, cache
    
    titulo = request.args.get('titulo', '', type=str)
    if not titulo:
        return jsonify({"error": "missing_parameter", "mensaje": "Parámetro 'titulo' requerido"}), 400
    
    k = request.args.get('k', 5, type=int)
    cache_key = f"rec_book_{titulo.lower()}_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    result = recommender.content_based(titulo, k)
    
    # Si hay error, no cachear
    if "error" in result:
        return jsonify(result), 404
    
    cache.set(cache_key, result)
    return jsonify(result)

@recommendations_bp.route('/popular', methods=['GET'])
def popular():
    """
    GET /recomendaciones/popular?k=10
    Libros más populares por número de ratings
    """
    from api.app import recommender, cache
    
    k = request.args.get('k', 10, type=int)
    cache_key = f"rec_popular_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    result = recommender.popular(k)
    cache.set(cache_key, result)
    return jsonify(result)

# ============================================================
# NUEVAS RUTAS: Búsqueda avanzada por título
# ============================================================

@recommendations_bp.route('/libro', methods=['GET'])
def search_by_title():
    """
    GET /recomendaciones/buscar/titulo?q=harry&metodo=tfidf&k=10&threshold=0.3
    
    Búsqueda avanzada de libros por título
    
    Parámetros:
    - q: query de búsqueda (requerido)
    - metodo: 'tfidf', 'fuzzy', 'hybrid' (default: 'hybrid')
    - k: número de resultados (default: 10)
    - threshold: umbral de similaridad 0-1 (default: 0.3)
    """
    from api.app import recommender, cache
    
    query = request.args.get('q', '', type=str)
    if not query:
        return jsonify({
            "error": "missing_parameter", 
            "mensaje": "Parámetro 'q' (query) requerido"
        }), 400
    
    k = request.args.get('k', 10, type=int)
    
    
    cache_key = f"search_{query.lower()}_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    
    
    try:
        results = recommender.find_books_by_hybrid(query, k)
        # Convertir DataFrame a dict
        if results.empty:
            response = {
                "query": query,
                "total_resultados": 0,
                "resultados": []
            }
        else:
            response = {
                "query": query,
                "total_resultados": len(results),
                "resultados": results.to_dict('records')
            }
        
        cache.set(cache_key, response)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "error": "search_error",
            "mensaje": str(e)
        }), 500
    
@recommendations_bp.route('/buscar/rapido', methods=['GET'])
def quick_search():
    """
    GET /recomendaciones/buscar/rapido?q=harry
    
    Búsqueda rápida con configuración optimizada
    Usa método híbrido con parámetros balanceados
    """
    from api.app import recommender, cache
    
    query = request.args.get('q', '', type=str)
    if not query:
        return jsonify({
            "error": "missing_parameter",
            "mensaje": "Parámetro 'q' requerido"
        }), 400
    
    cache_key = f"quick_search_{query.lower()}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    try:
        # Búsqueda optimizada: híbrido, top 5, threshold moderado
        results = recommender.find_books_by_hybrid(query, k=10, threshold=0.7)
        
        if results.empty:
            response = {
                "query": query,
                "encontrados": False,
                "resultados": []
            }
        else:
            response = {
                "query": query,
                "encontrados": True,
                "resultados": results.to_dict('records')
            }
        
        cache.set(cache_key, response)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "error": "search_error",
            "mensaje": str(e)
        }), 500
    
# ============================================================
# RUTA DE ESTADÍSTICAS
# ============================================================

@recommendations_bp.route('/stats', methods=['GET'])
def stats():
    """
    GET /recomendaciones/stats
    
    Estadísticas del sistema de recomendación
    """
    from api.app import recommender
    
    try:
        stats_data = {
            "total_usuarios": len(recommender.user_item_matrix.index) if recommender.user_item_matrix is not None else 0,
            "total_libros": len(recommender.data.books),
            "total_ratings": len(recommender.data.ratings),
            "matriz_usuario_item_shape": list(recommender.user_item_matrix.shape) if recommender.user_item_matrix is not None else None,
            "matriz_tfidf_shape": list(recommender.tfidf_matrix.shape) if recommender.tfidf_matrix is not None else None,
            "vocabulario_size": len(recommender.tfidf_vectorizer.vocabulary_) if recommender.tfidf_vectorizer is not None else 0
        }
        return jsonify(stats_data)
    except Exception as e:
        return jsonify({
            "error": "stats_error",
            "mensaje": str(e)
        }), 500
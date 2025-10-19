from flask import Blueprint, request, jsonify
import pandas as pd

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/recomendaciones')

@recommendations_bp.route('/usuario/<int:user_id>', methods=['GET'])
def user_recommendations(user_id):
    from api.app import recommender, cache
    
    k = request.args.get('k', 5, type=int)
    cache_key = f"rec_user_{user_id}_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    result = recommender.collaborative_filtering(user_id, k)
    cache.set(cache_key, result)
    return jsonify(result)

@recommendations_bp.route('/libro', methods=['GET'])
def book_recommendations():
    from api.app import recommender, cache
    
    titulo = request.args.get('titulo', '', type=str)
    if not titulo:
        return jsonify({"error": "missing_parameter"}), 400
    
    k = request.args.get('k', 5, type=int)
    cache_key = f"rec_book_{titulo}_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    result = recommender.content_based(titulo, k)
    cache.set(cache_key, result)
    return jsonify(result)

@recommendations_bp.route('/popular', methods=['GET'])
def popular():
    from api.app import recommender, cache
    
    k = request.args.get('k', 10, type=int)
    cache_key = f"rec_popular_{k}"
    
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)
    
    result = recommender.popular(k)
    cache.set(cache_key, result)
    return jsonify(result)
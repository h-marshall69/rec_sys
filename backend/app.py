from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import warnings
import re
import pickle
import os
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import lru_cache
import logging

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== CARGAR DATOS =====================
class DataLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.load_data()
        self._initialized = True
    
    def load_data(self):
        try:
            self.users = pd.read_parquet('./users_prep.parquet.gzip')
            self.books = pd.read_parquet('./books_prep.parquet.gzip')
            self.ratings = pd.read_parquet('./ratings_prep.parquet.gzip')
            logger.info("Datos cargados exitosamente")
        except Exception as e:
            logger.error(f"Error cargando datos: {e}")
            raise

# ===================== COLLABORATIVE FILTERING =====================
class UserBasedCollaborativeFiltering:
    def __init__(self, users, books, ratings, k=10):
        self.users = users.reset_index(drop=True)
        self.books = books
        self.ratings = ratings.reset_index(drop=True)
        self.k = k
        self.normalized_ratings = None
    
    def normalize(self, dataframe):
        row_sum = dataframe.sum(axis=1)
        non_zero = dataframe.astype(bool).sum(axis=1)
        self.dataframe_mean = row_sum / non_zero
        self.normalized_ratings = dataframe.subtract(self.dataframe_mean, axis=0)
    
    @staticmethod
    def compute_similarity(x, y):
        norm_x = np.linalg.norm(x)
        norm_y = np.linalg.norm(y)
        if norm_x == 0 or norm_y == 0:
            return 0
        return np.dot(x, y) / (norm_x * norm_y)
    
    def get_neighbors(self, user_id, similarity_matrix):
        try:
            user_index = self.users[self.users['User-ID'] == user_id].index[0]
        except IndexError:
            return None
        
        similarities = similarity_matrix.iloc[user_index].values
        neighbor_indices = similarities.argsort()[-(self.k + 1):][::-1]
        
        if user_index in neighbor_indices:
            neighbor_indices = neighbor_indices[neighbor_indices != user_index][:self.k]
        else:
            neighbor_indices = neighbor_indices[:self.k]
        
        return neighbor_indices
    
    def recommend(self, user_id):
        try:
            user_index = self.users[self.users['User-ID'] == user_id].index[0]
        except IndexError:
            return pd.DataFrame()
        
        user_ratings = self.ratings.iloc[user_index]
        unrated_isbns = [isbn for isbn, rating in user_ratings.items() if rating == 0]
        
        if not unrated_isbns:
            return pd.DataFrame()
        
        self.normalize(self.ratings)
        
        # Crear matriz de similitud de forma eficiente
        similarity_scores = []
        for i in range(len(self.users)):
            sim = self.compute_similarity(
                self.normalized_ratings.iloc[user_index].values,
                self.normalized_ratings.iloc[i].values
            )
            similarity_scores.append(sim)
        
        neighbor_indices = self.get_neighbors(user_id, pd.Series(similarity_scores))
        
        if neighbor_indices is None or len(neighbor_indices) == 0:
            return pd.DataFrame()
        
        # Calcular scores
        scores = {}
        for isbn in unrated_isbns:
            neighbor_ratings = self.ratings.loc[neighbor_indices, isbn].values
            neighbor_sims = [similarity_scores[i] for i in neighbor_indices]
            
            if np.sum(np.abs(neighbor_sims)) > 0:
                score = np.dot(neighbor_sims, neighbor_ratings) / np.sum(np.abs(neighbor_sims))
                scores[isbn] = score
        
        top_isbns = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.k]
        top_isbns = [isbn for isbn, _ in top_isbns]
        
        return self.books[self.books['ISBN'].isin(top_isbns)]

# ===================== CONTENT-BASED FILTERING =====================
class ContentBasedFiltering:
    def __init__(self, books, ratings, k=10):
        self.books = self._prepare_data(books, ratings)
        self.k = k
        self.tfidf_matrix = None
        self.sigmoid_matrix = None
        self.indices = None
        self._build_embeddings()
    
    def _prepare_data(self, books, ratings):
        rated_books = books[books['ISBN'].isin(ratings['ISBN'].unique())]
        rated_books = rated_books.drop_duplicates(subset=['Book-Title'], keep=False)
        
        popular_isbn = ratings['ISBN'].value_counts()
        popular_isbn = popular_isbn[popular_isbn >= 2].index.tolist()
        
        popular_books = rated_books[rated_books['ISBN'].isin(popular_isbn)].copy()
        popular_books['title_clean'] = popular_books['Book-Title'].apply(
            lambda x: re.sub('[^a-z0-9 ]', '', x.lower()).strip()
        )
        return popular_books.reset_index(drop=True)
    
    def _build_embeddings(self):
        tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
        self.tfidf_matrix = tfidf.fit_transform(self.books['title_clean'].fillna(''))
        self.sigmoid_matrix = sigmoid_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.books.index, index=self.books['Book-Title']).drop_duplicates()
    
    def recommend(self, book_title):
        try:
            idx = self.indices[book_title]
        except KeyError:
            return pd.DataFrame()
        
        scores = enumerate(self.sigmoid_matrix[idx])
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:self.k + 1]
        indices = [i[0] for i in scores]
        
        return self.books.iloc[indices][['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication']]

# ===================== MODELO HÍBRIDO =====================
class HybridRecommender:
    def __init__(self, users, books, ratings, k=10, weights=None):
        self.users = users
        self.books = books
        self.ratings = ratings
        self.k = k
        self.weights = weights or {'user_cf': 0.4, 'content_based': 0.6}
        
        self.user_cf = UserBasedCollaborativeFiltering(users, books, ratings, k)
        self.content_based = ContentBasedFiltering(books, ratings, k)
    
    def recommend(self, user_id):
        recommendations = {}
        
        # Collaborative Filtering
        cf_recs = self.user_cf.recommend(user_id)
        for isbn in cf_recs['ISBN']:
            recommendations[isbn] = self.weights['user_cf']
        
        # Content-based: obtener un libro que el usuario haya calificado bien
        try:
            user_idx = self.users[self.users['User-ID'] == user_id].index[0]
            user_ratings = self.ratings.iloc[user_idx]
            rated_books = user_ratings[user_ratings > 3].index
            
            if len(rated_books) > 0:
                similar_books = self.content_based.recommend(
                    self.books[self.books['ISBN'] == rated_books[0]]['Book-Title'].values[0]
                )
                for isbn in similar_books['ISBN']:
                    recommendations[isbn] = recommendations.get(isbn, 0) + self.weights['content_based']
        except:
            pass
        
        # Ordenar y retornar top-k
        top_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:self.k]
        isbns = [isbn for isbn, _ in top_recs]
        
        return self.books[self.books['ISBN'].isin(isbns)]

# ===================== INICIALIZAR COMPONENTES =====================
data_loader = DataLoader()
hybrid_recommender = HybridRecommender(
    data_loader.users,
    data_loader.books,
    data_loader.ratings,
    k=10
)

# ===================== RUTAS API =====================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/recommendations/hybrid', methods=['POST'])
def get_hybrid_recommendations():
    """Obtener recomendaciones usando modelo híbrido"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        k = data.get('k', 10)
        
        if not user_id:
            return jsonify({'error': 'user_id es requerido'}), 400
        
        hybrid_recommender.k = k
        recommendations = hybrid_recommender.recommend(user_id)
        
        if recommendations.empty:
            return jsonify({'recommendations': [], 'count': 0}), 200
        
        result = recommendations[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication']].to_dict('records')
        return jsonify({'recommendations': result, 'count': len(result)}), 200
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/collaborative', methods=['POST'])
def get_collaborative_recommendations():
    """Obtener recomendaciones usando Collaborative Filtering"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        k = data.get('k', 10)
        
        if not user_id:
            return jsonify({'error': 'user_id es requerido'}), 400
        
        cf = UserBasedCollaborativeFiltering(
            data_loader.users,
            data_loader.books,
            data_loader.ratings,
            k
        )
        recommendations = cf.recommend(user_id)
        
        if recommendations.empty:
            return jsonify({'recommendations': [], 'count': 0}), 200
        
        result = recommendations[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication']].to_dict('records')
        return jsonify({'recommendations': result, 'count': len(result)}), 200
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/content-based', methods=['POST'])
def get_content_based_recommendations():
    """Obtener recomendaciones usando Content-Based Filtering"""
    try:
        data = request.get_json()
        book_title = data.get('book_title')
        k = data.get('k', 10)
        
        if not book_title:
            return jsonify({'error': 'book_title es requerido'}), 400
        
        cb = ContentBasedFiltering(data_loader.books, data_loader.ratings, k)
        recommendations = cb.recommend(book_title)
        
        if recommendations.empty:
            return jsonify({'recommendations': [], 'count': 0}), 200
        
        result = recommendations.to_dict('records')
        return jsonify({'recommendations': result, 'count': len(result)}), 200
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    """Obtener información del usuario"""
    try:
        user = data_loader.users[data_loader.users['User-ID'] == user_id]
        if user.empty:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        result = user.to_dict('records')[0]
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<isbn>', methods=['GET'])
def get_book_info(isbn):
    """Obtener información del libro"""
    try:
        book = data_loader.books[data_loader.books['ISBN'] == isbn]
        if book.empty:
            return jsonify({'error': 'Libro no encontrado'}), 404
        
        result = book.to_dict('records')[0]
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas del sistema"""
    return jsonify({
        'total_users': len(data_loader.users),
        'total_books': len(data_loader.books),
        'total_ratings': len(data_loader.ratings),
        'avg_rating': float(data_loader.ratings['Book-Rating'].mean())
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
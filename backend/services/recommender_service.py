# services\recommender_service.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
from utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

class RecommenderService:
    """Lógica centralizada de recomendaciones"""
    
    def __init__(self, data_service):
        self.data = data_service
        self.user_item_matrix = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.title_tfidf_matrix = None
        self.title_vectorizer = None
    
    def build_matrices(self):
        """Construye matrices para los algoritmos"""
        try:
            # Matriz usuario-item
            self.user_item_matrix = self.data.ratings.pivot_table(
                index='User-ID',
                columns='ISBN',
                values='Book-Rating',
                fill_value=0
            )
            logger.info(f"✓ Matriz usuario-item: {self.user_item_matrix.shape}")
            
            # Matriz TF-IDF para content-based
            self._build_tfidf_matrix()

            # Matriz TF-IDF solo para títulos (búsqueda mejorada)
            self._build_title_tfidf_matrix()

        except Exception as e:
            logger.error(f"✗ Error construyendo matrices: {e}")
            raise
    
    def _build_tfidf_matrix(self):
        """Construye matriz TF-IDF para búsqueda por contenido"""
        features = (
            self.data.books['Book-Title'].fillna('') + ' ' +
            self.data.books['Book-Author'].fillna('')
        ).apply(lambda x: x.lower())
        
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=500
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(features)
        logger.info(f"✓ Matriz TF-IDF contenido: {self.tfidf_matrix.shape}")

    def _build_title_tfidf_matrix(self):
        """Construye matriz TF-IDF solo para títulos (búsqueda por nombre)"""
        titles = self.data.books['Book-Title'].fillna('').apply(lambda x: x.lower())
        
        self.title_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=300,
            ngram_range=(1, 2)  # Considera bigramas para mejor matching
        )
        self.title_tfidf_matrix = self.title_vectorizer.fit_transform(titles)
        logger.info(f"✓ Matriz TF-IDF títulos: {self.title_tfidf_matrix.shape}")

    def find_books_by_tfidf(self, query_title, k=10, threshold=0.3):
        """Búsqueda usando TF-IDF y cosine similarity"""
        # Transformar query
        query_vector = self.title_vectorizer.transform([query_title])
        
        # Calcular similaridades
        similarities = cosine_similarity(query_vector, self.title_tfidf_matrix).flatten()
        
        # Filtrar por umbral
        valid_indices = np.where(similarities >= threshold)[0]
        
        if len(valid_indices) == 0:
            logger.warning(f"No se encontraron libros con similaridad >= {threshold}")
            return pd.DataFrame()
        
        # Ordenar y obtener top k
        top_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]][:k]
        
        # Crear resultado
        results = self.data.books.iloc[top_indices].copy()
        results['similarity_score'] = similarities[top_indices]
        results['match_method'] = 'tfidf'
        
        return results[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 
                       'Image-URL-M', 'similarity_score', 'match_method']]
    

    def find_books_by_fuzzy(self, query_title, k=10, threshold=0.3):
        """Búsqueda usando SequenceMatcher (fuzzy string matching)"""
        titles = self.data.books['Book-Title'].fillna('').apply(lambda x: x.lower())
        
        # Calcular similaridad con cada título
        similarities = titles.apply(
            lambda title: SequenceMatcher(None, query_title, title).ratio()
        ).values
        
        # Filtrar por umbral
        valid_indices = np.where(similarities >= threshold)[0]
        
        if len(valid_indices) == 0:
            logger.warning(f"No se encontraron libros con similaridad >= {threshold}")
            return pd.DataFrame()
        
        # Ordenar y obtener top k
        top_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]][:k]
        
        # Crear resultado
        results = self.data.books.iloc[top_indices].copy()
        results['similarity_score'] = similarities[top_indices]
        results['match_method'] = 'fuzzy'
        
        return results[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 
                       'Image-URL-M', 'similarity_score', 'match_method']]
    
    def find_books_by_hybrid(self, query_title, k=10, threshold=0.3):
        """Combina TF-IDF y Fuzzy matching"""
        # Obtener resultados de ambos métodos
        tfidf_results = self.find_books_by_tfidf(query_title, k*2, threshold*0.7)
        fuzzy_results = self.find_books_by_fuzzy(query_title, k*2, threshold*0.7)
        
        # Combinar y normalizar scores
        combined = pd.concat([tfidf_results, fuzzy_results])
        
        if combined.empty:
            return pd.DataFrame()
        
        # Agrupar por ISBN y promediar scores
        combined = combined.groupby('ISBN').agg({
            'Book-Title': 'first',
            'Book-Author': 'first',
            'Year-Of-Publication': 'first',
            'Image-URL-M': 'first',
            'similarity_score': 'mean'  # Promedio de ambos métodos
        }).reset_index()
        
        combined['match_method'] = 'hybrid'
        
        # Ordenar y retornar top k
        combined = combined.sort_values('similarity_score', ascending=False).head(k)
        
        return combined[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 
                        'Image-URL-M', 'similarity_score', 'match_method']]

        
    def collaborative_filtering(self, user_id, k=5):
        """Recomendación colaborativa"""
        if user_id not in self.user_item_matrix.index:
            return {"error": "cold_start", "mensaje": f"Usuario {user_id} no encontrado"}
        
        user_ratings = self.user_item_matrix.loc[user_id]
        similarities = cosine_similarity(
            self.user_item_matrix,
            user_ratings.values.reshape(1, -1)
        ).flatten()
        
        similar_users = self.user_item_matrix.index[
            (similarities > 0.1) & (similarities < 0.99)
        ].tolist()
        
        if not similar_users:
            return {"error": "no_similar_users"}
        
        top_similar_idx = np.argsort(similarities)[-10:][::-1]
        top_similar_users = self.user_item_matrix.index[top_similar_idx].tolist()
        
        recommendations = {}
        for sim_user in top_similar_users:
            sim_user_ratings = self.user_item_matrix.loc[sim_user]
            unrated_books = sim_user_ratings[sim_user_ratings > 0][user_ratings == 0]
            
            for isbn, rating in unrated_books.items():
                recommendations[isbn] = recommendations.get(isbn, 0) + rating
        
        top_books = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:k]
        return self._format_response(top_books)
    
    def content_based_m(self, book_title, k=5):
        """Recomendación basada en contenido"""
        matching = self.data.books[
            self.data.books['Book-Title'].str.contains(book_title, case=False, na=False)
        ]
        
        if matching.empty:
            return {"error": "book_not_found"}
        
        book_idx = matching.index[0]
        similarity = cosine_similarity(
            self.tfidf_matrix[book_idx],
            self.tfidf_matrix
        ).flatten()
        
        similar_idx = np.argsort(similarity)[-k-1:-1][::-1]
        recommendations = self.data.books.iloc[similar_idx][
            ['ISBN', 'Book-Title', 'Book-Author', "Image-URL-M"]
        ]
        
        return {
            "metodo": "content_based",
            "libro_consulta": book_title,
            "recomendaciones": recommendations.to_dict('records')
        }
    
    def content_based(self, book_title, k=5):
        """Recomendación basada en contenido (título + autor)"""
        # Primero buscar el libro
        matching = self.find_books_by_hybrid(book_title, k)
        
        if matching.empty:
            return {"error": "book_not_found", "query": book_title}
        
        book_idx = self.data.books[
            self.data.books['ISBN'] == matching.iloc[0]['ISBN']
        ].index[0]
        
        # Calcular similaridad usando contenido (título + autor)
        similarity = cosine_similarity(
            self.tfidf_matrix[book_idx],
            self.tfidf_matrix
        ).flatten()
        
        # Excluir el mismo libro
        similarity[book_idx] = -1
        
        similar_idx = np.argsort(similarity)[-k:][::-1]
        recommendations = self.data.books.iloc[similar_idx][
            ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Image-URL-M']
        ].copy()
        
        recommendations['similarity_score'] = similarity[similar_idx]
        
        return {
            "metodo": "content_based",
            "libro_consulta": matching.iloc[0]['Book-Title'],
            "isbn_consulta": matching.iloc[0]['ISBN'],
            "recomendaciones": recommendations.to_dict('records')
        }
    
    def popular(self, k=5):
        """Libros más populares"""
        popular_books = self.data.ratings['ISBN'].value_counts().head(k).index
        recommendations = self.data.books[
            self.data.books['ISBN'].isin(popular_books)
        ][['ISBN', 'Book-Title', 'Book-Author', "Image-URL-M"]]
        
        return {
            "metodo": "popularity",
            "recomendaciones": recommendations.to_dict('records')
        }
    
    def _format_response(self, books_list):
        """Formatea respuesta con detalles"""
        resultado = []
        for isbn, score in books_list:
            book = self.data.books[self.data.books['ISBN'] == isbn]
            if not book.empty:
                resultado.append({
                    "isbn": isbn,
                    "titulo": book['Book-Title'].values[0],
                    "autor": book['Book-Author'].values[0],
                    "score": float(score)
                })
        return {"metodo": "collaborative_filtering", "recomendaciones": resultado}
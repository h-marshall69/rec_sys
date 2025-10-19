# services/recommendation_service.py
from models.collaborative import CollaborativeFiltering
from models.content_based import ContentBased
from models.popularity import Popularity
from cache.redis_cache import RedisCache

class RecommendationService:
    def __init__(self, users, books, ratings):
        self.users = users
        self.books = books
        self.ratings = ratings
        
        # Inicializar modelos
        self.collaborative = CollaborativeFiltering(self._build_matrix())
        self.content_based = ContentBased(self.books)
        self.popularity = Popularity(self.ratings, self.books)
        
        self.cache = RedisCache()
    
    def _build_matrix(self):
        return self.ratings.pivot_table(
            index='User-ID',
            columns='ISBN',
            values='Book-Rating',
            fill_value=0
        )
    
    def get_for_user(self, user_id, k=5):
        cache_key = f"user_recommendations:{user_id}:{k}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        result = self.collaborative.recommend(user_id, k)
        self.cache.set(cache_key, result, ttl=3600)
        return result
    
    def get_for_book(self, title, k=5):
        cache_key = f"book_recommendations:{title}:{k}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        result = self.content_based.recommend(title, k)
        self.cache.set(cache_key, result, ttl=3600)
        return result
    
    def get_popular(self, k=5):
        cache_key = f"popular_recommendations:{k}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        result = self.popularity.recommend(k)
        self.cache.set(cache_key, result, ttl=86400)  # 24h
        return result
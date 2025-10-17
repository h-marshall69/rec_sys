# config.py - Configuración centralizada
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    DEBUG = False
    TESTING = False
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False
    
    # API
    API_TITLE = 'Book Recommender API'
    API_VERSION = '1.0.0'
    
    # Datos
    DATA_PATH = os.getenv('DATA_PATH', './')
    PARQUET_USERS = os.path.join(DATA_PATH, 'users_prep.parquet.gzip')
    PARQUET_BOOKS = os.path.join(DATA_PATH, 'books_prep.parquet.gzip')
    PARQUET_RATINGS = os.path.join(DATA_PATH, 'ratings_prep.parquet.gzip')
    
    # Modelos
    DEFAULT_K = 10
    MAX_K = 100
    MIN_K = 1
    
    # Collaborative Filtering
    CF_K_NEIGHBORS = int(os.getenv('CF_K_NEIGHBORS', 10))
    
    # Pesos del modelo híbrido
    HYBRID_WEIGHTS = {
        'user_cf': float(os.getenv('HYBRID_CF_WEIGHT', 0.4)),
        'content_based': float(os.getenv('HYBRID_CB_WEIGHT', 0.6))
    }
    
    # Cache
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True') == 'True'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hora
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True') == 'True'
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '200 per day, 50 per hour')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    TESTING = True
    CACHE_ENABLED = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
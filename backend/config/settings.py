import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Rutas de datos
    DATA_PATH = os.getenv('DATA_PATH', './data')
    USERS_FILE = os.path.join(DATA_PATH, 'users_prep.parquet.gzip')
    BOOKS_FILE = os.path.join(DATA_PATH, 'books_prep.parquet.gzip')
    RATINGS_FILE = os.path.join(DATA_PATH, 'ratings_prep.parquet.gzip')
    
    # Parámetros de filtrado
    MIN_BOOK_RATINGS = int(os.getenv('MIN_BOOK_RATINGS', 3))
    MIN_USER_RATINGS = int(os.getenv('MIN_USER_RATINGS', 5))
    
    # Caché
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True') == 'True'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hora
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
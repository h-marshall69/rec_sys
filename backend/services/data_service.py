import pandas as pd
from config.settings import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class DataService:
    """Gestiona la carga y preparación de datos"""
    
    _instance = None  # Singleton para evitar cargar datos múltiples veces
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.users = None
        self.books = None
        self.ratings = None
        self.load_data()
        self._initialized = True
    
    def load_data(self):
        """Carga datos con manejo de errores"""
        try:
            self.users = pd.read_parquet(Config.USERS_FILE)
            self.books = pd.read_parquet(Config.BOOKS_FILE)
            self.ratings = pd.read_parquet(Config.RATINGS_FILE)
            
            logger.info(f"✓ Ratings: {self.ratings.shape}")
            logger.info(f"✓ Users: {self.users.shape}")
            logger.info(f"✓ Books: {self.books.shape}")
        except Exception as e:
            logger.error(f"✗ Error cargando datos: {e}")
            raise
    
    def prepare_data(self):
        """Prepara datos con filtrado inteligente"""
        try:
            # Filtrar libros con mínimo de ratings
            book_counts = self.ratings['ISBN'].value_counts()
            popular_books = book_counts[
                book_counts >= Config.MIN_BOOK_RATINGS
            ].index
            self.ratings = self.ratings[self.ratings['ISBN'].isin(popular_books)]
            
            # Filtrar usuarios activos
            user_counts = self.ratings['User-ID'].value_counts()
            active_users = user_counts[
                user_counts >= Config.MIN_USER_RATINGS
            ].index
            self.ratings = self.ratings[self.ratings['User-ID'].isin(active_users)]
            
            # Sincronizar tablas
            self.books = self.books[
                self.books['ISBN'].isin(self.ratings['ISBN'].unique())
            ]
            self.users = self.users[
                self.users['User-ID'].isin(self.ratings['User-ID'].unique())
            ]
            
            logger.info(f"✓ Datos preparados - Ratings: {self.ratings.shape}")
        except Exception as e:
            logger.error(f"✗ Error preparando datos: {e}")
            raise
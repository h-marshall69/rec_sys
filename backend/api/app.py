# api\app.py
from flask import Flask
from config.settings import Config
from services.data_service import DataService
from services.recommender_service import RecommenderService
from services.user_service import UserService
from services.cache_service import CacheService
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def create_app():
    """Factory function para crear la app"""
    app = Flask(__name__)
    
    # Inicializar servicios
    global data, recommender, user_service, cache
    data = DataService()
    data.prepare_data()
    
    cache = CacheService()
    recommender = RecommenderService(data)
    recommender.build_matrices()
    user_service = UserService(data)
    
    logger.info("✓ Servicios inicializados")
    
    # Registrar blueprints
    from api.routes import recommendations, users, health, isbm
    app.register_blueprint(health.health_bp)
    app.register_blueprint(recommendations.recommendations_bp)
    app.register_blueprint(users.users_bp)
    app.register_blueprint(isbm.isbm_bp)
    
    logger.info("✓ Rutas registradas")
    
    return app
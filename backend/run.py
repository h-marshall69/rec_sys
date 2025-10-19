import os
from app import create_app
from app.config import DevelopmentConfig, ProductionConfig
from app.data.loader import DataLoader

config = DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else ProductionConfig

app = create_app(config)

@app.before_request
def load_data():
    """Cargar datos antes del primer request"""
    data_loader = DataLoader()
    if not data_loader.is_loaded():
        data_loader.load()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
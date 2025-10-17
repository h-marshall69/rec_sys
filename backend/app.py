from flask import Flask, jsonify
from flask_cors import CORS
from routes.genres import genres_bp
from routes.users import users_bp
from routes.recommendations import recommendations_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(genres_bp, url_prefix='/api/')
    app.register_blueprint(users_bp, url_prefix='/api/')
    app.register_blueprint(recommendations_bp, url_prefix='/api/')
    
    # Ruta de bienvenida
    @app.route('/')
    def index():
        return jsonify({
            'mensaje': 'API de Géneros de Películas',
            'endpoints': {
                'obtener_generos': '/api/genres',
            }
        })
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
from api.app import create_app
from config.settings import Config

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.API_HOST,
        port=Config.API_PORT,
        debug=Config.DEBUG
    )
# app/__init__.py
from flask import Flask
from config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = '691XyZ3Kqz123dsf'

    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%m-%d-%Y'):
        return datetime.strptime(value, '%Y-%m-%d').strftime(format)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
